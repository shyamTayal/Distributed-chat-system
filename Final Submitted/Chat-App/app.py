# libraries
import socket
import time

# Class to handle chat at user end
class User:
    HOST = ''
    PORT = 8000
    
    # class constructor: initiates object with default variables
    def __init__(self, file_name):
        self.NUM_USERS = 0
        self.USERID_2_IP = {}
        self.IP_2_USERID = {}
        self.MSG_QUEUE = []
        self.parse(file_name)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 1))
        local_ip_address = s.getsockname()[0]
        self.MY_IP = local_ip_address
        self.MY_USER_ID = self.IP_2_USERID[self.MY_IP]

    # filter out the message in which current user is either sending or receiving, ignore rest of messages
    def filter(self):
        self.MSG_QUEUE = [
            msg for msg in self.MSG_QUEUE if msg["sender"] == self.MY_USER_ID
            or msg["recv"] == self.MY_USER_ID
        ]

    # open and parse input file.
    # extract detail about system from input file
    def parse(self, file):
        with open(file, "r") as f:
            data = f.read().splitlines()
            self.NUM_USERS = int(data[0])
            for i in range(1, self.NUM_USERS + 1):
                id, ip = data[i].split(' ')
                self.USERID_2_IP[int(id)] = str(ip)
                self.IP_2_USERID[str(ip)] = int(id)
            for i in range(self.NUM_USERS + 1, len(data)):
                sender, receiver, msg = data[i].split('|')
                self.MSG_QUEUE.append({
                    "sender": int(sender),
                    "recv": int(receiver),
                    "msg": msg
                })
    
    # returns USER ID provided a IP address
    def get_user_id(self, ip):
        return self.IP_2_USERID[ip]

    # returns IP address provided a user's ID
    def get_ip(self, user_id):
        return self.USERID_2_IP[user_id]

    # sends mesage `msg` to  `receiver` and returns True on success else returns False on failure
    def send_msg(self, msg, receiver):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_socket.connect((self.get_ip(receiver), self.PORT))
            client_socket.sendall(msg.encode('utf-8'))
            return True
        except socket.error as e:
            print(f"Error sending msg: {e}")
            return False
    # Main function of app it manages all sending and receiving messages to and from other users.
    def start_receiving(self):
        # opens a port to listen incoming messages
        listener_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener_socket.bind((self.HOST, self.PORT))
        listener_socket.listen(999)
        print(f"📞| Listening started... on port {self.PORT}")
        print("")
        temp_queue = []
        msg_idx = 0
        # run till all msgs are not sent or received
        while True and msg_idx < len(self.MSG_QUEUE):
            # if this msg is to be send then try sending it to target user
            if (self.MSG_QUEUE[msg_idx]["sender"] == self.MY_USER_ID):
                # send msg
                print(
                    f"➡️ | To {self.MSG_QUEUE[msg_idx]['recv']} \t: {self.MSG_QUEUE[msg_idx]['msg']}"
                )
                while not self.send_msg(self.MSG_QUEUE[msg_idx]["msg"],
                                        self.MSG_QUEUE[msg_idx]["recv"]):
                    print("Error sending msg, retrying...")
                msg_idx += 1
                time.sleep(1)
            # else wait to receive msg from other node
            elif (self.MSG_QUEUE[msg_idx]["recv"] == self.MY_USER_ID):
                # receive msg
                found_in_queue = False
                for idx, old_msg in enumerate(temp_queue):
                    if (old_msg["from"] == self.MSG_QUEUE[msg_idx]["sender"]):
                        print(
                            f"⬅️ | From {old_msg['from']} \t: {old_msg['msg']}"
                        )
                        del temp_queue[idx]
                        found_in_queue = True
                        msg_idx += 1
                        break
                if (not found_in_queue):
                    while True:
                        client_socket, addr = listener_socket.accept()
                        full_msg = ""
                        # collect entire msg
                        while True:
                            chunk = client_socket.recv(1024).decode('utf-8')
                            if not chunk:
                                break
                            full_msg += chunk
                        ip, port = addr
                        if self.get_user_id(
                                ip) == self.MSG_QUEUE[msg_idx]["sender"]:
                            print(
                                f"⬅️ | From {self.MSG_QUEUE[msg_idx]['sender']} \t: {full_msg}"
                            )
                            msg_idx += 1
                            break
                        elif self.get_user_id(
                                ip) != self.MSG_QUEUE[msg_idx]["sender"]:
                            temp_queue.append({
                                "from": self.get_user_id(ip),
                                "msg": full_msg
                            })
                time.sleep(1)

    # prints initial detail of User and chat group to console
    def to_string(self):
        print("=" * 50)
        print(f"👤 | User ID: {self.MY_USER_ID}")
        print(f"📍 | User IP: {self.MY_IP}")
        print(f"👥 | # of users: {self.NUM_USERS}")
        print("=" * 50)
        print("")

if __name__ == "__main__":
    header_art = '''
+-+-+-+-+-+-+-+-+-+-+-+ +-+-+-+-+ +-+-+-+
|D|i|s|t|r|i|b|u|t|e|d| |C|h|a|t| |A|p|p|
+-+-+-+-+-+-+-+-+-+-+-+ +-+-+-+-+ +-+-+-+
    '''
    print(header_art)
    user = User("input.txt")
    user.filter()
    user.to_string()
    user.start_receiving()