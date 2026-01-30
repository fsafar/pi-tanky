#!/usr/bin/env python3
"""
Pi-Tanky Web Server
Flask + SocketIO server for controlling Pi-Tanky via web interface
"""

import logging
import sys
from flask import Flask, send_from_directory
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from motor_control import MotorController

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/fadi/pi-tanky/tanky.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('WebServer')

# Initialize Flask app
app = Flask(__name__, static_folder='web/build', static_url_path='')
CORS(app)
app.config['SECRET_KEY'] = 'pi-tanky-secret-change-this-in-production'

# Initialize SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

# Global motor controller instance
motor_controller = None
current_speed = 50


@app.route('/')
def serve_react():
    """Serve React app"""
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/health')
def health():
    """Health check endpoint"""
    return {'status': 'ok', 'speed': current_speed}


@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    global motor_controller
    
    if motor_controller is None:
        try:
            motor_controller = MotorController()
            logger.info("Motor controller initialized for web client")
        except Exception as e:
            logger.error(f"Failed to initialize motor controller: {e}")
            emit('error', {'message': 'Failed to initialize motor controller'})
            return
    
    logger.info("Client connected")
    emit('status', {'connected': True, 'speed': current_speed})


@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection - stop motors for safety"""
    logger.info("Client disconnected - stopping motors")
    if motor_controller:
        motor_controller.stop()


@socketio.on('control')
def handle_control(data):
    """
    Handle motor control commands
    
    Expected data format:
    {
        'action': 'forward' | 'backward' | 'left' | 'right' | 'stop',
        'speed': 0-100 (optional, uses current_speed if not provided)
    }
    """
    global current_speed
    
    if not motor_controller:
        emit('error', {'message': 'Motor controller not initialized'})
        return
    
    action = data.get('action')
    speed = data.get('speed', current_speed)
    
    # Clamp speed to valid range
    speed = max(0, min(100, speed))
    
    try:
        if action == 'forward':
            motor_controller.move_forward(speed)
        elif action == 'backward':
            motor_controller.move_backward(speed)
        elif action == 'left':
            motor_controller.turn_left(speed)
        elif action == 'right':
            motor_controller.turn_right(speed)
        elif action == 'stop':
            motor_controller.stop()
        else:
            logger.warning(f"Unknown action: {action}")
            emit('error', {'message': f'Unknown action: {action}'})
            return
        
        # Send acknowledgment
        emit('status', {'action': action, 'speed': speed})
        
    except Exception as e:
        logger.error(f"Error executing control command: {e}")
        emit('error', {'message': str(e)})


@socketio.on('set_speed')
def handle_set_speed(data):
    """Update global speed setting"""
    global current_speed
    
    speed = data.get('speed', 50)
    current_speed = max(0, min(100, speed))
    
    logger.info(f"Speed set to {current_speed}%")
    emit('status', {'speed': current_speed})


@socketio.on('emergency_stop')
def handle_emergency_stop():
    """Emergency stop - immediately halt all motors"""
    logger.warning("EMERGENCY STOP triggered")
    if motor_controller:
        motor_controller.stop()
    emit('status', {'action': 'emergency_stop', 'speed': 0})


def cleanup():
    """Cleanup function called on shutdown"""
    global motor_controller
    logger.info("Shutting down web server")
    if motor_controller:
        motor_controller.cleanup()
        motor_controller = None


if __name__ == '__main__':
    import atexit
    atexit.register(cleanup)
    
    logger.info("="*50)
    logger.info("Starting Pi-Tanky Web Server")
    logger.info("Access at: http://pi5.local:5000")
    logger.info("="*50)
    
    try:
        # Run server on all interfaces, port 5000
        socketio.run(app, host='0.0.0.0', port=5000, debug=False, allow_unsafe_werkzeug=True)
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received")
    finally:
        cleanup()
