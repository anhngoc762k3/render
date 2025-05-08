document.getElementById("questionForm").addEventListener("submit", function(event) {
    event.preventDefault();

    const question = document.getElementById("question").value;
    const chatHistory = document.getElementById("chatHistory");

    fetch("/ask", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: new URLSearchParams({ "question": question })
    })
    .then(response => response.json())
    .then(data => {
        if (data.history && Array.isArray(data.history)) {
            // Xóa lịch sử cũ
            chatHistory.innerHTML = "";

            // Hiển thị tất cả các cặp hỏi & đáp
            data.history.forEach(pair => {
                const block = document.createElement("div");
                block.classList.add("chat-block");

                block.innerHTML = `
                    <p><strong>Câu hỏi:</strong> ${pair.question}</p>
                    <p><strong>Trả lời:</strong> ${pair.answer}</p>
                    <hr>
                `;
                chatHistory.appendChild(block);
            });
        } else if (data.error) {
            chatHistory.innerHTML = `<p>Lỗi: ${data.error}</p>`;
        }
    })
    .catch(error => {
        chatHistory.innerHTML = `<p>Lỗi: ${error}</p>`;
    });

    document.getElementById("question").value = ""; // Xóa ô nhập
});
