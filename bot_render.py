from flask import Flask, request, jsonify, render_template
import pdfplumber
from g4f.client import Client
import os

app = Flask(__name__)
client = Client()

# Đường dẫn file PDF
pdf_file_path = "MTvE2.pdf"

# Hàm đọc nội dung từ file PDF
def read_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

# Hàm trả lời câu hỏi dựa trên nội dung PDF
def generate_response(question, pdf_text):
    context = pdf_text[:6000] if len(pdf_text) > 6000 else pdf_text
    prompt = f"Đây là một đoạn văn từ tài liệu: {context}\n\nCâu hỏi: {question}\nTrả lời:"

    response = client.chat.completions.create(
        model="gpt-4",  # hoặc model bạn muốn sử dụng
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content.strip()

# Đọc nội dung từ file PDF
pdf_text = read_pdf(pdf_file_path)

@app.route('/')
def index():
    return render_template('index.html')  # Đảm bảo bạn có file index.html trong thư mục templates

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    question = data.get('question')
    if not question:
        return jsonify({"error": "Không nhận được câu hỏi."}), 400

    answer = generate_response(question, pdf_text)
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(debug=True)
