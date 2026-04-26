import React, { useState } from "react";
import "./App.css";

function App() {
  const [score, setScore] = useState(5);
  const [text, setText] = useState("");
  const [emotion, setEmotion] = useState("");

  const predictEmotion = () => {
    let detected = "Calm";

    if (text.includes("stress") || score <= 3) detected = "Stressed";
    if (text.includes("sad")) detected = "Sad";
    if (text.includes("anxious")) detected = "Anxious";

    setEmotion(detected);
  };

  const getRecommendation = () => {
    switch (emotion) {
      case "Stressed":
        return "Try 5-minute breathing exercise 🧘";
      case "Sad":
        return "Journal your thoughts or call a friend ✍";
      case "Anxious":
        return "Practice grounding (5-4-3-2-1 method)";
      default:
        return "Keep maintaining your positive energy 🌿";
    }
  };

  return (
    <div className="container">
      <h1>Track • Laugh • Heal</h1>

      <div className="card">
        <h2>Daily Check-In</h2>

        <input
          type="range"
          min="1"
          max="10"
          value={score}
          onChange={(e) => setScore(e.target.value)}
        />
        <p>Mood Score: {score}</p>

        <textarea
          placeholder="How are you feeling today?"
          value={text}
          onChange={(e) => setText(e.target.value.toLowerCase())}
        />

        <button onClick={predictEmotion}>Submit</button>
      </div>

      {emotion && (
        <div className="card result">
          <h2>Emotion: {emotion}</h2>
          <p>{getRecommendation()}</p>
        </div>
      )}
    </div>
  );
}

export default App;