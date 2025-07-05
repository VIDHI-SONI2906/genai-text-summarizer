Brevify – Text Summarizer Using Generative AI

Brevify is a web application that summarizes long text (PDF, DOCX, TXT, or manual input) into concise summaries using Generative AI NLP models. Built with Flask, styled using HTML/CSS, and powered by Hugging Face’s sshleifer/distilbart-cnn-12-6 model.

Overview:

🔍 Features
Upload and summarize PDF, DOCX, or TXT files

Summarize manual text input

Output as Narrative, Bullet points, or Table

Clean and simple web interface


🤖 AI Models Used
Model Name

Use Case

sshleifer/distilbart-cnn-12-6

Text Summarization

(Extendable to:)

GPT-2, GPT-3

Text Generation

T5

Summarization, Q&A

BART

Text Summarization & Generation

Falcon, LLaMA, Bloom

Large Language Models


🛠️ Tech Stack

Frontend: HTML, CSS, Bootstrap

Backend: Python, Flask

AI: Hugging Face Transformers (via API)

NLP Task: Summarization


Getting Started:

🚀 Installation & Setup
Follow these steps to get Brevify up and running on your local machine.

1. Clone the Repository
git clone https://github.com/VIDHI-SONI2906/genai-text-summarizer.git
cd genai-text-summarizer

2. Create a Virtual Environment
It's highly recommended to use a virtual environment to manage project dependencies.

python -m venv venv

Activate the virtual environment:

On Windows:

.\venv\Scripts\activate

On macOS / Linux:

source venv/bin/activate

3. Install Dependencies
With your virtual environment activated, install the required Python packages:

pip install -r requirements.txt

4. Setup Hugging Face API Token
To interact with the Hugging Face Inference API, you need an API token.

Create an account at Hugging Face.

Go to Settings → Access Tokens and generate a new token with at least "read" permissions.

In the root of your project directory, create a new file named .env (note the leading dot).

Add your Hugging Face API token to this .env file:

HUGGINGFACE_API_TOKEN="hf_your_actual_token_here"

Important: Replace "hf_your_actual_token_here" with the token you generated. The .env file is already added to .gitignore to prevent it from being committed to your repository.

5. Run the Flask App
Ensure your virtual environment is active, and then run the Flask application:

python app.py

Visit the application in your web browser: http://127.0.0.1:5000

Screenshots
Home Page
![image](https://github.com/user-attachments/assets/b9b04e8d-0fc2-4a51-b082-7e1ad29da61f)

Summary Output
![image](https://github.com/user-attachments/assets/9fe68765-82d8-4ddd-b32f-b1005e71c0f3)



