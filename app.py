from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

from utils.summarizer import summarize_document
from utils.qa_engine import answer_question
from utils.logic_challenge import generate_challenges, evaluate_response

load_dotenv()

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        uploaded_file = request.files['document']
        if uploaded_file:
            filepath = os.path.join(UPLOAD_FOLDER, uploaded_file.filename) # type: ignore
            uploaded_file.save(filepath)

            summary, text = summarize_document(filepath)
            return render_template('result.html', summary=summary, doc_text=text)
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    question = request.form.get('question', '').strip()
    text = request.form.get('doc_text', '').strip()

    if not text:
        return jsonify({
            'answer': 'There is no document content available to answer from.',
            'justification': 'Document text is missing or empty.'
        })

    answer, justification = answer_question(question, text)
    return jsonify({'answer': answer, 'justification': justification})

@app.route('/challenge', methods=['POST'])
def challenge():
    text = request.form.get('doc_text', '').strip()

    if not text:
        return jsonify({'questions': ['No document text found to generate questions.']})

    questions = generate_challenges(text)
    return jsonify({'questions': questions})

@app.route('/evaluate', methods=['POST'])
def evaluate():
    text = request.json.get('doc_text', '').strip() # type: ignore
    answers = request.json.get('answers', {}) # type: ignore

    if not text or not answers:
        return jsonify({'evaluations': ['Missing document or answers.']})

    evaluations = [evaluate_response(f"Q{i+1}", ans, text) for i, ans in enumerate(answers.values())]
    return jsonify({'evaluations': evaluations})

if __name__ == '__main__':
    app.run(debug=True)
