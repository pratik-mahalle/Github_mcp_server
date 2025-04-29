from flask import Flask, request, jsonify
import os
import hmac
import hashlib
# Import your GitHub and Gemini interaction functions later

app = Flask(__name__)

# Load GitHub webhook secret from environment variable
GITHUB_WEBHOOK_SECRET = os.environ.get("GITHUB_WEBHOOK_SECRET")

def verify_signature(data, signature, secret):
    """Verifies the GitHub webhook signature."""
    if secret is None:
        return False
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
    # Add handlers for other relevant events
    else:
        print(f"Received unhandled event: {event}")
        return jsonify({'message': 'Event received but not processed'}), 200

def handle_pull_request(payload):
    """Handles pull_request events."""
    action = payload.get('action')
    pull_request = payload.get('pull_request')
    if action in ['opened', 'synchronize', 'reopened']:
        print(f"Processing pull request {pull_request['number']} - Action: {action}")
        # Implement your Gemini and decision logic here
        return jsonify({'message': f'Pull request {pull_request["number"]} - {action} received'}), 200
    else:
        return jsonify({'message': f'Pull request {pull_request["number"]} - {action} ignored'}), 200

def handle_pull_request_review(payload):
    """Handles pull_request_review events."""
    action = payload.get('action')
    review = payload.get('review')
    pull_request = payload.get('pull_request')
    print(f"Processing review for pull request {pull_request['number']} - Action: {action}")
    # Implement your Gemini and decision logic based on review state
    return jsonify({'message': f'Review for PR {pull_request["number"]} - {action} received'}), 200

@app.route('/')
def health_check():
    """Simple health check endpoint for Lambda."""
    return jsonify({'status': 'OK'}), 200

if __name__ == '__main__':
    app.run(debug=True)