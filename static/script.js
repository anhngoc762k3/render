document.addEventListener("DOMContentLoaded", function () {
    const chatbox = document.getElementById("chatbox");
    const form = document.getElementById("questionForm");
    const input = document.getElementById("question");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        await sendQuestion();
    });

    input.addEventListener("keydown", function (e) {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            form.requestSubmit();
        }
    });

    async function sendQuestion() {
        const question = input.value.trim();
        if (!question) return;

        appendMessage("Bạn", question, "user");

        try {
            const response = await fetch("/ask", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                body: new URLSearchParams({ question })
            });

            const data = await response.json();
            const answer = data.answer || data.error || "Không có phản hồi.";

            appendMessage("Bot", answer, "bot");
        } catch (err) {
            appendMessage("Bot", "Lỗi khi kết nối đến máy chủ.", "bot");
        }

        input.value = "";
        input.focus();
    }

    function appendMessage(sender, text, cls) {
        const div = document.createElement("div");
        div.classList.add("message");
        div.innerHTML = `<span class="${cls}">${sender}:</span><div style="margin-top: 5px;">${text}</div>`;
        chatbox.appendChild(div);
        chatbox.scrollTop = chatbox.scrollHeight;
    }
});
