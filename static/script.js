document.getElementById("questionForm").addEventListener("submit", function(event) {
    event.preventDefault();

    const question = document.getElementById("question").value;
    const responseElement = document.getElementById("answerText");

    fetch('/ask', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({
            'question': question
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.answer) {
            responseElement.textContent = data.answer;
        } else if (data.error) {
            responseElement.textContent = "Error: " + data.error;
        }
    })
    .catch(error => {
        responseElement.textContent = "Error: " + error;
    });
});
