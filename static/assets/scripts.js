function executeCanvasCode(code) {
    try {
        const canvas = document.getElementById('myCanvas');
        const ctx = canvas.getContext('2d');
        ctx.clearRect(0, 0, canvas.width, canvas.height); // Clear the canvas
        eval(code); // Executes the JavaScript code to modify the canvas.
    } catch (err) {
        console.error("Error executing canvas code:", err);
        console.log("Executing canvas code:", code); // Log the code
    }
}

function sendMessage() {
    let message = document.getElementById('inputBox').value;
    if (message.trim() === '') return;

    const userMessage = document.createElement('p');
    userMessage.className = 'user animate__animated animate__bounceIn';
    userMessage.textContent = message;
    document.getElementById('chatbox').appendChild(userMessage);

    fetch('/send_message', {
        method: 'POST',
        body: new URLSearchParams({ 'user_input': message }),
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    })
    .then(response => response.json())
    .then(data => {
        const botMessage = document.createElement('p');
        botMessage.className = 'bot animate__animated animate__bounceIn';
        botMessage.textContent = data.response;
        document.getElementById('chatbox').appendChild(botMessage);

        // Extract and execute JavaScript code if it exists in the bot's response
        const codeMatch = data.response.match(/```([\s\S]*?)```/);
        if (codeMatch && codeMatch[1]) {
            console.log("Extracted canvas code:", codeMatch[1].trim());
            executeCanvasCode(codeMatch[1].trim());
        }

        document.getElementById('inputBox').value = '';
        document.getElementById('chatbox').scrollTop = document.getElementById('chatbox').scrollHeight;

        // Check if the chat box is at the bottom before scrolling
        const chatbox = document.getElementById('chatbox');
        if (chatbox.scrollHeight - chatbox.scrollTop === chatbox.clientHeight) {
        chatbox.scrollTop = chatbox.scrollHeight;
        }

    });
}

document.getElementById('inputBox').addEventListener('keydown', function(e) {
    if (e.key === 'Enter') {
        console.log("Enter key pressed");
        sendMessage();
    }
});
