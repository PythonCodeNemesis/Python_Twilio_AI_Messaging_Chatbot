import React, { useState } from "react";
import "./App.css";

function App() {
  const [userInput, setUserInput] = useState("");
  const [botResponse, setBotResponse] = useState("");

  const sendMessage = async () => {
    // Send the user's message to the backend API
    const response = await fetch("http://127.0.0.1:5000/sms", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ Body: userInput }),
    });

    const data = await response.json();

    // Update the bot's response in the state
    setBotResponse(data.Body);
  };

  return (
    <div className="chat-container">
      <div className="chat-header">
        <img
          className="chatbot-image"
          src="path/to/your/chatbot-image.png"
          alt="Chatbot"
        />
        <h1>Twilio AI Messenger</h1>
      </div>
      <div className="chat-body">
        <div className="message-container user-message">
          <p>{userInput}</p>
        </div>
        <div className="message-container bot-message">
          <p>{botResponse}</p>
        </div>
      </div>
      <div className="chat-input">
        <input
          type="text"
          value={userInput}
          onChange={(e) => setUserInput(e.target.value)}
          placeholder="Type your message here..."
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
}

export default App;
