// --- Configuration ---
// Update this URL to point to your FastAPI server
const API_URL = "http://127.0.0.1:8000/chat"; 

// Generate a random thread_id to maintain session memory on the backend
const threadId = "user_" + Math.random().toString(36).substr(2, 9);

// --- DOM Elements ---
const chatContainer = document.getElementById("chatContainer");
const chatHistory = document.getElementById("chatHistory");
const userInput = document.getElementById("userInput");
const typingIndicator = document.getElementById("typingIndicator");

// --- State Management: Toggle Window ---
function toggleChat() {
    chatContainer.classList.toggle("active");
    if (chatContainer.classList.contains("active")) {
        // Auto-focus the input when opened
        setTimeout(() => userInput.focus(), 300);
    }
}

// --- Event Listeners ---
// Listen for 'Enter' key press in the input field
userInput.addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        event.preventDefault();
        sendMessage();
    }
});

// --- UI Functions ---
function appendMessage(sender, text) {
    // 1. Create the main message wrapper
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message", sender); // sender will be 'user' or 'bot'

    // 2. Create the content bubble
    const contentDiv = document.createElement("div");
    contentDiv.classList.add("message-content");
    contentDiv.textContent = text;

    // 3. Create the timestamp
    const timeDiv = document.createElement("div");
    timeDiv.classList.add("timestamp");
    const now = new Date();
    timeDiv.textContent = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    // 4. Assemble and append
    messageDiv.appendChild(contentDiv);
    messageDiv.appendChild(timeDiv);
    chatHistory.appendChild(messageDiv);

    // 5. Auto-scroll to the newest message
    scrollToBottom();
}

function scrollToBottom() {
    chatHistory.scrollTop = chatHistory.scrollHeight;
}

function showTypingIndicator() {
    typingIndicator.style.display = "block";
    scrollToBottom();
}

function hideTypingIndicator() {
    typingIndicator.style.display = "none";
}

// --- Main API Integration Hook ---
async function sendMessage() {
    const text = userInput.value.trim();
    if (!text) return; // Don't send empty messages

    // 1. Instantly show user message and clear input
    appendMessage("user", text);
    userInput.value = "";
    
    // 2. Show typing indicator while we wait for the API
    showTypingIndicator();

    try {
        // 3. Send POST request to FastAPI backend
        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                message: text,
                thread_id: threadId
            })
        });

        // 4. Handle HTTP errors
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        // 5. Parse the JSON response
        const data = await response.json();

        // 6. Hide indicator and show the bot's final reply
        hideTypingIndicator();
        appendMessage("bot", data.reply);

        // Optional: You could also log or use data.category if you want 
        // to show a small tag in the UI about how the message was routed!

    } catch (error) {
        console.error("API Error:", error);
        hideTypingIndicator();
        appendMessage("bot", "I'm sorry, I'm having trouble connecting to the server right now. Please try again later.");
    }
}