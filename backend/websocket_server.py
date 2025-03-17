#!/usr/bin/env python3

# websocket_server.py
# WebSocket server to connect the Python game logic with the React frontend

import asyncio
import json
import websockets
from game import RadicalTileGame, run  # Import the game logic

# Create a game instance
game = RadicalTileGame()

# Store active WebSocket connections
connected_clients = set()

async def handle_client(websocket):
    """Handle a WebSocket connection from the React frontend."""
    # Register the client
    connected_clients.add(websocket)
    try:
        # Send initial game state
        await websocket.send(json.dumps({
            "type": "gameState",
            "leftRadical": game.current_left_radical,
            "rightRadical": game.current_right_radical,
            "lastDetectedConfig": game.last_detected_config
        }))

        asyncio.create_task(run(game))

        # Start sensor monitor
        sensor_task = asyncio.create_task(sensor_monitor())
        
        # Process messages from the client
        async for message in websocket:
            try:
                data = json.loads(message)
                
                # Handle different message types
                if data["type"] == "reset":
                    game.reset()
                    await broadcast_game_state()
                
                elif data["type"] == "setConfiguration":
                    # For manual testing in the UI
                    config = tuple(data["config"])
                    detected_radical = game.process_sensor_input(config)
                    
                    response = {
                        "type": "radicalDetected",
                        "radical": detected_radical,
                        "leftRadical": game.current_left_radical,
                        "rightRadical": game.current_right_radical
                    }
                    
                    # Check for a valid character
                    character = game.check_valid_character()
                    if character:
                        response["character"] = character
                        response["isValid"] = True
                    
                    await websocket.send(json.dumps(response))
                    
            except json.JSONDecodeError:
                print(f"Error: Received invalid JSON: {message}")
                
    except websockets.exceptions.ConnectionClosed:
        print("Client connection closed")
    finally:
        # Unregister the client
        connected_clients.remove(websocket)

async def broadcast_game_state():
    """Broadcast the current game state to all connected clients."""
    if not connected_clients:
        return
    
    message = json.dumps({
        "type": "gameState",
        "leftRadical": game.current_left_radical,
        "rightRadical": game.current_right_radical,
        "lastDetectedConfig": game.last_detected_config
    })
    
    await asyncio.gather(
        *[client.send(message) for client in connected_clients]
    )

async def sensor_monitor():
    """
    Monitor sensor input from the physical board.
    This function would be modified to read from your actual hardware.
    """
    while True:
        # print('sensor monitor')
        # Placeholder for hardware sensor reading logic
        # In a real implementation, this would read from GPIO pins or other hardware interface
        # For example:
        # sensor_values = read_sensors_from_hardware()
        # detected_radical = game.process_sensor_input(sensor_values)
        
        # For demo, we're just waiting without actual sensor reading
        # await asyncio.sleep(0.1)
        
        # After actual sensor reading, you would broadcast the update
        await broadcast_game_state()
        await asyncio.sleep(0.1)

async def main():
    """Start the WebSocket server and sensor monitoring."""
    # Start WebSocket server
    async with websockets.serve(handle_client, "localhost", 8765) as server:

        
        print("WebSocket server started on ws://localhost:8765")
        
        # Keep the server running
        # await asyncio.Future()  # Run forever

        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
