import os
import requests
import json

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta"  # Adjust if the API version changes
GEMINI_MODEL = "gemini-pro"  # Or the specific model you want to use

def analyze_code_with_gemini(code_diff, prompt_template="Review the following code changes and provide feedback, suggestions for improvement, and identify potential issues:\n\n{}\n\n"):
    """Sends code diff to Gemini for analysis."""
    if not GEMINI_API_KEY:
        print("Error: GEMINI_API_KEY environment variable not set.")
        return None

    url = f"{GEMINI_BASE_URL}/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
    prompt = prompt_template.format(code_diff)
    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raise an exception for bad status codes
        response_data = response.json()
        # Extract the text response from Gemini - adjust based on actual API response structure
        if "candidates" in response_data and response_data["candidates"]:
            for candidate in response_data["candidates"]:
                if "content" in candidate and "parts" in candidate["content"]:
                    for part in candidate["content"]["parts"]:
                        if "text" in part:
                            return part["text"]
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error communicating with Gemini API for code analysis: {e}")
        return None
    except json.JSONDecodeError:
        print("Error decoding Gemini API response for code analysis.")
        return None

def improve_text_with_gemini(text, task_description="Improve the following text for clarity and conciseness:\n\n{}\n\n"):
    """Sends text to Gemini for improvement (e.g., PR titles, descriptions)."""
    if not GEMINI_API_KEY:
        print("Error: GEMINI_API_KEY environment variable not set.")
        return None

    url = f"{GEMINI_BASE_URL}/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
    prompt = task_description.format(text)
    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raise an exception for bad status codes
        response_data = response.json()
        # Extract the text response from Gemini - adjust based on actual API response structure
        if "candidates" in response_data and response_data["candidates"]:
            for candidate in response_data["candidates"]:
                if "content" in candidate and "parts" in candidate["content"]:
                    for part in candidate["content"]["parts"]:
                        if "text" in part:
                            return part["text"]
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error communicating with Gemini API for text improvement: {e}")
        return None
    except json.JSONDecodeError:
        print("Error decoding Gemini API response for text improvement.")
        return None

# You can add more Gemini interaction functions as needed