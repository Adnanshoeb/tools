import socket
import time

# AMI credentials
AMI_HOST = '127.0.0.1'
AMI_PORT = 5038  # Default AMI port
AMI_USERNAME = 'XXXXX'
AMI_PASSWORD = 'i&XXXX#8S'

# Destination DID
DID_TO_CALL = 'XXXX'

# Event to track (e.g., "Newstate" for call state changes)
EVENT_TO_TRACK = 'Newstate'

# Log file to store wait times
LOG_FILE = 'wait_time_log.txt'

# Create a socket connection to the AMI
ami_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ami_socket.connect((AMI_HOST, AMI_PORT))

def send_command(command):
    ami_socket.send(command.encode())

def originate_call(did):
    originate_cmd = "Action: Originate\r\nChannel: SIP/Aarenet/{}\r\nExten: XXXXX\r\nContext: extension-context-ASTERISK_SIP-10\r\nPriority: 1\r\nCallerid: CXXXX\r\nTimeout: 30000\r\n\r\n".format(did)
    send_command(originate_cmd)

# Log in to the AMI
login_command = "Action: Login\r\nUsername: {}\r\nSecret: {}\r\n\r\n".format(AMI_USERNAME, AMI_PASSWORD)
send_command(login_command)

# Originate a call
originate_call(DID_TO_CALL)

# Subscribe to events
subscribe_command = "Action: Waitevent\r\nEventmask: {}\r\n\r\n".format(EVENT_TO_TRACK)
send_command(subscribe_command)

# Monitor events
while True:
    response = ami_socket.recv(4096).decode()
    if EVENT_TO_TRACK in response and DID_TO_CALL in response:
        event_time = time.strftime('%Y-%m-%d %H:%M:%S')
        with open(LOG_FILE, 'a') as log_file:
            log_file.write("{}: {} event received\n".format(event_time, EVENT_TO_TRACK))

    time.sleep(1)  # Adjust the sleep duration as needed

# Close the socket connection
ami_socket.close()
