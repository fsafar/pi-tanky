# Product Requirements Document: Pi-Tanky Robot Vehicle

## 1. Project Overview

**Project Name:** Pi-Tanky  
**Version:** 1.0  
**Date:** January 29, 2026  
**Document Owner:** [Your Name]

### 1.1 Executive Summary
Pi-Tanky is a small, custom-built robotic vehicle featuring tank-style tracked locomotion, powered by a Raspberry Pi 5. The vehicle is designed with dual motors for independent track control, enabling differential steering, and equipped with high-quality video streaming capabilities for remote operation and surveillance applications.

### 1.2 Project Goals
- Build a fully functional tank-style tracked vehicle from scratch
- Implement reliable motor control for differential steering
- Enable real-time video streaming with day/night capability
- Create a platform for future robotics and automation projects

## 2. Hardware Specifications

### 2.1 Compute Platform
- **Model:** Raspberry Pi 5
- **Purpose:** Main control system, motor control, video processing
- **Features:** GPIO pins for motor driver interface, sufficient processing power for video streaming

### 2.2 Motor System
- **Motor Driver:** Pololu Dual G2 High-Power Motor Driver 18v18 for Raspberry Pi
  - Dual channel motor control
  - Up to 18V, 18A per channel
  - Direct GPIO interface with Raspberry Pi
  - Built-in current sensing
  
- **Motors:** 100:1 Metal Gearmotor 37Dx57L mm 12V (Quantity: 2)
  - High torque 100:1 gear ratio
  - 12V nominal operating voltage
  - One motor per track for independent control
  
### 2.3 Power System
- **Battery:** 15 Ah, 12V battery
  - Powers motors and electronics
  - Expected runtime: TBD based on motor load testing
  - Voltage compatible with motor specifications

### 2.4 Vision System
- **Camera:** Arducam HQ Camera for Raspberry Pi
  - Sensor: 12.3MP IMX477
  - CS-Mount lens compatibility
  - Automatic IR-Cut switching for day/night operation
  - CSI interface to Raspberry Pi 5

### 2.5 Chassis
- Tank-style chained tracks (2x)
- Custom frame/chassis (to be designed)
- Component mounting provisions

## 3. Software Requirements

### 3.1 Operating System
- Raspberry Pi OS (64-bit recommended)
- Alternative: Ubuntu Server for Raspberry Pi

### 3.2 Core Software Components
- **Motor Control Library**
  - Python/C++ library for Pololu motor driver
  - PWM control for variable speed
  - Direction control for each motor
  - Emergency stop functionality

- **Video Streaming**
  - libcamera for camera interface
  - WebRTC streaming server (secure, low-latency)
  - H.264 encoding for efficient bandwidth usage
  - Adjustable resolution and frame rate
  - Encrypted stream transmission

- **Web Control Interface**
  - Responsive web-based dashboard (HTML5/CSS/JavaScript)
  - Real-time bidirectional communication (WebSocket over TLS)
  - Gamepad/joystick support via browser API
  - Keyboard control option
  - Touch-friendly mobile interface
  - Network latency monitoring
  - Session management

- **Security & Authentication**
  - HTTPS/TLS encryption for all web traffic
  - User authentication system (username/password)
  - Session token management
  - Rate limiting to prevent abuse
  - CORS configuration for API security
  - Optional: VPN support for enhanced security
  - Optional: Two-factor authentication (2FA)

### 3.3 Communication
- WiFi connectivity for remote control
- HTTPS (port 443) for web interface
- WebSocket Secure (WSS) for real-time control
- Optional: Ethernet for development/debugging
- SSH access for system administration (key-based authentication)
- Firewall configuration to restrict unnecessary ports

## 4. Functional Requirements

### 4.1 Movement Control (Priority: High)
- **FR-1.1:** System shall control left and right tracks independently
- **FR-1.2:** System shall support forward movement (both tracks forward)
- **FR-1.3:** System shall support backward movement (both tracks reverse)
- **FR-1.4:** System shall support pivot turns (tracks in opposite directions)
- **FR-1.5:** System shall support variable speed control (0-100%)
- **FR-1.6:** System shall support gradual turns (differential track speeds)

### 4.2 Video Streaming (Priority: High)
- **FR-2.1:** System shall stream live video feed to remote client
- **FR-2.2:** System shall automatically switch between day/night modes using IR-Cut filter
- **FR-2.3:** Video stream shall have latency < 500ms under normal network conditions
- **FR-2.4:** System shall support minimum 720p resolution at 30fps
- **FR-2.5:** Video quality shall be adjustable to accommodate network bandwidth

