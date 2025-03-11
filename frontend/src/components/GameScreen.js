// components/GameScreen.js
import React from "react";

const GameScreen = ({ puzzle, gameState, onNext, userInput }) => {
  return (
    <div className="game-screen">
      <div className="puzzle-area">
        <h2 className="puzzle-title">
          ({puzzle.pinyin}) – "{puzzle.meaning}"
        </h2>

        <div className="puzzle-prompt">
          <p className="hint">
            <strong>Hint:</strong> {puzzle.hint}
          </p>

          {/* Placeholder for images */}
          {puzzle.imageUrls && (
            <div className="image-container">
              {puzzle.imageUrls.map((url, index) => (
                <img
                  key={index}
                  src={url}
                  alt={`Hint ${index + 1}`}
                  className="hint-image"
                />
              ))}
            </div>
          )}
        </div>

        <div className="user-input-area">
          <h3>Place the correct radical tiles on the board</h3>
          <div className="radical-display">
            <div className="radical left-radical">
              <p>{userInput ? userInput.charAt(0) : "?"}</p>
            </div>
            <div className="radical-plus">+</div>
            <div className="radical right-radical">
              <p>{userInput ? userInput.charAt(1) : "?"}</p>
            </div>
            <div className="radical-equals">=</div>
            <div className="character-result">
              <p>{userInput || "?"}</p>
            </div>
          </div>
        </div>

        <div className={`feedback-area ${gameState}`}>
          {gameState === "correct" && (
            <div className="correct-feedback">
              <h3>Correct! Great job! 👏</h3>
              <p>You formed the character {puzzle.character}!</p>
              <button onClick={onNext} className="next-button">
                Next Puzzle
              </button>
            </div>
          )}

          {gameState === "incorrect" && (
            <div className="incorrect-feedback">
              <h3>Try one more time!</h3>
              <p>
                That's not quite right. Check your radical tiles and try again.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default GameScreen;
