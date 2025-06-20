function submitQuestion() {
  const question = document.getElementById('questionInput').value.trim();
  const doc_text = document.getElementById('doc_text').value;

  if (!question) {
    alert("Please enter a question.");
    return;
  }

  fetch('/ask', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: `question=${encodeURIComponent(question)}&doc_text=${encodeURIComponent(doc_text)}`
  })
  .then(response => response.json())
  .then(data => {
    document.getElementById('answerOutput').innerHTML = `
      <strong>Answer:</strong> ${data.answer}<br>
      <em>Justification:</em> ${data.justification}
    `;
    document.getElementById('questionInput').value = '';
  })
  .catch(error => {
    console.error('Error:', error);
    document.getElementById('answerOutput').innerHTML = '❌ Failed to get a response. Please try again.';
  });
}

function getChallenges() {
  const doc_text = document.getElementById('doc_text').value;

  fetch('/challenge', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: `doc_text=${encodeURIComponent(doc_text)}`
  })
  .then(response => response.json())
  .then(data => {
    let html = '';
    data.questions.forEach((q, i) => {
      html += `<p><strong>Q${i+1}:</strong> ${q}</p><input type="text" id="ans${i}" placeholder="Your answer"><br>`;
    });
    html += `<button onclick="submitAnswers(${data.questions.length})">Submit Answers</button>`;
    document.getElementById('challengeOutput').innerHTML = html;
  })
  .catch(error => {
    console.error('Error:', error);
    document.getElementById('challengeOutput').innerHTML = '❌ Failed to generate questions.';
  });
}

function submitAnswers(count) {
  const doc_text = document.getElementById('doc_text').value;
  const answers = {};

  for (let i = 0; i < count; i++) {
    answers[i] = document.getElementById(`ans${i}`).value.trim();
  }

  fetch('/evaluate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ doc_text, answers })
  })
  .then(response => response.json())
  .then(data => {
    let html = '<h4>Evaluation:</h4>';
    data.evaluations.forEach((e, i) => {
      html += `<p><strong>Q${i+1} Feedback:</strong> ${e}</p>`;
    });
    document.getElementById('challengeOutput').innerHTML += html;
  })
  .catch(error => {
    console.error('Error:', error);
    document.getElementById('challengeOutput').innerHTML += '<p>❌ Failed to evaluate answers.</p>';
  });
}