### 4.3 Safety Features (Priority: Critical)
- **FR-3.1:** System shall implement emergency stop function
- **FR-3.2:** System shall stop motors if control connection is lost
- **FR-3.3:** System shall monitor battery voltage and alert on low battery
- **FR-3.4:** System shall monitor motor current and prevent overload
- **FR-3.5:** System shall implement controlled startup/shutdown procedures

### 4.4 Remote Control (Priority: High)
- **FR-4.1:** User shall control vehicle remotely via WiFi from any web browser
- **FR-4.2:** Control interface shall display real-time video feed
- **FR-4.3:** Control interface shall display battery status
- **FR-4.4:** Control interface shall display connection status
- **FR-4.5:** Multiple control input methods supported (keyboard, gamepad, touch)
- **FR-4.6:** Web interface shall be accessible from desktop and mobile devices
- **FR-4.7:** Control interface shall work across different browsers (Chrome, Firefox, Safari, Edge)
- **FR-4.8:** User shall receive visual feedback for all control inputs
- **FR-4.9:** Interface shall display network latency in real-time

### 4.5 Security & Access Control (Priority: Critical)
- **FR-5.1:** System shall require user authentication before granting control access
- **FR-5.2:** All web traffic shall be encrypted using HTTPS/TLS
- **FR-5.3:** Control commands shall be transmitted over encrypted WebSocket (WSS)
- **FR-5.4:** System shall implement session timeout after period of inactivity
- **FR-5.5:** System shall log all access attempts (successful and failed)
- **FR-5.6:** System shall allow only one active control session at a time
- **FR-5.7:** System shall provide secure credential storage (hashed passwords)
- **FR-5.8:** Admin shall be able to change credentials remotely
- **FR-5.9:** System shall prevent unauthorized API access via token validation
- **FR-5.10:** System shall implement CSRF protection for web forms

### 4.6 Monitoring & Telemetry (Priority: Medium)
- **FR-6.1:** System shall log motor speeds and directions
- **FR-6.2:** System shall display current draw from motors in web interface
- **FR-6.3:** System shall display CPU temperature and usage in web interface
- **FR-6.4:** System shall track total operating time
- **FR-6.5:** System shall provide diagnostic information for troubleshooting
- **FR-6.6:** Web interface shall display real-time telemetry data
- **FR-6.7:** System shall maintain access logs for security auditing

## 5. Non-Functional Requirements

### 5.1 Performance
- **NFR-1.1:** Motor response time < 100ms from control input
- **NFR-1.2:** System boot time < 60 seconds
- **NFR-1.3:** Video streaming latency < 500ms
- **NFR-1.4:** Control interface response time < 200ms

### 5.2 Reliability
- **NFR-2.1:** System shall operate continuously for minimum 30 minutes
- **NFR-2.2:** WiFi connection shall auto-reconnect on dropout
- **NFR-2.3:** System shall recover gracefully from software errors

### 5.3 Security
- **NFR-3.1:** All passwords shall be hashed using bcrypt or similar
- **NFR-3.2:** TLS certificates shall use minimum 2048-bit RSA or equivalent
- **NFR-3.3:** Session tokens shall expire after 30 minutes of inactivity
- **NFR-3.4:** Failed login attempts shall be limited (max 5 per 15 minutes)
- **NFR-3.5:** System shall not expose sensitive information in error messages

### 5.4 Usability
- **NFR-4.1:** Control interface shall be intuitive for first-time users
- **NFR-4.2:** Emergency stop shall be easily accessible in web UI
- **NFR-4.3:** System status shall be clearly visible
- **NFR-4.4:** Web interface shall load within 3 seconds on standard broadband
- **NFR-4.5:** Interface shall be responsive across screen sizes (320px to 4K)

### 5.5 Maintainability
- **NFR-5.1:** Code shall be modular and well-documented
- **NFR-5.2:** Hardware components shall be easily accessible for maintenance
- **NFR-5.3:** System shall support remote software updates via web interface
- **NFR-5.4:** Configuration changes shall not require system reboot when possible

### 5.6 Power Efficiency
- **NFR-6.1:** System shall optimize power consumption for extended runtime
- **NFR-6.2:** Battery should provide minimum 1 hour of moderate operation

## 6. Use Cases

### 6.1 Primary Use Cases

**UC-1: Remote Exploration**
- User starts the vehicle and control interface
- User navigates vehicle to explore remote/inaccessible areas
- Real-time video feedback guides navigation
- User returns vehicle to starting position

