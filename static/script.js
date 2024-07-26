document.addEventListener("DOMContentLoaded", function () {
  const sendButton = document.getElementById("sendButton");
  const userInput = document.getElementById("userInput");
  const chatbox = document.getElementById("chatbox");

  const botName = "Goku"; 

  // Function to send a message
  async function sendMessage() {
    const message = userInput.value;
    if (!message) return;

    // Add user's message to chatbox
    addMessageToChatbox("You", message);
    userInput.value = "";

    // Send the message to the backend
    const response = await fetch("/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message: message }),
    });

    const data = await response.json();
    if (data.response) {
      // Add bot's response to chatbox
      addMessageToChatbox(botName, data.response);
    } else {
      addMessageToChatbox(botName, "Error: Could not get response");
    }
  }

  // Add message to chatbox
  function addMessageToChatbox(sender, message) {
    const messageElement = document.createElement("div");
    messageElement.classList.add("message");
    messageElement.innerHTML = `<strong>${sender}:</strong> ${message}`;
    chatbox.appendChild(messageElement);
    chatbox.scrollTop = chatbox.scrollHeight; // Scroll to the bottom
  }

  // Send message on button click
  sendButton.addEventListener("click", sendMessage);

  // Send message on Enter key press
  userInput.addEventListener("keydown", function (event) {
    if (event.key === "Enter") {
      sendMessage();
    }
  });
});
