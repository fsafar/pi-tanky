#!/usr/bin/env python3
"""
Motor Control Script for Pi-Tanky
Controls the Pololu Dual G2 High-Power Motor Driver for Raspberry Pi
"""

import time
import logging
import sys
try:
    import RPi.GPIO as GPIO
except ImportError:
    print("Warning: RPi.GPIO not available. Running in simulation mode.")
    GPIO = None

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/fadi/pi-tanky/tanky.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('MotorController')

class MotorController:
    """Controls dual motors via Pololu Dual G2 motor driver"""
    
    def __init__(self, m1_pwm=12, m1_dir=24, m1_slp=22, m2_pwm=13, m2_dir=25, m2_slp=23, pwm_freq=1000):
        """
        Initialize motor controller
        
        Pololu Dual G2 18v18 for Raspberry Pi - GPIO Pin Mapping (BCM):
        - Motor 1 (M1): DIR=GPIO24, PWM=GPIO12, SLP=GPIO22, FLT=GPIO5
        - Motor 2 (M2): DIR=GPIO25, PWM=GPIO13, SLP=GPIO23, FLT=GPIO6
        
        Args:
            m1_pwm: GPIO pin for Motor 1 PWM (left track, default: 12)
            m1_dir: GPIO pin for Motor 1 Direction (default: 24)
            m1_slp: GPIO pin for Motor 1 Sleep (inverted, default: 22)
            m2_pwm: GPIO pin for Motor 2 PWM (right track, default: 13)
            m2_dir: GPIO pin for Motor 2 Direction (default: 25)
            m2_slp: GPIO pin for Motor 2 Sleep (inverted, default: 23)
            pwm_freq: PWM frequency in Hz (default: 1000)
        """
        self.m1_pwm_pin = m1_pwm
        self.m1_dir_pin = m1_dir
        self.m1_slp_pin = m1_slp
        self.m2_pwm_pin = m2_pwm
        self.m2_dir_pin = m2_dir
        self.m2_slp_pin = m2_slp
        self.pwm_freq = pwm_freq
        
        if GPIO:
            # Setup GPIO mode
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
            
            # Setup motor 1 pins
            GPIO.setup(self.m1_pwm_pin, GPIO.OUT)
            GPIO.setup(self.m1_dir_pin, GPIO.OUT)
            GPIO.setup(self.m1_slp_pin, GPIO.OUT)
            GPIO.output(self.m1_slp_pin, GPIO.HIGH)  # Wake motor 1 (SLP is inverted: HIGH=awake)
            
            # Setup motor 2 pins
            GPIO.setup(self.m2_pwm_pin, GPIO.OUT)
            GPIO.setup(self.m2_dir_pin, GPIO.OUT)
            GPIO.setup(self.m2_slp_pin, GPIO.OUT)
            GPIO.output(self.m2_slp_pin, GPIO.HIGH)  # Wake motor 2 (SLP is inverted: HIGH=awake)
            
            # Initialize PWM
            self.m1_pwm = GPIO.PWM(self.m1_pwm_pin, self.pwm_freq)
            self.m2_pwm = GPIO.PWM(self.m2_pwm_pin, self.pwm_freq)
            
            # Start PWM at 0% duty cycle
            self.m1_pwm.start(0)
            self.m2_pwm.start(0)
            
            logger.info("Motor controller ready")
        else:
            logger.warning("Simulation mode")
            self.m1_pwm = None
            self.m2_pwm = None
    
    def set_motor_speed(self, motor, speed, direction='forward'):
        """
        Set speed and direction for a single motor
        
        Args:
            motor: 1 for left track, 2 for right track
            speed: Speed from 0 to 100 (percentage)
            direction: 'forward' or 'backward'
        """
        # Clamp speed to valid range
        speed = max(0, min(100, speed))
        
        # According to Pololu G2 specs:
        # DIR=0 (LOW): current flows from MxA to MxB
        # DIR=1 (HIGH): current flows from MxB to MxA
        # Both motors use same DIR logic (wiring/mounting handles the mirroring)
        
        # Both motors: DIR LOW = forward, DIR HIGH = backward
        dir_value = GPIO.LOW if direction == 'forward' else GPIO.HIGH
        
        if motor == 1:
            if GPIO and self.m1_pwm:
                GPIO.output(self.m1_dir_pin, dir_value)
                self.m1_pwm.ChangeDutyCycle(speed)
                logger.debug(f"M1: DIR={'HIGH' if dir_value == GPIO.HIGH else 'LOW'} ({direction}), PWM={speed}%")
            else:
                logger.debug("[SIM] Motor 1 (Left): %s at %d%%", direction, speed)
        elif motor == 2:
            if GPIO and self.m2_pwm:
                GPIO.output(self.m2_dir_pin, dir_value)
                self.m2_pwm.ChangeDutyCycle(speed)
                logger.debug(f"M2: DIR={'HIGH' if dir_value == GPIO.HIGH else 'LOW'} ({direction}), PWM={speed}%")
            else:
                logger.debug("[SIM] Motor 2 (Right): %s at %d%%", direction, speed)
    
    def move_forward(self, speed):
        """
        Move both motors forward at specified speed
        
        Args:
            speed: Speed from 0 to 100 (percentage)
        """
        logger.info("Forward %d%%", speed)
        self.set_motor_speed(1, speed, 'forward')
        self.set_motor_speed(2, speed, 'forward')
    
    def move_backward(self, speed):
        """
        Move both motors backward at specified speed
        
        Args:
            speed: Speed from 0 to 100 (percentage)
        """
        logger.info("Backward %d%%", speed)
        self.set_motor_speed(1, speed, 'backward')
        self.set_motor_speed(2, speed, 'backward')
    
    def turn_left(self, speed):
        """
        Turn left (left track backward, right track forward)
        
        Args:
            speed: Speed from 0 to 100 (percentage)
        """
        logger.info("Turn LEFT %d%%", speed)
        self.set_motor_speed(1, speed, 'backward')
        self.set_motor_speed(2, speed, 'forward')
    
    def turn_right(self, speed):
        """
        Turn right (left track forward, right track backward)
        
        Args:
            speed: Speed from 0 to 100 (percentage)
        """
        logger.info("Turn RIGHT %d%%", speed)
        self.set_motor_speed(1, speed, 'forward')
        self.set_motor_speed(2, speed, 'backward')
    
    def stop(self):
        """Stop both motors"""
        logger.info("STOP")
        self.set_motor_speed(1, 0, 'forward')
        self.set_motor_speed(2, 0, 'forward')
    
    def cleanup(self):
        """Clean up GPIO resources"""
        self.stop()
        if GPIO and self.m1_pwm and self.m2_pwm:
            # Put motors to sleep
            GPIO.output(self.m1_slp_pin, GPIO.LOW)
            GPIO.output(self.m2_slp_pin, GPIO.LOW)
            # Stop PWM
            self.m1_pwm.stop()
            self.m2_pwm.stop()
            GPIO.cleanup()
            logger.info("GPIO cleanup complete")


