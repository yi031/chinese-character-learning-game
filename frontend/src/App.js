// App.js - Main component for the Chinese Radical Game

import React, { useState, useEffect } from 'react';
import './App.css';
import StartScreen from './components/StartScreen';
import GameScreen from './components/GameScreen';
import puzzleData from './data/puzzleData';

function App() {
  const [gameStarted, setGameStarted] = useState(false);
  const [currentPuzzleIndex, setCurrentPuzzleIndex] = useState(0);
  const [currentUserInput, setCurrentUserInput] = useState(null);
  const [gameState, setGameState] = useState('pending'); // pending, correct, incorrect
  
  // Start the game
  const startGame = () => {
    setGameStarted(true);
    setCurrentPuzzleIndex(0);
    setGameState('pending');
  };
  
  // Move to the next puzzle
  const nextPuzzle = () => {
    if (currentPuzzleIndex < puzzleData.length - 1) {
      setCurrentPuzzleIndex(currentPuzzleIndex + 1);
      setGameState('pending');
      setCurrentUserInput(null);
    } else {
      // Game completed
      alert("Congratulations! You've completed all puzzles!");
      setGameStarted(false);
    }
  };
  
  // Process input from the physical board
  const processInput = (input) => {
    setCurrentUserInput(input);
    
    const currentPuzzle = puzzleData[currentPuzzleIndex];
    if (input === currentPuzzle.character) {
      setGameState('correct');
    } else {
      setGameState('incorrect');
    }
  };
  
  // Mock function to simulate receiving data from Python backend
  // This would be replaced with actual WebSocket or API communication
  useEffect(() => {
    // Example of how to connect to backend
    const connectToBackend = () => {
      // Mock implementation - in a real app, this would be a WebSocket or API call
      const mockCheckForInput = setInterval(() => {
        // This is where you'd check for new input from your physical board via Python
        // For demo purposes, we'll just log that we're checking
        console.log("Checking for input from physical board...");
        
        // For testing: randomly simulate a correct answer occasionally
        if (Math.random() < 0.1 && gameState === 'pending' && gameStarted) {
          const correctCharacter = puzzleData[currentPuzzleIndex].character;
          processInput(correctCharacter);
        }
      }, 3000);
      
      return () => clearInterval(mockCheckForInput);
    };
    
    const cleanup = connectToBackend();
    return cleanup;
  }, [gameStarted, currentPuzzleIndex, gameState]);
  
  return (
    <div className="App">
      {!gameStarted ? (
        <StartScreen onStart={startGame} />
      ) : (
        <GameScreen 
          puzzle={puzzleData[currentPuzzleIndex]}
          gameState={gameState}
          onNext={nextPuzzle}
          userInput={currentUserInput}
        />
      )}
    </div>
  );
}

export default App;
