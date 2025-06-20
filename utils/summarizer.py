import os
import nltk
import fitz
import numpy as np
import google.generativeai as genai
from dotenv import load_dotenv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY")) # type: ignore

nltk.download('punkt')

def read_text(filepath):
    """Reads and extracts text from PDF or TXT file using PyMuPDF."""
    if filepath.endswith('.pdf'):
        doc = fitz.open(filepath)
        return "\n".join(page.get_text() for page in doc) # type: ignore
    elif filepath.endswith('.txt'):
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    return ""

def clean_sentences(sentences):
    """Removes very short or non-informative lines like bullets or numbers."""
    return [s for s in sentences if len(s.split()) > 5 and not s.strip().startswith(('•', '●', '-', '–', '▪', '1.', '2.', '3.'))]

def abstractive_summary(text):
    """Uses Gemini model to generate a clean 150-word summary."""
    prompt = f"Summarize the following research paper content in under 150 words:\n\n{text[:10000]}"
    try:
        model = genai.GenerativeModel("gemini-1.5-flash") # type: ignore
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return "Abstractive summarization failed: " + str(e)

def extractive_summary(sentences, max_sentences=5):
    """TF-IDF and KMeans based extractive summary."""
    tfidf = TfidfVectorizer(stop_words='english')
    X = tfidf.fit_transform(sentences)
    kmeans = KMeans(n_clusters=min(max_sentences, len(sentences)), random_state=0)
    kmeans.fit(X)
    closest, _ = pairwise_distances_argmin_min(kmeans.cluster_centers_, X.toarray())  # type: ignore
    selected = [sentences[i] for i in sorted(closest)]
    return ' '.join(selected)

def summarize_document(filepath, max_sentences=5):
    """Returns a 150-word summary + full cleaned text."""
    text = read_text(filepath).strip()

    if not text:
        return "Document contains no readable text.", ""

    raw_sentences = nltk.sent_tokenize(text)
    sentences = clean_sentences(raw_sentences)

    if len(sentences) == 0:
        return "Document structure not suitable for summarization.", text

    try:
        summary = abstractive_summary(text)
        return summary, text
    except:
        summary = extractive_summary(sentences, max_sentences)
        return summary[:150] + '...', text
