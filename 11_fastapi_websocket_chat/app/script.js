let ws;

document.getElementById("joinBtn").onclick = () => {
    const username = document.getElementById("username").value.trim();
    const room = document.getElementById("room").value.trim() || "general";

    if (!username) {
        alert("Enter a username");
        return;
    }

    // Simulate JWT token (in real app, get it from backend login)
    const token = username + "_token";

    // Show chat UI
    document.getElementById("login").classList.add("hidden");
    document.getElementById("chatUI").classList.remove("hidden");
    document.getElementById("roomName").textContent = room;

    // Connect WebSocket
    ws = new WebSocket(`ws://localhost:8000/ws/chat/?token=${token}&room=${room}`);

    ws.onopen = () => {
        appendMessage("Connected to chat room: " + room);
    };

    ws.onmessage = (event) => {
        appendMessage(event.data);
    };

    ws.onclose = () => {
        appendMessage("Disconnected from chat");
    };
};

document.getElementById("sendBtn").onclick = sendMessage;
document.getElementById("messageInput").addEventListener("keypress", (e) => {
    if (e.key === "Enter") sendMessage();
});

function sendMessage() {
    const input = document.getElementById("messageInput");
    const message = input.value.trim();
    if (message && ws) {
        ws.send(message);
        input.value = "";
    }
}

function appendMessage(msg) {
    const messagesDiv = document.getElementById("messages");
    const p = document.createElement("p");
    p.textContent = msg;
    messagesDiv.appendChild(p);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}
