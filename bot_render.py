from flask import Flask, request, jsonify
import os, re, sys
import pdfplumber
from g4f.client import Client

app = Flask(__name__)
client = Client()

os.environ["G4F_NO_UPDATE"] = "true"
os.environ["G4F_DEBUG"] = "false"

pdf_file_path = "MTvE2.pdf"  

class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        self._original_stderr = sys.stderr
        sys.stdout = open(os.devnull, 'w')
        sys.stderr = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stderr.close()
        sys.stdout = self._original_stdout
        sys.stderr = self._original_stderr

def read_pdf(file_path):
    try:
        with pdfplumber.open(file_path) as pdf:
            text = ""
            for page in pdf.pages:
                extracted_text = page.extract_text()
                if extracted_text:
                    text += extracted_text + "\n"
        return text
    except Exception as e:
        return f"Lỗi đọc file PDF: {str(e)}"

def generate_response(question, pdf_text):
    try:
        context = pdf_text[:6000] if len(pdf_text) > 6000 else pdf_text
        prompt = f"Đây là một đoạn văn từ tài liệu: {context}\n\nCâu hỏi: {question}\nTrả lời:"

        with HiddenPrints():
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                stream=False
            )
        answer = response.choices[0].message.content.strip()
        answer = re.sub(r'\n+', '\n', answer)
        return answer
    except Exception as e:
        return f"Đã xảy ra lỗi: {str(e)}"

@app.route("/ask", methods=["POST"])
def ask_question():
    data = request.get_json()
    question = data.get("question", "")
    if not question:
        return jsonify({"error": "Missing question"}), 400

    pdf_text = read_pdf(pdf_file_path)
    if "Lỗi đọc file PDF" in pdf_text:
        return jsonify({"error": pdf_text}), 500

    answer = generate_response(question, pdf_text)
    return jsonify({"answer": answer})

@app.route("/", methods=["GET"])
def home():
    return "API is running11."

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000)) 
    app.run(host="0.0.0.0", port=port)