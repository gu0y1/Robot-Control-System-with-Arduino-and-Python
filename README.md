# Robot Control System with Arduino and Python

This repository contains the code for a robot control system that uses Arduino for hardware interfacing and Python for data processing and user interface. The system features real-time data communication between Arduino and Python, utilizing an ultrasonic sensor for distance measurement and motor encoders for speed and acceleration calculations.

## Fundamental Concepts

- **Arduino Programming**: Utilized for reading sensor data and controlling motors.
- **Serial Communication**: Enables communication between Arduino and Python via serial ports.
- **Ultrasonic Sensor (HC-SR04)**: Measures distance by emitting and receiving ultrasonic waves.
- **Motor Encoders**: Calculate the robot's speed and acceleration.
- **Python with Rich Library**: Enhances user experience with a dynamic command-line interface and real-time data visualization.
- **Flask Web Framework**: Facilitates remote control via HTTP requests.

## Hardware Requirements

- Arduino Board (Uno, Mega, etc.)
- HC-SR04 Ultrasonic Sensor
- Motors with Encoders
- Jumper Wires and Breadboard
- Power Supply for Arduino and Motors

## Software Requirements

- Arduino IDE
- Python 3.x
- Libraries: `serial`, `rich`, `keyboard`, `flask`

## Setup and Installation

### Arduino Setup

1. Connect HC-SR04 to Arduino: VCC to 5V, GND to GND, Trig to pin 9, Echo to pin 10.
2. Connect motor encoders to appropriate analog pins (e.g., A0 and A1).
3. Upload the Arduino code from `arduino_code.ino` to your Arduino board.

### Python Environment Setup

1. Ensure Python 3.x is installed on your system.
2. Install required Python libraries: `pip install pyserial rich keyboard flask`.

### Running the Python Script

1. Navigate to the directory containing `robot_control.py`.
2. Execute the script with `python robot_control.py`.
3. The Rich CLI will display real-time data from Arduino.

### Web Interface

- The Flask server runs on `http://localhost:5000`.
- Access this address in a web browser for remote control capabilities.

## Usage

- Use keyboard keys 'w', 'a', 's', 'd' to control the robot through the CLI.
- Utilize the web interface for remote control and to issue commands to the robot.

## Contributing

Contributions to this project are welcome. Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.

---

## Arduino Code Analysis

### Overview

The Arduino code orchestrates the robot's movement, processes commands, measures speed using motor encoders, calculates acceleration, and utilizes an HC-SR04 ultrasonic sensor for distance measurement. It operates in a loop, reading commands from the serial port, executing commands, and sending back the robot's status.

### Hardware Setup

- **Motor Encoders**: Connected to analog pins for speed measurement.
- **HC-SR04 Ultrasonic Sensor**:
  - Trig Pin: Connected to digital pin 9 for triggering ultrasonic pulses.
  - Echo Pin: Connected to digital pin 10 for receiving reflected ultrasonic pulses.
- **Arduino Board**: Any compatible board like Uno or Mega.

### Implementation Details

- **setup()**: Initializes serial communication and sensor pins.
- **loop()**: Checks for incoming serial commands, executes commands, and sends robot status periodically.
- **executeCommand(char command)**: Placeholder for implementing specific movements like forward or turn.
- **calculateSpeed()**: Calculates speed based on encoder value changes, adjusted for time interval and wheel radius.
- **calculateDistance()**: Measures distance using the ultrasonic sensor, taking multiple readings for accuracy.
- **sendResponse()**: Collects and sends data like wheel speed, linear and angular speed, acceleration, and distance in a structured format.

### Usage

1. Upload this code to Arduino.
2. Connect Arduino to a computer.
3. Use a serial communication tool or the provided Python script to control the robot and receive status updates.

### Potential Enhancements

- Implement specific actions in `executeCommand`.
- Improve error handling and robustness in serial communication.
- Integrate additional sensors or actuators as required.

---

## Python Code Analysis

### Overview

The Python script establishes a user interface for controlling the Arduino-based robot and visualizing its telemetry data using the `serial`, `keyboard`, and `rich` libraries.

### Implementation Details

- **Serial Communication**: Establishes a connection with Arduino for command transmission and data reception.
- **Keyboard Interaction**: Listens for key inputs for robot control.
- **Real-time Display**: Creates a live dashboard using the `rich` library to display telemetry data.
- **Progress Bars and Formatting**: Visual representation of parameters like speed and distance.
- **Main Function**: Sets up the console, initializes the dashboard, and starts a data-reading thread.
- **Error Handling**: Includes basic error handling for potential exceptions during runtime.

### Usage

1. Connect Arduino with the uploaded script.
2. Run the Python script, ensuring the correct COM port is set.
3. Control the robot using keyboard inputs and monitor its status on the dashboard.

### Requirements

- Python environment with `serial`, `keyboard`, `rich` libraries.
- An Arduino connected via USB with the appropriate script.

### Enhancements

- Expand control capabilities with additional keyboard commands.
- Enhance error handling and exception management.
- Implement a shutdown command for safe script closure and serial port disconnection.

This Python script effectively complements the Arduino code, providing a user-friendly interface for real-time control and monitoring of the robot.

### Flask Web Interface

In addition to the CLI, the system incorporates a Flask web server, allowing remote control via HTTP requests. This expands the robot's accessibility and control options.

#### Implementation

- **Flask Setup**: The script initializes a Flask app that listens on port 5000.
- **Web Routes**: A simple web interface is available at `http://localhost:5000`, offering a form to send commands to the Arduino.
- **Command Processing**: When a command is submitted via the web interface, it is encoded and sent to the Arduino. The script then waits for a response before updating the web page.

#### Usage

- Access the Flask server via a web browser at `http://localhost:5000`.
- Use the web interface to send commands to the robot.

### Contributions and Licensing

#### Contributing

Contributions to this project are welcome. Please fork the repository and submit a pull request with your changes.

#### License

This project is licensed under the MIT License - see the LICENSE file for details. This open-source license allows for free use, modification, and distribution.

## Final Remarks

The integration of Arduino and Python in this project demonstrates a powerful combination for robotics and automation projects. By leveraging the simplicity of Arduino for hardware interfacing and the versatility of Python for data processing and user interface, this system serves as a valuable learning tool and a robust foundation for further development and customization.