**UC-2: Surveillance/Monitoring**
- User deploys vehicle to monitoring location
- Vehicle streams video while stationary or patrolling
- IR-Cut switching enables day/night operation
- User monitors feed from remote location

**UC-3: Secure Remote Access**
- User opens web browser on laptop/mobile device
- User navigates to vehicle's HTTPS address
- User authenticates with username and password
- System establishes secure encrypted connection
- User controls vehicle and views live video feed
- User logs out, session is terminated securely

**UC-4: Robotics Platform Development**
- Developer uses Pi-Tanky as testbed for algorithms
- Autonomous navigation algorithms tested
- Computer vision applications deployed
- Sensor integration and testing

### 6.2 Edge Cases
- Loss of WiFi connection during operation
- Battery depletion during operation
- Obstacle causing motor stall
- Extreme lighting conditions affecting video quality

## 7. System Architecture

### 7.1 Hardware Architecture
```
[Battery 12V 15Ah]
    |
    +-- [Motor Driver] -- [Motor Left] -- [Track Left]
    |                  \
    |                   -- [Motor Right] -- [Track Right]
    |
    +-- [Raspberry Pi 5]
             |
             +-- [Arducam HQ Camera]
             +-- [WiFi Module]
```

### 7.2 Software Architecture (Proposed)
```
┌─────────────────────────────────────────┐
│         Web Interface (Client)          │
│  HTML5 + JavaScript + WebSocket Client  │
└─────────────────┬───────────────────────┘
                  │ HTTPS/WSS (Encrypted)
┌─────────────────┴───────────────────────┐
│        Security Layer (Server)          │
│  Authentication, TLS, Session Mgmt      │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────┴───────────────────────┐
│       Interface Layer (Server)          │
│  Web Server, WebSocket, API Endpoints   │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────┴───────────────────────┐
│      Communication Layer (Server)       │
│   Network Handling, Video Streaming     │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────┴───────────────────────┐
│      Application Layer (Server)         │
│  Navigation Logic, Safety Monitors      │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────┴───────────────────────┐
│         Control Layer (Server)          │
│     Motor Control, PWM Generation       │
└─────────────────────────────────────────┘
```

**Technology Stack (Proposed):**
- **Backend:** Python (Flask/FastAPI) or Node.js (Express)
- **WebSocket:** Socket.IO or native WebSocket with SSL
- **Video:** WebRTC or GStreamer with encryption
- **Frontend:** Vanilla JavaScript or React/Vue.js
- **Security:** Let's Encrypt for SSL, JWT for sessions
- **Database:** SQLite for user credentials and logs

## 8. Development Phases

### Phase 1: Hardware Assembly & Testing (Week 1-2)
- Assemble chassis and tracks
- Mount motors and motor driver
- Connect power system
- Verify motor operation with basic test code

### Phase 2: Motor Control Development (Week 2-3)
- Implement motor driver interface
- Create motor control library
- Test differential steering
- Implement safety features

### Phase 3: Camera Integration (Week 3-4)
- Set up camera hardware
- Configure libcamera
- Implement video streaming
- Test IR-Cut switching

### Phase 4: Web Interface Development (Week 4-5)
- Set up web server (Flask/FastAPI/Express)
- Create responsive HTML/CSS/JavaScript interface
- Implement WebSocket for real-time control
- Integrate video display in web UI
- Add telemetry display dashboard
- Test across multiple browsers and devices

### Phase 5: Security Implementation (Week 5-6)
- Generate/obtain SSL/TLS certificates
- Implement HTTPS for web server
- Add user authentication system
- Implement session management
- Add WebSocket encryption (WSS)
- Configure firewall rules
- Implement rate limiting
- Add access logging
- Security testing and penetration testing

### Phase 6: Testing & Refinement (Week 6-7)
- Field testing
- Performance optimization
- Bug fixes
- Documentation

### Phase 7: Advanced Features (Future)
- Autonomous navigation
- Obstacle detection
- GPS waypoint navigation
- Additional sensors

## 9. Success Metrics

### 9.1 Technical Metrics
- Vehicle successfully responds to all control inputs
- Video stream maintains < 500ms latency
- Battery life > 60 minutes of operation
- All safety features function correctly
- Zero critical failures during testing
- All web traffic encrypted (100% HTTPS/WSS)
- Authentication system prevents unauthorized access
- Web interface loads within 3 seconds

### 9.2 User Experience Metrics
- Control interface is usable without documentation
- Emergency stop accessible within 1 second
- Video quality sufficient for navigation
- Web interface works on mobile and desktop browsers
- Login process completed in < 10 seconds

