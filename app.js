const chatContainer = document.getElementById('chat-container');
const userInput = document.getElementById('user-input');
const messageForm = document.getElementById('messageForm');

messageForm.addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the default form submission behavior
    
    const message = userInput.value.trim();
    if (message !== '') {
        appendMessage('user', message);
        userInput.value = '';

        // Send message to Flask app
        fetch('http://127.0.0.1:5000/webhook', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json' // Specify the content type
            },
            body: JSON.stringify({ message }) // Convert message to JSON format
        })
        .then(response => response.json())
        .then(data => {
            // Process Rasa response
            const rasaResponse = data[0].text;
            appendMessage('bot', rasaResponse);
        })
        .catch(error => console.error('Error:', error));
    }
});

function appendMessage(sender, message) {
    const messageElement = document.createElement('div');
    messageElement.classList.add(sender);
    messageElement.innerText = message;
    chatContainer.appendChild(messageElement);
}
