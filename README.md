# Chinese Character Learning System
A tactile-based interactive system for learning Chinese characters that combines hardware sensors with a responsive web application.

## Overview
This project creates an immersive learning experience for Chinese characters by integrating physical touch-sensitive radical tiles with a digital interface. Users can trace radicals on custom-designed tiles, and the system provides real-time feedback and learning guidance.

## Features
Touch-sensitive radical tiles with conductive traces
Real-time character recognition and feedback
Seamless communication between hardware and software components

## Technologies Used
- Hardware: Arduino Mega2560, custom PCB design, conductive materials
- Backend: Python, Flask, PySerial, Flask-SocketIO
- Frontend: React.js, JavaScript, HTML/CSS, WebSocket API
- Communication: Serial communication, WebSockets
  
## To run the app
`cd frontend --> npm start`

`cd backend --> python websocket_server.py`
