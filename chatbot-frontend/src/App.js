import React, { useState } from "react";
import cors from "cors";

// const corsOptions = {
//   origin: "http://127.0.0.1:5000/sms", // Update this with the actual backend URL
// };

function App() {
  const [userInput, setUserInput] = useState("");
  const [botResponse, setBotResponse] = useState("");

  const sendMessage = async () => {
    const response = await fetch("http://127.0.0.1:5000/sms", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ Body: userInput }),
    });

    const data = await response.json();

    setBotResponse(data);

    // Log the bot response in the console
    console.log(data);
  };

  return (
    <div>
      <h1>AI Chatbot</h1>
      <div>
        <input
          type="text"
          value={userInput}
          onChange={(e) => setUserInput(e.target.value)}
        />
        <button onClick={sendMessage}>Send</button>
      </div>
      <p>{botResponse}</p>
    </div>
  );
}

// export default cors(corsOptions)(App);
export default App;

// import React, { useState } from "react";

// function App() {
//   const [userInput, setUserInput] = useState("");
//   const [botResponse, setBotResponse] = useState("");

//   const sendMessage = async () => {
//     // Send the user's message to the backend API
//     const response = await fetch("http://127.0.0.1:5000/sms", {
//       method: "POST",
//       headers: {
//         "Content-Type": "application/json",
//       },
//       body: JSON.stringify({ Body: userInput }),
//     });

//     const data = await response.json();

//     // Update the bot's response in the state
//     setBotResponse(data.Body);
//   };

//   return (
//     <div>
//       <h1>AI Chatbot</h1>
//       <div>
//         <input
//           type="text"
//           value={userInput}
//           onChange={(e) => setUserInput(e.target.value)}
//         />
//         <button onClick={sendMessage}>Send</button>
//       </div>
//       <p>{botResponse}</p>
//     </div>
//   );
// }

// export default App;
