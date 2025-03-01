from flask import Flask, render_template, request
from google import genai
import PyPDF2

app = Flask(__name__)

# Configure Gemini API - Replace with your API key
API_KEY = "Get your own api"
client = genai.Client(api_key=API_KEY)

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def analyze_text_with_gemini(text, query):
    prompt = f"Based on the following text, {query}\n\nText: {text}"
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Error in Gemini API: {str(e)}"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'pdf_file' not in request.files:
            return render_template('index.html', error='No file uploaded')
        
        pdf_file = request.files['pdf_file']
        query = request.form.get('query', 'Please summarize this document')
        
        if pdf_file.filename == '':
            return render_template('index.html', error='No file selected')
        
        try:
            # Extract text from PDF
            text = extract_text_from_pdf(pdf_file)
            
            # Analyze text using Gemini
            result = analyze_text_with_gemini(text, query)
            
            return render_template('index.html', result=result)
        
        except Exception as e:
            return render_template('index.html', error=f'Error: {str(e)}')
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)