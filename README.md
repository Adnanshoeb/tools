# asteriskcallgenerator

**AMI Event Monitor**
This script monitors events from an Asterisk Manager Interface (AMI) and logs specific events to a file.

**Prerequisites**
1. Python 3 installed on your system
2. Access to the Asterisk Manager Interface (AMI) with appropriate credentials
3. Knowledge of the events you want to monitor and their corresponding event names
**Setup**
1. Clone or download the script to your local machine.
2. Install any required Python dependencies (if applicable).
3. Open the script and update the following variables with your configuration:
4. AMI_HOST: The IP address of your Asterisk server.
5. AMI_PORT: The port number for the AMI.
6. AMI_USERNAME: Your AMI username.
7. AMI_PASSWORD: Your AMI password.
8. DID_TO_CALL: The destination DID you want to call.
9. EVENT_TO_TRACK: The event you want to monitor (e.g., "Newstate" for call state changes).
10. LOG_FILE: The path to the log file where event details will be stored.
11. Save the changes to the script.

**Usage**
1. Open a terminal or command prompt.
2. Navigate to the directory containing the script.
3. Run the script using the following command:
Copy code
python ami_event_monitor.py
**License**
This project is licensed under the MIT License - see the LICENSE file for details.
