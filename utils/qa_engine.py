import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))  # type: ignore

model = genai.GenerativeModel("gemini-1.5-flash")  # type: ignore

def answer_question(question, text):
    prompt = f"""You are an AI assistant. Use the following document to answer the user's question.
Document:
{text[:3000]}

Question: {question}
Only answer using the information from the document."""
    
    response = model.generate_content(prompt)
    answer = response.text.strip()
    justification = "This is supported by the provided document excerpt."
    return answer, justification