def main():
    """Main function to test motor control"""
    logger.info("=" * 40)
    logger.info("Pi-Tanky Motor Control Test")
    logger.info("=" * 40)
    
    # Initialize motor controller
    controller = MotorController()
    
    try:
        # Test forward movement at different speeds
        speeds = [30, 50, 75, 100]
        
        for speed in speeds:
            controller.move_forward(speed)
            time.sleep(2)  # Run for 2 seconds
            controller.stop()
            time.sleep(1)  # Pause between tests
        
        logger.info("Test complete")
        
    except KeyboardInterrupt:
        logger.warning("Interrupted by user")
    finally:
        controller.cleanup()


def interactive():
    """Interactive control mode"""
    logger.info("="*40)
    logger.info("Pi-Tanky Interactive Control Mode")
    logger.info("="*40)
    logger.info("Controls:")
    logger.info("  w/s: Forward/Backward")
    logger.info("  a/d: Turn Left/Right")
    logger.info("  =/- (or arrow up/down): Increase/Decrease speed")
    logger.info("  SPACE: Stop")
    logger.info("  q: Quit")
    logger.info("="*40)
    
    controller = MotorController()
    current_speed = 50
    current_action = None  # Track current movement: 'forward', 'backward', 'left', 'right', or None
    
    try:
        import tty
        import termios
        import select
        
        # Get terminal settings
        old_settings = termios.tcgetattr(sys.stdin)
        
        try:
            # Set terminal to raw mode for immediate key detection
            tty.setraw(sys.stdin.fileno())
            
            logger.info("Ready! Current speed: %d%%", current_speed)
            
            while True:
                # Check if key is available
                if select.select([sys.stdin], [], [], 0.1)[0]:
                    key = sys.stdin.read(1)
                    
                    if key == 'q' or key == 'Q':
                        logger.info("Quitting...")
                        break
                    elif key == 'w' or key == 'W':
                        controller.move_forward(current_speed)
                        current_action = 'forward'
                    elif key == 's' or key == 'S':
                        controller.move_backward(current_speed)
                        current_action = 'backward'
                    elif key == 'a' or key == 'A':
                        controller.turn_left(current_speed)
                        current_action = 'left'
                    elif key == 'd' or key == 'D':
                        controller.turn_right(current_speed)
                        current_action = 'right'
                    elif key == ' ':
                        controller.stop()
                        current_action = None
                    elif key == '=' or key == '+':
                        current_speed = min(100, current_speed + 20)
                        logger.info("SPEED: %d%%", current_speed)
                        # Reapply current action at new speed
                        if current_action == 'forward':
                            controller.move_forward(current_speed)
                        elif current_action == 'backward':
                            controller.move_backward(current_speed)
                        elif current_action == 'left':
                            controller.turn_left(current_speed)
                        elif current_action == 'right':
                            controller.turn_right(current_speed)
                    elif key == '-' or key == '_':
                        current_speed = max(0, current_speed - 20)
                        logger.info("SPEED: %d%%", current_speed)
                        # Reapply current action at new speed
                        if current_action == 'forward':
                            controller.move_forward(current_speed)
                        elif current_action == 'backward':
                            controller.move_backward(current_speed)
                        elif current_action == 'left':
                            controller.turn_left(current_speed)
                        elif current_action == 'right':
                            controller.turn_right(current_speed)
                    # Handle arrow keys (escape sequences)
                    elif key == '\x1b':  # ESC
                        next1 = sys.stdin.read(1)
                        if next1 == '[':
                            next2 = sys.stdin.read(1)
                            if next2 == 'A':  # Up arrow
                                current_speed = min(100, current_speed + 20)
                                logger.info("SPEED: %d%%", current_speed)
                                # Reapply current action at new speed
                                if current_action == 'forward':
                                    controller.move_forward(current_speed)
                                elif current_action == 'backward':
                                    controller.move_backward(current_speed)
                                elif current_action == 'left':
                                    controller.turn_left(current_speed)
                                elif current_action == 'right':
                                    controller.turn_right(current_speed)
                            elif next2 == 'B':  # Down arrow
                                current_speed = max(0, current_speed - 20)
                                logger.info("SPEED: %d%%", current_speed)
                                # Reapply current action at new speed
                                if current_action == 'forward':
                                    controller.move_forward(current_speed)
                                elif current_action == 'backward':
                                    controller.move_backward(current_speed)
                                elif current_action == 'left':
                                    controller.turn_left(current_speed)
                                elif current_action == 'right':
                                    controller.turn_right(current_speed)
                    
        finally:
            # Restore terminal settings
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
            
    except ImportError:
        logger.error("Interactive mode requires termios (Linux/Unix only)")
        logger.info("Falling back to simple input mode...")
        simple_interactive(controller, current_speed)
    except KeyboardInterrupt:
        logger.warning("Interrupted by user")
    finally:
        controller.cleanup()


