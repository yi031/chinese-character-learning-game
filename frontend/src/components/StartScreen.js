// components/StartScreen.js
import React from "react";

const StartScreen = ({ onStart }) => {
  return (
    <div className="start-screen">
      <h1>Chinese Radical Puzzle Game</h1>
      <div className="instructions">
        <h2>How to Play</h2>
        <ol>
          <li>Read the puzzle prompt and hint</li>
          <li>Place radical tiles on the electric board</li>
          <li>Combine the correct radicals to form the Chinese character</li>
          <li>The game will tell you if your answer is correct</li>
          <li>Move on to the next puzzle after solving each one</li>
        </ol>
        <p className="tip">
          Tip: Pay attention to the hint for clues about which radicals to use!
        </p>
      </div>
      <button className="start-button" onClick={onStart}>
        Start Game
      </button>
    </div>
  );
};

export default StartScreen;
