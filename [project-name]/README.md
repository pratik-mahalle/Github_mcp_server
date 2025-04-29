# Project Title

## Description
This project is a Python application that integrates with the Gemini API for code analysis and the GitHub API for managing pull requests and comments. It uses Flask to handle incoming webhook events from GitHub.

## Features
- Analyze code changes using the Gemini API.
- Post comments on GitHub pull requests with feedback from Gemini.
- Manage GitHub pull requests, including adding labels and requesting reviews.

## Requirements
- Python 3.x
- Flask
- PyGithub
- requests

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone https://github.com/yourusername/project-name.git
   cd project-name
   ```

2. **Create a virtual environment (optional but recommended):**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the root directory and add your `GEMINI_API_KEY` and `GITHUB_WEBHOOK_SECRET`:
   ```
   GEMINI_API_KEY=your_gemini_api_key
   GITHUB_WEBHOOK_SECRET=your_github_webhook_secret
   ```

5. **Run the application:**
   ```
   python app.py
   ```

## Usage
- The application listens for GitHub webhook events at the `/webhook` endpoint.
- It processes pull requests and reviews, providing feedback and managing labels as specified.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.