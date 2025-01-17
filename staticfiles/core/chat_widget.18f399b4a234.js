(function() {
    var threadID = null;
    var backendURL = "https://3280a653-bce3-4755-b076-9d26aea1d67b-00-1yju02xjv8g7k.spock.replit.dev";
    var typingIndicatorInterval = null;
    var apiKey = "security_key_clubcito"; // Añadir la clave API

    // Añadir meta tag para prevenir el zoom en dispositivos móviles
    var metaViewport = document.createElement('meta');
    metaViewport.name = "viewport";
    metaViewport.content = "width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no";
    document.head.appendChild(metaViewport);

    // Crear burbuja flotante
    var chatBubble = document.createElement('div');
    chatBubble.className = 'chat-bubble';
    chatBubble.innerHTML = '<img src="static/core/images/Clubcito.png" alt="Chat">';
    document.body.appendChild(chatBubble);

    // Crear contenedor de chat
    var chatContainer = document.createElement('div');
    chatContainer.className = 'chat-container';
    chatContainer.innerHTML = `
  <div class="chat-content-vertical">
      <div class="chat-header" style="height: 20px;">
          <button class="chat-close" id="chatClose">x</button>
      </div>
      <div class="chat-bot-info">
          <img src="static/core/images/Clubcito.png" alt="Yumbot" class="chat-bot-icon">
          <span class="chat-bot-title"> Hola soy Clubcito</span>
          <span class="chat-bot-subtitle">Asistente IA Soporte al Cliente</span>
      </div>
      <div class="chat-messages" id="chatMessages"></div>
      <div class="chat-input-container">
          <button id="startConversationButton">Iniciar conversación</button>
          <input type="text" id="chatInput" placeholder="Escribe un mensaje..." style="display: none;">
          <button id="sendButton" style="display: none;">Enviar</button>
      </div>
  </div>
`;
    document.body.appendChild(chatContainer);

    var chatMessages = document.getElementById('chatMessages');
    var chatInput = document.getElementById('chatInput');
    var sendButton = document.getElementById('sendButton');
    var startConversationButton = document.getElementById('startConversationButton');
    var chatClose = document.getElementById('chatClose');

    // Mostrar/ocultar chat
    chatBubble.addEventListener('click', function() {
        chatContainer.style.display = 'flex';
        chatBubble.style.display = 'none';
        if (!threadID) {
            showStartConversationButton();
        } else {
            resetChat();
        }
    });

    chatClose.addEventListener('click', function() {
        chatContainer.style.display = 'none';
        chatBubble.style.display = 'flex';
        threadID = null;  // Resetear threadID
        chatMessages.innerHTML = '';  // Limpiar mensajes del chat
        showStartConversationButton();
    });

    startConversationButton.addEventListener('click', startConversation);

    // Enviar mensaje
    sendButton.addEventListener('click', sendMessage);
    chatInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') sendMessage();
    });

    function showStartConversationButton() {
        startConversationButton.style.display = 'block';
        chatInput.style.display = 'none';
        sendButton.style.display = 'none';
    }

    function showChatInput() {
        startConversationButton.style.display = 'none';
        chatInput.style.display = 'block';
        sendButton.style.display = 'block';
    }

    function startConversation() {
        //console.log("Iniciando conversación...");
        startConversationButton.disabled = true; // Deshabilitar el botón
        startConversationButton.classList.add('button-disabled'); // Añadir clase de deshabilitado

        // Añadir efecto de carga
        startConversationButton.innerHTML = 'Iniciando...';

        fetch(`${backendURL}/start?platform=Web`, {
            method: 'GET',
            headers: {
                'X-API-KEY': apiKey // Añadir la clave API a los encabezados
            }
        })
            .then(response => {
                //console.log("Respuesta de /start:", response);
                if (!response.ok) throw new Error("Error al obtener el thread_id");
                return response.json();
            })
            .then(data => {
                //console.log("Datos obtenidos de /start:", data);
                threadID = data.thread_id;
                // Mostrar los mensajes de manera separada con pequeños retrasos
            addMessageToChat('Asistente', 'Hola 😊');
            setTimeout(() => {
                addMessageToChat('Asistente', '¿En qué te puedo ayudar?');
            }, 1000);
            setTimeout(() => {
                addMessageToChat('Asistente', '¿Quieres saber cómo unirte al Club?');
            }, 2000);
            setTimeout(() => {
                addMessageToChat('Asistente', '¿Buscas algún negocio en particular?');
            }, 3000);
            
                showChatInput();
                setTimeout(() => {
                    startConversationButton.disabled = false; // Habilitar el botón después de 3 segundos
                    startConversationButton.classList.remove('button-disabled'); // Remover clase de deshabilitado
                    startConversationButton.innerHTML = 'Iniciar conversación'; // Restablecer texto del botón
                }, 3000);
            })
            .catch(error => {
                console.error('Error al iniciar la conversación:', error);
                addMessageToChat('Error', 'No se pudo iniciar la conversación.');
                startConversationButton.disabled = false; // Habilitar el botón en caso de error
                startConversationButton.classList.remove('button-disabled'); // Remover clase de deshabilitado
                startConversationButton.innerHTML = 'Iniciar conversación'; // Restablecer texto del botón
            });
    }

    function resetChat() {
        // Reiniciar el chat al mensaje predeterminado de bienvenida
        chatMessages.innerHTML = '';
        addMessageToChat('Asistente', '¿En qué te puedo ayudar? 😊');
    }

    function sendMessage() {
        var message = chatInput.value.trim();
        if (!message || !threadID) return;

        addMessageToChat('Tú', message);

        chatInput.value = '';

        startTypingIndicator();

        console.log("Enviando mensaje al backend:", message);
        fetch(`${backendURL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-API-KEY': apiKey // Añadir la clave API a los encabezados
            },
            body: JSON.stringify({
                thread_id: threadID,
                message: message
            })
        })
            .then(response => {
                console.log("Respuesta de /chat:", response);
                if (!response.ok) throw new Error("Error al enviar el mensaje");
                return response.json();
            })
            .then(data => {
                console.log("Datos obtenidos de /chat:", data);
                stopTypingIndicator();
                addMessageToChat('Asistente', data.response);
            })
            .catch(error => {
                console.error('Error al obtener respuesta:', error);
                stopTypingIndicator();
                addMessageToChat('Error', 'No se pudo obtener respuesta.');
            });
    }

    function startTypingIndicator() {
        var typingIndicator = document.createElement('div');
        typingIndicator.className = 'message-bubble assistant-message typing-indicator';

        // Agregar imagen para el asistente
        var img = document.createElement('img');
        img.src = 'static/core/images/Clubcito.png';
        img.alt = 'Asistente';
        img.className = 'assistant-icon';
        typingIndicator.appendChild(img);

        var typingText = document.createElement('div');
        typingText.className = 'message-text';
        typingText.innerHTML = 'Escribiendo...';
        typingIndicator.appendChild(typingText);

        chatMessages.appendChild(typingIndicator);
        chatMessages.scrollTop = chatMessages.scrollHeight;

        typingIndicatorInterval = setInterval(() => {
            if (typingText.innerHTML.endsWith('...')) {
                typingText.innerHTML = 'Escribiendo';
            } else {
                typingText.innerHTML += '.';
            }
        }, 500);
    }

    function stopTypingIndicator() {
        clearInterval(typingIndicatorInterval);
        typingIndicatorInterval = null;

        var typingIndicators = chatMessages.querySelectorAll('.typing-indicator');
        typingIndicators.forEach(function(indicator) {
            indicator.remove();
        });
    }

    function addMessageToChat(sender, message) {
        var typingIndicator = chatMessages.querySelector('.typing-indicator');
        if (typingIndicator) typingIndicator.remove();

        var messageWrapper = document.createElement('div');
        messageWrapper.className = sender === 'Tú' ? 'message-wrapper user-message' : 'message-wrapper assistant-message';

        var messageElement = document.createElement('div');
        messageElement.className = 'message-bubble';

        if (sender !== 'Tú') {
            // Agregar imagen para el asistente
            var img = document.createElement('img');
            img.src = 'static/core/images/Clubcito.png';
            img.alt = 'Asistente';
            img.className = 'assistant-icon';
            messageElement.appendChild(img);
        }

        var messageText = document.createElement('div');
        messageText.className = 'message-text';
        messageText.innerHTML = `${marked.parse(message)}`;
        messageElement.appendChild(messageText);

        messageWrapper.appendChild(messageElement);
        chatMessages.appendChild(messageWrapper);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
})();
