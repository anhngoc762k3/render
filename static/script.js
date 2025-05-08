document.getElementById("questionForm").addEventListener("submit", function(event) {
    event.preventDefault();

    const questionInput = document.getElementById("question");
    const question = questionInput.value.trim();
    if (!question) return;

    fetch('/ask', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({ 'question': question })
    })
    .then(response => response.json())
    .then(data => {
        const historyDiv = document.getElementById("history");

        const userMessage = document.createElement("p");
        userMessage.innerHTML = "<strong>Bạn:</strong> " + question;
        historyDiv.appendChild(userMessage);

        const botMessage = document.createElement("p");
        botMessage.innerHTML = "<strong>Trả lời:</strong> " + (data.answer || data.error || "Không có phản hồi");
        historyDiv.appendChild(botMessage);

        questionInput.value = "";
        historyDiv.scrollTop = historyDiv.scrollHeight;
    })
    .catch(error => {
        const historyDiv = document.getElementById("history");
        const errorMessage = document.createElement("p");
        errorMessage.innerHTML = "<strong>Lỗi:</strong> " + error;
        historyDiv.appendChild(errorMessage);
    });
});
