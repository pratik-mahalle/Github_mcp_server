from flask import Flask, request, jsonify
import os
import hmac
import hashlib
from utils.github_utils import get_pull_request_diff, post_github_comment, add_github_label, request_github_reviewers, update_github_pull_request
from utils.gemini_utils import analyze_code_with_gemini, improve_text_with_gemini

app = Flask(__name__)

# Load GitHub webhook secret from environment variable
GITHUB_WEBHOOK_SECRET = os.environ.get("GITHUB_WEBHOOK_SECRET")

def verify_signature(data, signature, secret):
    """Verifies the GitHub webhook signature."""
    if secret is None:
        print("Warning: GITHUB_WEBHOOK_SECRET not set. Signature verification disabled.")
        return True  # Insecure, but allows local testing without the secret

    digest = hmac.new(secret.encode('utf-8'), data, hashlib.sha256).hexdigest()
    return hmac.compare_digest(f"sha256={digest}", signature)

@app.route('/webhook', methods=['POST'])
def webhook_handler():
    """Handles incoming GitHub webhook events."""
    signature = request.headers.get('X-Hub-Signature-256')
    raw_data = request.get_data()

    if not verify_signature(raw_data, signature, GITHUB_WEBHOOK_SECRET):
        print("Webhook signature verification failed.")
        return jsonify({'error': 'Invalid signature'}), 401

    payload = request.get_json()
    if payload is None:
        print("Failed to parse webhook payload.")
        return jsonify({'error': 'Invalid payload'}), 400

    event = request.headers.get('X-GitHub-Event')

    if event == 'pull_request':
        return handle_pull_request(payload)
    elif event == 'pull_request_review':
        return handle_pull_request_review(payload)
    # Add handlers for other relevant events here
    else:
        print(f"Received unhandled event: {event}")
        return jsonify({'message': 'Event received but not processed'}), 200

def handle_pull_request(payload):
    """Handles pull_request events."""
    action = payload.get('action')
    pull_request = payload.get('pull_request')
    repo_full_name = payload.get('repository', {}).get('full_name')
    pr_number = pull_request.get('number')

    if action in ['opened', 'synchronize']:
        print(f"Processing pull request {pr_number} in {repo_full_name} - Action: {action}")

        code_diff = get_pull_request_diff(repo_full_name, pr_number)
        if code_diff:
            gemini_feedback = analyze_code_with_gemini(code_diff)
            if gemini_feedback:
                comment = f"**Gemini Code Review:**\n\n{gemini_feedback}"
                post_github_comment(repo_full_name, pr_number, comment)
                add_github_label(repo_full_name, pr_number, "gemini-reviewed")
            else:
                print(f"Gemini analysis failed or returned no feedback for PR {pr_number}.")
        else:
            print(f"Could not retrieve code diff for PR {pr_number}.")

        return jsonify({'message': f'Pull request {pr_number} - {action} processed'}), 200
    elif action == 'closed':
        print(f"Pull request {pr_number} in {repo_full_name} closed.")
        return jsonify({'message': f'Pull request {pr_number} closed'}), 200
    else:
        return jsonify({'message': f'Pull request {pr_number} - {action} ignored'}), 200

def handle_pull_request_review(payload):
    """Handles pull_request_review events."""
    action = payload.get('action')
    review = payload.get('review')
    pull_request = payload.get('pull_request')
    repo_full_name = payload.get('repository', {}).get('full_name')
    pr_number = pull_request.get('number')
    review_state = review.get('state')

    print(f"Review for pull request {pr_number} in {repo_full_name} - Action: {action}, State: {review_state}")

    if action == 'submitted' and review_state == 'approved':
        print(f"Pull request {pr_number} approved. You might want to add logic to auto-merge or add a merge label here.")
        add_github_label(repo_full_name, pr_number, "approved")
    elif action == 'submitted' and review_state == 'changes_requested':
        print(f"Pull request {pr_number} requested changes.")
        add_github_label(repo_full_name, pr_number, "changes-requested")

    return jsonify({'message': f'Review for PR {pr_number} - {action} ({review_state}) received'}), 200

@app.route('/')
def health_check():
    """Simple health check endpoint for Lambda."""
    return jsonify({'status': 'OK'}), 200

if __name__ == '__main__':
    app.run(debug=True)