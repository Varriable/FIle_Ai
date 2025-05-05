import openai
import os
from docx import Document
import magic
from django.conf import settings
from openai import OpenAI
import requests
from PyPDF2 import PdfReader
import magic
from dotenv import load_dotenv

# Load .env file from the project root
load_dotenv()


HF_API_TOKEN = os.getenv("HF_API_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/sshleifer/distilbart-cnn-12-6"


def extract_text(file_path):
    """Extract text from PDF, DOCX, and TXT files"""
    try:
        file_type = magic.from_file(file_path, mime=True)
        
        if 'pdf' in file_type:
            with open(file_path, 'rb') as f:
                reader = PdfReader(f)
                return "\n".join([page.extract_text() for page in reader.pages])
        
        elif 'word' in file_type or 'officedocument' in file_type:
            doc = Document(file_path)
            return "\n".join([para.text for para in doc.paragraphs])
        
        elif 'text/plain' in file_type:
            with open(file_path, 'r') as f:
                return f.read()
        
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
    
    except Exception as e:
        raise RuntimeError(f"Text extraction failed: {str(e)}")

# def analyze_content(text, query=None):
#     headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
    
#     # Model-specific prompt format
#     prompt = f"""<｜begin▁of▁sentence｜>[INST]
#     <<SYS>>
#     You are a helpful document analysis assistant. { "Answer the question based on the document." if query else "Provide a concise summary." }
#     <</SYS>>
    
#     Document Content:
#     {text[:2500]}
    
#     {"Question: " + query if query else "Summary Request:"}
#     [/INST]"""
    
#     payload = {
#         "inputs": prompt,
#         "parameters": {
#             "max_new_tokens": 500,
#             "temperature": 0.3,
#             "repetition_penalty": 1.2
#         }
#     }
    
#     try:
#         response = requests.post(API_URL, headers=headers, json=payload)
        
#         if response.status_code == 200:
#             return response.json()[0]['generated_text'].split("[/INST]")[-1].strip()
#         else:
#             return f"API Error: {response.text}"

#     except Exception as e:
#         return f"AI Error: {str(e)}"
    
# def analyze_content(text, query=None):
#     headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
    
#     # Clean and truncate text
#     cleaned_text = text[:1024]  # Model's max input length
    
#     payload = {
#         "inputs": cleaned_text,
#         "parameters": {
#             "max_length": 150,
#             "min_length": 30,
#             "do_sample": False
#         }
#     }
    
#     try:
#         response = requests.post(API_URL, headers=headers, json=payload)
        
#         if response.status_code == 200:
#             # Correct response format for summarization model
#             return response.json()[0]['summary_text'].strip()
#         else:
#             return f"API Error ({response.status_code}): {response.text}"

#     except Exception as e:
#         return f"AI Error: {str(e)}"

def analyze_content(text, query=None):
    """
    Analyze text using LM Studio's OpenAI-compatible local server.
    If query is provided, the model will attempt to answer it based on the text.
    Otherwise, a summary is generated.
    """
    try:
        url = "http://localhost:1234/v1/chat/completions"

        headers = {
            "Content-Type": "application/json"
        }

        # Truncate text if needed
        context = text[:3000]

        system_prompt = "You are a helpful assistant. Summarize or answer based on the document."
        user_prompt = f"Document:\n{context}\n\n{'Question: ' + query if query else 'Please summarize this document.'}"

        payload = {
            "model": "local-model",  # Placeholder name; LM Studio doesn't use it
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.5
        }

        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content'].strip()
        else:
            return f"API Error ({response.status_code}): {response.text}"

    except Exception as e:
        return f"AI Error: {str(e)}"
