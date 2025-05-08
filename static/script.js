const chatbox = document.getElementById("chatbox");
const form = document.getElementById("questionForm");
const input = document.getElementById("question");

form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const question = input.value.trim();
    if (!question) return;

    appendMessage("Bạn", question, "user");
    input.value = "";

    // Hiển thị trạng thái đang xử lý
    appendMessage("Bot", "Đang xử lý...", "bot", true);

    try {
        const response = await fetch("/ask", {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: new URLSearchParams({ question })
        });

        const data = await response.json();
        const answer = data.answer || data.error || "Không có phản hồi.";

        // Xóa dòng "Đang xử lý..."
        removeLastMessage();

        appendMessage("Bot", answer, "bot");
    } catch (error) {
        removeLastMessage();
        appendMessage("Bot", "❌ Lỗi khi kết nối server: " + error.message, "bot");
    }

    input.focus();
});

function appendMessage(sender, text, cls, isTemp = false) {
    const div = document.createElement("div");
    div.classList.add("message");
    if (isTemp) div.classList.add("temp");

    div.innerHTML = `<span class="${cls}">${sender}:</span><pre style="white-space: pre-wrap;">${text}</pre>`;
    chatbox.appendChild(div);
    chatbox.scrollTop = chatbox.scrollHeight;
}

function removeLastMessage() {
    const messages = chatbox.querySelectorAll(".message");
    if (messages.length > 0 && messages[messages.length - 1].classList.contains("temp")) {
        messages[messages.length - 1].remove();
    }
}
