from flask import Flask, render_template, request
import os
import re
import sys
import json
import pdfplumber
from g4f.client import Client

app = Flask(__name__)
client = Client()

os.environ["G4F_NO_UPDATE"] = "true"
os.environ["G4F_DEBUG"] = "false"

pdf_file_path = "data1.pdf"
json_file_path = "data.json"

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

def read_json(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        return {"error": f"Lỗi đọc file JSON: {str(e)}"}

def find_related_link(question, json_data):
    try:
        links = []
        for item in json_data.get("bai_hoc", []):
            if item["keyword"].lower() in question.lower():
                links.append(f'<a href="{item["link"]}" target="_blank">{item["link"]}</a>')
        return "<br><br><strong>Link bài học liên quan:</strong><br>" + "<br>".join(links) if links else ""
    except:
        return ""

def generate_response(question, pdf_text, json_data):
    try:
        thong_tin = "\n".join(json_data.get("thong_tin", []))
        context = (pdf_text + "\n" + thong_tin)[:6000]
        prompt = f"Đây là thông tin tổng hợp từ tài liệu PDF và JSON:\n{context}\n\nCâu hỏi: {question}\nTrả lời:"

        with HiddenPrints():
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                stream=False
            )
        answer = response.choices[0].message.content.strip()
        answer = re.sub(r'\n+', '\n', answer)

        # Gợi ý link bài học nếu có
        link_part = find_related_link(question, json_data)
        return answer + ("\n" + link_part if link_part else "")
    except Exception as e:
        return f"Đã xảy ra lỗi: {str(e)}"

@app.route("/", methods=["GET", "POST"])
def index():
    answer = ""
    question = ""
    if request.method == "POST":
        question = request.form.get("question", "")
        if question:
            pdf_text = read_pdf(pdf_file_path)
            json_data = read_json(json_file_path)
            if "error" in json_data or "Lỗi" in pdf_text:
                answer = "Lỗi khi đọc dữ liệu từ file PDF hoặc JSON."
            else:
                answer = generate_response(question, pdf_text, json_data)
                answer = answer.replace("\n", "<br>")
    return render_template("index.html", answer=answer, question=question)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
