document.addEventListener('DOMContentLoaded', function() {
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const chatMessages = document.getElementById('chat-messages');
    const suggestionButtons = document.querySelectorAll('.suggestion-btn');

    // Função para adicionar mensagem ao chat
    function addMessage(message, isUser = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = isUser ? 'message user-message' : 'message bot-message';
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        
        if (isUser) {
            messageContent.innerHTML = `<strong>Você:</strong> ${message}`;
        } else {
            messageContent.innerHTML = `<strong>Bot:</strong> ${message}`;
        }
        
        messageDiv.appendChild(messageContent);
        chatMessages.appendChild(messageDiv);
        
        // Scroll para a última mensagem
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Função para enviar mensagem
    async function sendMessage() {
        const message = userInput.value.trim();
        
        if (!message) return;
        
        // Adiciona mensagem do usuário ao chat
        addMessage(message, true);
        userInput.value = '';
        
        // Mostra indicador de digitação
        const typingIndicator = document.createElement('div');
        typingIndicator.className = 'message bot-message';
        typingIndicator.id = 'typing-indicator';
        typingIndicator.innerHTML = '<div class="message-content"><strong>Bot:</strong> Digitando...</div>';
        chatMessages.appendChild(typingIndicator);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        
        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: message })
            });
            
            const data = await response.json();
            
            // Remove indicador de digitação
            document.getElementById('typing-indicator').remove();
            
            if (data.response) {
                addMessage(data.response);
            } else {
                addMessage('Desculpe, ocorreu um erro. Tente novamente.');
                console.error('Erro:', data.error);
            }
        } catch (error) {
            // Remove indicador de digitação
            document.getElementById('typing-indicator').remove();
            
            addMessage('Erro de conexão. Verifique sua internet e tente novamente.');
            console.error('Erro:', error);
        }
    }

    // Event listeners
    sendButton.addEventListener('click', sendMessage);
    
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
    
    // Botões de sugestão
    suggestionButtons.forEach(button => {
        button.addEventListener('click', function() {
            userInput.value = this.getAttribute('data-question');
            sendMessage();
        });
    });
});