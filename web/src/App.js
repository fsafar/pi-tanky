import React, { useState, useEffect, useCallback } from 'react';
import io from 'socket.io-client';
import './App.css';

function App() {
  const [socket, setSocket] = useState(null);
  const [connected, setConnected] = useState(false);
  const [speed, setSpeed] = useState(50);
  const [currentAction, setCurrentAction] = useState('stop');
  const [pressedKeys, setPressedKeys] = useState(new Set());

  // Connect to WebSocket server
  useEffect(() => {
    const serverUrl = process.env.REACT_APP_SERVER_URL || window.location.origin;
    const newSocket = io(serverUrl);

    newSocket.on('connect', () => {
      console.log('Connected to server');
      setConnected(true);
    });

    newSocket.on('disconnect', () => {
      console.log('Disconnected from server');
      setConnected(false);
    });

    newSocket.on('status', (data) => {
      console.log('Status update:', data);
      if (data.speed !== undefined) {
        setSpeed(data.speed);
      }
      if (data.action) {
        setCurrentAction(data.action);
      }
    });

    newSocket.on('error', (data) => {
      console.error('Error from server:', data.message);
      alert(`Error: ${data.message}`);
    });

    setSocket(newSocket);

    return () => newSocket.close();
  }, []);

  // Send control command
  const sendControl = useCallback((action, customSpeed = null) => {
    if (socket && connected) {
      socket.emit('control', {
        action: action,
        speed: customSpeed !== null ? customSpeed : speed
      });
      setCurrentAction(action);
    }
  }, [socket, connected, speed]);

  // Handle speed change
  const handleSpeedChange = (newSpeed) => {
    setSpeed(newSpeed);
    if (socket && connected) {
      socket.emit('set_speed', { speed: newSpeed });
    }
  };

  // Keyboard controls
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (pressedKeys.has(e.key.toLowerCase())) return; // Prevent repeat
      
      setPressedKeys(prev => new Set(prev).add(e.key.toLowerCase()));

      switch(e.key.toLowerCase()) {
        case 'w':
          e.preventDefault();
          sendControl('forward');
          break;
        case 's':
          e.preventDefault();
          sendControl('backward');
          break;
        case 'a':
          e.preventDefault();
          sendControl('left');
          break;
        case 'd':
          e.preventDefault();
          sendControl('right');
          break;
        case ' ':
          e.preventDefault();
          sendControl('stop');
          break;
        case '=':
        case '+':
          e.preventDefault();
          handleSpeedChange(Math.min(100, speed + 20));
          break;
        case '-':
        case '_':
          e.preventDefault();
          handleSpeedChange(Math.max(0, speed - 20));
          break;
        default:
          break;
      }
    };

    const handleKeyUp = (e) => {
      setPressedKeys(prev => {
        const newSet = new Set(prev);
        newSet.delete(e.key.toLowerCase());
        return newSet;
      });

      // Stop motors when releasing movement keys
      if (['w', 's', 'a', 'd'].includes(e.key.toLowerCase())) {
        sendControl('stop');
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    window.addEventListener('keyup', handleKeyUp);

    return () => {
      window.removeEventListener('keydown', handleKeyDown);
      window.removeEventListener('keyup', handleKeyUp);
    };
  }, [sendControl, speed, pressedKeys, handleSpeedChange]);

  // Emergency stop
  const emergencyStop = () => {
    if (socket && connected) {
      socket.emit('emergency_stop');
      setCurrentAction('stop');
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🤖 Pi-Tanky Control</h1>
        <div className={`connection-status ${connected ? 'connected' : 'disconnected'}`}>
          {connected ? '● Connected' : '○ Disconnected'}
        </div>
      </header>

      <main className="App-main">
        <div className="status-panel">
          <div className="status-item">
            <label>Speed:</label>
            <span className="status-value">{speed}%</span>
          </div>
          <div className="status-item">
            <label>Action:</label>
            <span className="status-value">{currentAction.toUpperCase()}</span>
          </div>
        </div>

        <div className="speed-control">
          <label>Speed Control</label>
          <input
            type="range"
            min="0"
            max="100"
            step="10"
            value={speed}
            onChange={(e) => handleSpeedChange(parseInt(e.target.value))}
            disabled={!connected}
          />
          <div className="speed-buttons">
            <button onClick={() => handleSpeedChange(Math.max(0, speed - 20))} disabled={!connected}>
              - 20%
            </button>
            <button onClick={() => handleSpeedChange(Math.min(100, speed + 20))} disabled={!connected}>
              + 20%
            </button>
          </div>
        </div>

        <div className="controls">
          <div className="control-grid">
            <div className="control-row">
              <button
                className="control-btn"
                onMouseDown={() => sendControl('forward')}
                onMouseUp={() => sendControl('stop')}
                onTouchStart={(e) => { e.preventDefault(); sendControl('forward'); }}
                onTouchEnd={(e) => { e.preventDefault(); sendControl('stop'); }}
                disabled={!connected}
              >
                ▲<br/>Forward<br/>(W)
              </button>
            </div>
            <div className="control-row">
              <button
                className="control-btn"
                onMouseDown={() => sendControl('left')}
                onMouseUp={() => sendControl('stop')}
                onTouchStart={(e) => { e.preventDefault(); sendControl('left'); }}
                onTouchEnd={(e) => { e.preventDefault(); sendControl('stop'); }}
                disabled={!connected}
              >
                ◄<br/>Left<br/>(A)
              </button>
              <button
                className="control-btn stop-btn"
                onClick={() => sendControl('stop')}
                disabled={!connected}
              >
                ■<br/>Stop<br/>(SPACE)
              </button>
              <button
                className="control-btn"
                onMouseDown={() => sendControl('right')}
                onMouseUp={() => sendControl('stop')}
                onTouchStart={(e) => { e.preventDefault(); sendControl('right'); }}
                onTouchEnd={(e) => { e.preventDefault(); sendControl('stop'); }}
                disabled={!connected}
              >
                ►<br/>Right<br/>(D)
              </button>
            </div>
            <div className="control-row">
              <button
                className="control-btn"
                onMouseDown={() => sendControl('backward')}
                onMouseUp={() => sendControl('stop')}
                onTouchStart={(e) => { e.preventDefault(); sendControl('backward'); }}
                onTouchEnd={(e) => { e.preventDefault(); sendControl('stop'); }}
                disabled={!connected}
              >
                ▼<br/>Backward<br/>(S)
              </button>
            </div>
          </div>
        </div>

        <button
          className="emergency-stop"
          onClick={emergencyStop}
          disabled={!connected}
        >
          🛑 EMERGENCY STOP
        </button>

        <div className="keyboard-hint">
          <p><strong>Keyboard Controls:</strong></p>
          <p>W/S: Forward/Backward | A/D: Turn Left/Right | SPACE: Stop</p>
          <p>+/-: Increase/Decrease Speed</p>
        </div>
      </main>
    </div>
  );
}

export default App;
