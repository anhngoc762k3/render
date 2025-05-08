document.getElementById("questionForm").addEventListener("submit", function(event) {
    event.preventDefault();

    const question = document.getElementById("question").value;
    const responseElement = document.getElementById("answerText");

    fetch("/ask", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: new URLSearchParams({ "question": question })
    })
    .then(response => response.json())
    .then(data => {
        if (data.answer) {
            responseElement.innerHTML = data.answer;  // ⚠️ Cho phép <br> hoạt động
        } else if (data.error) {
            responseElement.innerHTML = "Lỗi: " + data.error;
        }
    })
    .catch(error => {
        responseElement.innerHTML = "Lỗi: " + error;
    });

    document.getElementById("question").value = ""; // Xoá ô nhập sau khi gửi
});
