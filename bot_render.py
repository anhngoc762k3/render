import asyncio
import json
import os
from flask import Flask, request, jsonify
from g4f.client import Client
import pdfplumber

# Thiết lập vòng lặp sự kiện cho Windows (chỉ dùng khi chạy trên Windows)
if os.name == "nt":
    from asyncio import WindowsSelectorEventLoopPolicy
    asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())

# Khởi tạo client của g4f
client = Client()

# Hàm đọc nội dung từ file PDF
def read_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

# Hàm trả lời câu hỏi dựa trên nội dung PDF
def generate_response(question, pdf_text):
    try:
        # Giới hạn ngữ cảnh nếu văn bản quá dài
        context = pdf_text[:6000] if len(pdf_text) > 6000 else pdf_text

        # Thiết lập prompt với câu hỏi và ngữ cảnh
        prompt = f"Đây là một đoạn văn từ tài liệu: {context}\n\nCâu hỏi: {question}\nTrả lời:"

        # Sử dụng g4f.client để gọi mô hình OpenAI
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Chọn mô hình
            messages=[{"role": "user", "content": prompt}],
        )

        # Trích xuất câu trả lời từ kết quả trả về
        answer = response.choices[0].message.content
        return answer
    except Exception as e:
        return f"Đã xảy ra lỗi: {str(e)}"

# Đọc nội dung từ file PDF
pdf_file_path = 'DATAA.pdf'  # Thay bằng đường dẫn đến file PDF của bạn
pdf_text = read_pdf(pdf_file_path)

# Khởi tạo Flask app
app = Flask(__name__)

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    question = data.get('question')

    if not question:
        return jsonify({"error": "Không nhận được câu hỏi."}), 400

    answer = generate_response(question, pdf_text)
    return jsonify({"answer": answer})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Đảm bảo chọn cổng đúng cho Render
    app.run(host="0.0.0.0", port=port)
