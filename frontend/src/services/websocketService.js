// services/websocketService.js

// WebSocket service to connect with the Python backend
class WebSocketService {
  constructor() {
    this.socket = null;
    this.isConnected = false;
    this.listeners = {
      radicalDetected: [],
      characterDetected: [],
      connectionChange: []
    };
  }

  // Connect to the WebSocket server
  connect() {
    if (this.socket && (this.socket.readyState === WebSocket.OPEN || this.socket.readyState === WebSocket.CONNECTING)) {
      console.log('WebSocket is already connected or connecting');
      return;
    }

    this.socket = new WebSocket('ws://localhost:8765');

    this.socket.onopen = () => {
      console.log('WebSocket connection established');
      this.isConnected = true;
      this._notifyListeners('connectionChange', true);
    };

    this.socket.onclose = () => {
      console.log('WebSocket connection closed');
      this.isConnected = false;
      this._notifyListeners('connectionChange', false);
      
      // Try to reconnect after a delay
      setTimeout(() => this.connect(), 3000);
    };

    this.socket.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    this.socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        console.log('Received message:', data);

        // Handle different message types
        switch (data.type) {
          case 'radicalDetected':
            this._notifyListeners('radicalDetected', {
              radical: data.radical,
              leftRadical: data.leftRadical,
              rightRadical: data.rightRadical
            });
            break;
            
          case 'gameState':
            this._notifyListeners('radicalDetected', {
              leftRadical: data.leftRadical,
              rightRadical: data.rightRadical
            });
            
            // If both radicals are present, check if they form a character
            if (data.leftRadical && data.rightRadical) {
              const character = data.character || null;
              if (character) {
                this._notifyListeners('characterDetected', { character });
              }
            }
            break;
            
          default:
            console.log('Unknown message type:', data.type);
        }
      } catch (error) {
        console.error('Error parsing WebSocket message:', error);
      }
    };
  }

  // Send a message to the WebSocket server
  send(message) {
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      this.socket.send(JSON.stringify(message));
    } else {
      console.error('WebSocket is not connected');
    }
  }

  // Reset the game state
  resetGame() {
    this.send({ type: 'reset' });
  }

  // Set a configuration (for testing without physical hardware)
  setConfiguration(config) {
    this.send({ 
      type: 'setConfiguration', 
      config 
    });
  }

  // Register a listener for events
  addListener(event, callback) {
    if (this.listeners[event]) {
      this.listeners[event].push(callback);
    }
  }

  // Remove a listener
  removeListener(event, callback) {
    if (this.listeners[event]) {
      this.listeners[event] = this.listeners[event].filter(cb => cb !== callback);
    }
  }

  // Notify all listeners of an event
  _notifyListeners(event, data) {
    if (this.listeners[event]) {
      this.listeners[event].forEach(callback => callback(data));
    }
  }

  // Disconnect the WebSocket
  disconnect() {
    if (this.socket) {
      this.socket.close();
      this.socket = null;
    }
  }
}

// Create and export a singleton instance
const websocketService = new WebSocketService();
export default websocketService;