def simple_interactive(controller, speed=50):
    """Simple interactive mode using input() - works on all platforms"""
    logger.info("Simple interactive mode (enter commands)")
    logger.info("Commands: w/s/a/d (movement), +/- (speed), space (stop), q (quit)")
    
    current_speed = speed
    
    while True:
        try:
            cmd = input(f"[Speed: {current_speed}%] > ").strip().lower()
            
            if cmd == 'q':
                break
            elif cmd == 'w':
                controller.move_forward(current_speed)
            elif cmd == 's':
                controller.move_backward(current_speed)
            elif cmd == 'a':
                controller.turn_left(current_speed)
            elif cmd == 'd':
                controller.turn_right(current_speed)
            elif cmd == '' or cmd == 'space':
                controller.stop()
            elif cmd == '+':
                current_speed = min(100, current_speed + 10)
                logger.info("Speed: %d%%", current_speed)
            elif cmd == '-':
                current_speed = max(0, current_speed - 10)
                logger.info("Speed: %d%%", current_speed)
            else:
                logger.warning("Unknown command: %s", cmd)
        except EOFError:
            break


if __name__ == "__main__":
    import sys
    
    # Check for interactive mode flag
    if len(sys.argv) > 1 and sys.argv[1] == '--interactive':
        interactive()
    else:
        main()
