# Smart Research Assistant

A web-based assistant that helps users upload research documents (PDF, TXT), generates concise summaries, answers questions based on the document, and creates logic-based comprehension challenges.

---

## Features

- **Document Upload:** Supports PDF and TXT files.
- **Summarization:** Generates a 150-word summary using Google Gemini (abstractive) or fallback extractive summarization.
- **Question Answering:** Users can ask questions about the uploaded document and receive context-based answers.
- **Logic Challenges:** Generates logic/comprehension questions from the document and evaluates user responses.

---

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd <your-repo-directory>
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Variables:**
   - Create a `.env` file in the root directory.
   - Add your Google Gemini API key:
     ```
     GEMINI_API_KEY=your_gemini_api_key_here
     ```

4. **Download NLTK Data:**
   - The app will attempt to download the required NLTK tokenizer (`punkt`) automatically on first run.

5. **Run the application:**
   ```bash
   python app.py
   ```
   - The app will be available at `http://127.0.0.1:5000/`.

---

## Architecture / Reasoning Flow

### 1. **Frontend (User Interface)**
- Users access a clean web interface (`index.html`) to upload their research document.
- After upload, the app displays a summary and provides interactive fields for Q&A and logic challenges (`result.html`).

### 2. **Backend (Flask App)**
- **File Upload:** Handles file uploads and saves them to the `uploads/` directory.
- **Summarization:**
  - Extracts text from PDF/TXT.
  - Cleans and tokenizes sentences.
  - Uses Google Gemini for abstractive summarization (150 words).
  - If Gemini fails, falls back to extractive summarization using TF-IDF and KMeans clustering.
- **Q&A:**
  - Accepts user questions.
  - Sends the question and document excerpt to Gemini for an answer, ensuring responses are grounded in the document.
- **Logic Challenges:**
  - Generates 3 logic/comprehension questions from the document using Gemini.
  - Evaluates user answers to these questions for correctness and justification.

### 3. **Core Modules**
- `utils/summarizer.py`: Handles text extraction, cleaning, and both abstractive/extractive summarization.
- `utils/qa_engine.py`: Handles question answering using Gemini.
- `utils/logic_challenge.py`: Generates and evaluates logic-based questions using Gemini.

### 4. **APIs & Endpoints**
- `/` : Main page for upload and summary.
- `/ask` : POST endpoint for Q&A.
- `/challenge` : POST endpoint to generate logic questions.
- `/evaluate` : POST endpoint to evaluate user answers to challenges.

---

## Requirements

- Python 3.7+
- See `requirements.txt` for all dependencies:
  - flask
  - openai
  - pdfplumber
  - nltk
  - scikit-learn
  - python-dotenv

---

## Notes

- The app uses Google Gemini for most NLP tasks. Ensure your API key is valid and has sufficient quota.
- Only PDF and TXT files are supported for upload.
- For best results, use research papers or well-structured documents.
