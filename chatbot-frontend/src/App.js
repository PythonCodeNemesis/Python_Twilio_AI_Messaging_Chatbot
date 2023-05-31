import React, { useState } from "react";
import "./App.css";

function App() {
  const [userInput, setUserInput] = useState("");
  const [chatHistory, setChatHistory] = useState([]);

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

    // Update the chat history with the user's message and bot's response
    setChatHistory((prevHistory) => [
      ...prevHistory,
      { sender: "user", message: userInput },
      { sender: "bot", message: data.message },
    ]);

    // Clear the input field
    setUserInput("");
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
        {chatHistory.map((message, index) => (
          <div
            className={`message-container ${
              message.sender === "user" ? "user-message" : "bot-message"
            }`}
            key={index}
          >
            <p>{message.message}</p>
          </div>
        ))}
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
