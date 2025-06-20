import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))  # type: ignore

model = genai.GenerativeModel("gemini-1.5-flash")  # type: ignore

def generate_challenges(text):
    prompt = f"From the following document, generate 3 logic-based or comprehension questions:\n\n{text[:3000]}"
    response = model.generate_content(prompt)
    questions = response.text.strip().split('\n')
    return [q.strip() for q in questions if q.strip()]

def evaluate_response(question, answer, text):
    prompt = f"Evaluate the answer '{answer}' to the question '{question}' based on this document:\n\n{text[:3000]}"
    response = model.generate_content(prompt)
    return response.text.strip()
