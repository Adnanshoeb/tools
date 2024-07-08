import socket
import time

AMI_HOST = '127.0.0.1'
AMI_PORT = 5038  
AMI_USERNAME = '1XXXX'
AMI_PASSWORD = 'XXXX'

DID_TO_CALL = '0XXXX90'

EVENT_TO_TRACK = 'Newstate'  

LOG_FILE = 'wait_time_log.txt'


def send_command(ami_socket, command):
    try:
        ami_socket.sendall(command.encode())
        response = ami_socket.recv(4096).decode()
        print(f"Command response: {response}")
        return response
    except (OSError, socket.error) as e:
        print(f"Error sending command: {e}")
        return None


def get_active_calls_count(ami_socket):
    active_calls_cmd = "Action: CoreShowChannels\r\n\r\n"
    response = send_command(ami_socket, active_calls_cmd)
    if response is None or "Response: Error" in response:
        print(f"Error retrieving active calls: {response}")
        return None
    print(f"Active calls response: {response}")
    active_calls_count = response.count("Channel:")
    print(f"Number of active calls: {active_calls_count}")
    return active_calls_count


def originate_call(did, ami_socket):
    originate_cmd = (
        "Action: Originate\r\n"
        "Channel: SIP/03XXXX90@SIPNETR/{}\r\n"
        "Exten: 0XXXXX91\r\n"
        "Context: extension-context-ASTERISK_SIP-10\r\n"
        "Priority: 1\r\n"
        "Callerid: XXXX90\r\n"
        "Timeout: 6000\r\n"
        "Async: true\r\n"
        "\r\n".format(did)
    )

    start_time = time.time()
    response = send_command(ami_socket, originate_cmd)
    if response is None or "Response: Error" in response:
        print(f"Error sending originate command: {response}")
        return False

    while True:
        response = ami_socket.recv(4096).decode()
        if EVENT_TO_TRACK in response:
            wait_time = time.time() - start_time
            print(f"Call originated for DID {did} with wait time: {wait_time:.2f} seconds")
            return True


def main():
    while True:
        ami_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        retry_delay = 1  # delay

        try:
            ami_socket.connect((AMI_HOST, AMI_PORT))

            login_command = "Action: Login\r\nUsername: {}\r\nSecret: {}\r\n\r\n".format(AMI_USERNAME, AMI_PASSWORD)
            response = send_command(ami_socket, login_command)

            print(f"AMI initial response: {response}")

            while True:
                response = ami_socket.recv(4096).decode()
                print(f"AMI login response: {response}")
                if "Response: Success" in response:
                    break
                elif "Response: Error" in response:
                    print(f"Login error: {response}")
                    return

            while True:
                active_calls_count = get_active_calls_count(ami_socket)
                if active_calls_count is None:
                    print("Failed to retrieve active calls count.")
                    break

                if active_calls_count < 80:
                    call_result = originate_call(DID_TO_CALL, ami_socket)
                    if not call_result:
                        break
                else:
                    print(f"There are already {active_calls_count} or more connected calls. Waiting before next check.")
                
                time.sleep(0)

        except (OSError, socket.error) as e:
            print(f"Error in main loop: {e}")
            time.sleep(retry_delay)
            retry_delay = min(retry_delay * 2, 60)  # Max delay Exp backoff

        finally:
            ami_socket.close()


if __name__ == "__main__":
    main()
