import os
from github import Github

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GITHUB_USERNAME = os.environ.get("GITHUB_USERNAME")  # Optional, but might be useful

def get_github_client():
    """Returns an authenticated GitHub client."""
    if not GITHUB_TOKEN:
        print("Error: GITHUB_TOKEN environment variable not set.")
        return None
    return Github(GITHUB_TOKEN)

def get_pull_request_diff(repo_name, pull_request_number):
    """Fetches the diff content of a pull request."""
    g = get_github_client()
    if not g:
        return None
    try:
        repo = g.get_repo(repo_name)
        pull = repo.get_pull(pull_request_number)
        return pull.get_patch()
    except Exception as e:
        print(f"Error fetching diff for {repo_name}#{pull_request_number}: {e}")
        return None

def post_github_comment(repo_name, issue_number, comment):
    """Posts a comment on a GitHub issue (which includes pull requests)."""
    g = get_github_client()
    if not g:
        return None
    try:
        repo = g.get_repo(repo_name)
        issue = repo.get_issue(issue_number)
        issue.create_comment(comment)
        print(f"Comment posted on {repo_name}#{issue_number}")
        return True
    except Exception as e:
        print(f"Error posting comment on {repo_name}#{issue_number}: {e}")
        return False

def add_github_label(repo_name, issue_number, label):
    """Adds a label to a GitHub issue (which includes pull requests)."""
    g = get_github_client()
    if not g:
        return None
    try:
        repo = g.get_repo(repo_name)
        issue = repo.get_issue(issue_number)
        issue.add_to_labels(label)
        print(f"Label '{label}' added to {repo_name}#{issue_number}")
        return True
    except Exception as e:
        print(f"Error adding label to {repo_name}#{issue_number}: {e}")
        return False

def request_github_reviewers(repo_name, pull_request_number, reviewers=None, team_reviewers=None):
    """Requests reviewers for a GitHub pull request."""
    g = get_github_client()
    if not g:
        return None
    if not reviewers and not team_reviewers:
        print(f"Warning: No reviewers or team reviewers specified for {repo_name}#{pull_request_number}")
        return False
    try:
        repo = g.get_repo(repo_name)
        pull = repo.get_pull(pull_request_number)
        pull.create_review_request(reviewers=reviewers, team_reviewers=team_reviewers)
        print(f"Review requested for {repo_name}#{pull_request_number} with reviewers: {reviewers}, team reviewers: {team_reviewers}")
        return True
    except Exception as e:
        print(f"Error requesting reviewers for {repo_name}#{pull_request_number}: {e}")
        return False

def update_github_pull_request(repo_name, pull_request_number, title=None, body=None, state=None, base=None, maintainer_can_modify=None):
    """Updates details of a GitHub pull request."""
    g = get_github_client()
    if not g:
        return None
    try:
        repo = g.get_repo(repo_name)
        pull = repo.get_pull(pull_request_number)
        update_data = {}
        if title is not None:
            update_data['title'] = title
        if body is not None:
            update_data['body'] = body
        if state is not None and state.lower() in ['open', 'closed']:
            update_data['state'] = state.lower()
        if base is not None:
            update_data['base'] = base
        if maintainer_can_modify is not None:
            update_data['maintainer_can_modify'] = maintainer_can_modify

        if update_data:
            pull.edit(**update_data)
            print(f"Pull request {repo_name}#{pull_request_number} updated: {update_data}")
            return True
        else:
            print(f"No updates specified for pull request {repo_name}#{pull_request_number}")
            return True
    except Exception as e:
        print(f"Error updating pull request {repo_name}#{pull_request_number}: {e}")
        return False