### 9.3 Security Metrics
- Zero unauthorized access attempts successful
- All passwords properly hashed in storage
- SSL/TLS certificate valid and properly configured
- No sensitive data exposed in logs or error messages
- Session timeout functions correctly

## 10. Risks & Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Motor driver overheating | High | Medium | Add heatsinks, monitor temperature, current limiting |
| WiFi range limitation | Medium | High | Use external antenna, WiFi extender, plan operations within range |
| Battery insufficient runtime | Medium | Medium | Optimize power usage, consider larger battery, implement power saving modes |
| Video streaming lag | Medium | Medium | Optimize encoding, reduce resolution/framerate options, buffer management |
| Mechanical stress on tracks | High | Medium | Robust chassis design, quality tracks, avoid excessive loads |
| Software crashes | Medium | Low | Watchdog timer, error handling, automated restart |
| Component compatibility issues | High | Low | Verify specifications before assembly, test incrementally |
| Unauthorized access to controls | Critical | Medium | Strong authentication, HTTPS/TLS, rate limiting, access logging |
| Man-in-the-middle attacks | High | Low | TLS encryption, certificate validation, secure WebSocket |
| Credential theft | High | Medium | Password hashing, session timeout, optional 2FA |
| DDoS/resource exhaustion | Medium | Low | Rate limiting, firewall rules, connection limits |

## 11. Constraints & Assumptions

### 11.1 Constraints
- Budget limitations for additional components
- Motor driver limited to 12-18V operation
- WiFi range limitations
- Battery capacity fixed at 15Ah
- Processing power limited by Raspberry Pi 5

### 11.2 Assumptions
- Suitable WiFi network available for operation
- Users access system from trusted networks or VPN
- Flat to moderately rough terrain
- Indoor/outdoor operation in normal weather
- User has basic technical knowledge
- Standard development tools available
- Modern web browser with WebSocket support
- Users understand basic security practices (password management)

## 12. Future Enhancements

### 12.1 Short-term (v1.1-v1.2)
- Native mobile app (iOS/Android)
- Two-factor authentication (2FA)
- Battery percentage estimation algorithm
- Recording capability for video with cloud storage
- Multiple video quality presets
- Multi-user access with role-based permissions
- VPN integration for enhanced security
- Remote configuration management via web UI

### 12.2 Long-term (v2.0+)
- Autonomous navigation with obstacle avoidance
- GPS integration for outdoor navigation
- Additional sensors (ultrasonic, IMU, LIDAR)
- Solar charging capability
- Multi-robot coordination
- Machine learning integration
- Robotic arm attachment point

## 13. Documentation Requirements

- Hardware assembly guide
- Software installation guide with security setup
- Web interface user guide
- API documentation (RESTful endpoints and WebSocket protocol)
- Security configuration guide (SSL setup, firewall configuration)
- User manual for remote access
- Troubleshooting guide
- Safety guidelines
- Network architecture diagram
- Security best practices document

## 14. Testing Requirements

### 14.1 Unit Testing
- Motor driver interface functions
- Camera interface functions
- Safety feature triggers

### 14.2 Integration Testing
- Motor control with video streaming
- Network connectivity with control
- Power system under load

### 14.3 System Testing
- End-to-end operation scenarios
- Stress testing (extended operation)
- Range testing (WiFi limits)
- Battery life testing

### 14.4 Security Testing
- Penetration testing for web interface
- Authentication bypass attempts (should fail)
- Session hijacking attempts (should fail)
- SQL injection testing (if database used)
- XSS and CSRF vulnerability testing
- SSL/TLS configuration validation
- Password encryption verification

### 14.5 Acceptance Testing
- All functional requirements met
- Performance benchmarks achieved
- User acceptance of control interface
- Security requirements validated
- Remote access from multiple devices confirmed

## 15. Regulatory & Safety Considerations

- Ensure wireless operation complies with local regulations
- Data protection and privacy compliance (GDPR if applicable)
- Secure storage of user credentials
- Network security best practices
- Battery charging safety (use appropriate charger)
- Motor current limits to prevent damage
- Heat management for electronics
- Emergency shutdown accessible
- Operating guidelines for safe use
- Disclosure of security vulnerabilities and patch management

## Appendices

### Appendix A: Component Datasheets
- [Link to Raspberry Pi 5 documentation]
- [Link to Pololu motor driver datasheet]
- [Link to motor specifications]
- [Link to Arducam documentation]

### Appendix B: Pinout Configuration
To be documented during implementation

### Appendix C: Software Dependencies
To be documented during development

---

**Document Revision History**

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-01-29 | [Your Name] | Initial PRD creation |
