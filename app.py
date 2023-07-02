from flask import Flask, request, render_template
from transformers import pipeline

# Initialize Flask app
app = Flask(__name__)


# Load the summarization pipeline
summarizer = pipeline("summarization", model="model")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    # Get the user input from the form
    org_text = request.form['text']
    app = request.form['application']
    platform = request.form['platform']
    
    text = f"customer:{app} type:{platform} {org_text}"
    
    max_len = int(len(text)*0.15)
    if max_len < 30:
        max_len = 30

    # Use the summarization pipeline to generate a summary
    summary = summarizer(text, max_length=max_len, min_length=30)[0]['summary_text']
    if "none" in summary[:5].lower():
        summary = "none"
    # Render the template with the summary result
    return render_template('result.html', text=org_text, summary=summary)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

