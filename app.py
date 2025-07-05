import os # Import the os module to access environment variables
from flask import Flask, render_template, request, jsonify
import requests # Used for making API calls to Hugging Face Inference API
import docx # Used for handling .docx files
from pdfminer.high_level import extract_text # Used for handling .pdf files
from dotenv import load_dotenv # Import load_dotenv from python-dotenv

# Load environment variables from .env file.
# This must be called early in your application's lifecycle to ensure variables are loaded.
load_dotenv()

app = Flask(__name__) # Correct Flask app initialization

# --- Hugging Face API Configuration ---
# Retrieve API URL from environment variables, with a fallback default
HUGGINGFACE_API_URL = os.getenv('HUGGINGFACE_API_URL', 'https://api-inference.huggingface.co/models/sshleifer/distilbart-cnn-12-6')

# Retrieve API Token from environment variables.
# This ensures your token is not hardcoded and remains secure.
HUGGINGFACE_API_TOKEN = os.getenv('HUGGINGFACE_API_TOKEN')

# Crucial check: If the API token is not found, raise an error to prevent insecure operations.
if not HUGGINGFACE_API_TOKEN:
    raise ValueError("HUGGINGFACE_API_TOKEN not found in environment variables. Please ensure your .env file is correctly configured and loaded.")

# Set up the headers for API requests using the loaded token
headers = {
    "Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"
}

# --- Flask Routes ---
@app.route('/')
def home():
    """Renders the main summarizer page."""
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    """
    Handles text summarization requests from the frontend.
    Accepts text input.
    """
    try:
        data = request.form.get('text', '')
        summary_length = int(request.form.get('length', 150))
        format_type = request.form.get('format', 'narrative')

        if not data.strip():
            return jsonify({"error": "Text is empty"}), 400

        payload = {
            "inputs": data,
            "parameters": {
                "max_length": summary_length,
                "min_length": 40,
                "do_sample": False
            }
        }

        # Make the request to the Hugging Face Inference API
        # Ensure the response variable is not duplicated (response = response = ...)
        response = requests.post(HUGGINGFACE_API_URL, headers=headers, json=payload, timeout=60)

        if response.status_code != 200:
            # Log the full API response for debugging in case of failure
            print(f"API request failed with status code {response.status_code}: {response.text}")
            return jsonify({"error": f"API request failed ({response.status_code}): {response.text}"}), 500

        output = response.json()
        if isinstance(output, list) and 'summary_text' in output[0]:
            summary_text = output[0]['summary_text']
        else:
            # Log unexpected response structure from the API
            print(f"Unexpected API response format: {output}")
            return jsonify({"error": "Unexpected API response format"}), 500

        print("Final Summary:", summary_text) # Debugging print for server console

        formatted = format_summary(summary_text, format_type)

        # Check if the request is an AJAX call (typical for fetching just JSON)
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({"summary": formatted, "original": data})

        # For non-AJAX requests, render the template with the summary
        return render_template('index.html', original_text=data, summary=formatted)

    except requests.exceptions.Timeout:
        print("Error: Hugging Face API request timed out.")
        return jsonify({"error": "Hugging Face API request timed out. Please try again."}), 504
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to Hugging Face API. Check internet connection.")
        return jsonify({"error": "Could not connect to Hugging Face API. Please check your internet connection."}), 503
    except Exception as e:
        # Catch any other unexpected errors during summarization
        print("Error during summarization:", str(e))
        return jsonify({"error": str(e)}), 500

@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Handles file uploads (PDF, DOCX, TXT) and extracts text.
    """
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files['file']
        filename = file.filename.lower()

        if filename.endswith('.pdf'):
            # pdfminer.high_level.extract_text expects a file-like object
            text = extract_text(file)
        elif filename.endswith('.docx'):
            # docx.Document expects a file-like object
            text = extract_text_from_docx(file)
        elif filename.endswith('.txt'):
            text = file.read().decode('utf-8')
        else:
            return jsonify({"error": "Unsupported file type"}), 400

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({"text": text})

        return render_template('index.html', original_text=text)
    except Exception as e:
        # Catch any other unexpected errors during file upload/extraction
        print("Error during file upload/extraction:", str(e))
        return jsonify({"error": str(e)}), 500

def extract_text_from_docx(file):
    """Helper function to extract text from a DOCX file."""
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

def format_summary(summary, format_type):
    """Formats the summary based on the requested type."""
    if format_type == "bullet":
        # Simple bullet point conversion. For more robust results, consider NLP libraries.
        sentences = [s.strip() for s in summary.replace(". ", ".\n").split('\n') if s.strip()]
        return "<br>".join([f"• {point}" for point in sentences])
    elif format_type == "table":
        # For tabular format, a simple text summary is usually placed in one cell.
        # If you need structured data in a table, the summarization model would need to output it.
        return f"<table class='table table-bordered'><tr><td>{summary}</td></tr></table>"
    return summary # Default to narrative format

if __name__ == "__main__":
    # Get Flask configuration from environment variables (loaded from .env)
    # Default to True for debug, 127.0.0.1 for host, and 5000 for port
    debug_mode = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    host = os.getenv('FLASK_HOST', '127.0.0.1')
    port = int(os.getenv('FLASK_PORT', 5000))
    
    app.run(debug=debug_mode, host=host, port=port)
