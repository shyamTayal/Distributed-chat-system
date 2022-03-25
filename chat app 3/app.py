import socket
import time
class User:
    HOST = ''
    PORT = 8000
    def __init__(self, file_name):
        self.NUM_USERS=0
        self.USERID_2_IP={}
        self.IP_2_USERID={}
        self.MSG_QUEUE=[]
        self.parse(file_name)
        self.MY_IP=socket.gethostbyname(socket.gethostname())
        # self.MY_PORT=8000
        self.MY_USER_ID=self.IP_2_USERID[self.MY_IP]
    def filter(self):
        self.MSG_QUEUE = [msg for msg in self.MSG_QUEUE if msg["sender"] == self.MY_USER_ID or msg["recv"] == self.MY_USER_ID]
    def parse(self, file):
        with open(file, "r") as f:
            data = f.read().splitlines()

            self.NUM_USERS = int(data[0])

            for i in range(1, self.NUM_USERS+1):
                id, ip = data[i].split(' ')
                self.USERID_2_IP[int(id)] = str(ip)
                self.IP_2_USERID[str(ip)] = int(id)
            for i in range(self.NUM_USERS+1, len(data)):
                sender, receiver, msg = data[i].split('|')
                self.MSG_QUEUE.append({"sender":int(sender), "recv":int(receiver), "msg":msg})
    def get_user_id(self, ip):
        return self.IP_2_USERID[ip]
    def get_ip(self, user_id):
        return self.USERID_2_IP[user_id]
    def send_msg(self, msg, receiver):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_socket.connect((self.get_ip(receiver), self.PORT))
            client_socket.sendall(msg.encode('utf-8'))
            return True
        except socket.error as e:
            print(f"Error sending msg: {e}")
            return False
    def start_receiving(self):
        listener_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener_socket.bind((self.HOST, self.PORT))
        listener_socket.listen(999)
        print(f"Listening started... on port {self.PORT}")
        temp_queue=[]
        msg_idx=0
        while True and msg_idx < len(self.MSG_QUEUE):
            if(self.MSG_QUEUE[msg_idx]["sender"] == self.MY_USER_ID):
                # send msg
                print(f"Sending msg to {self.MSG_QUEUE[msg_idx]['recv']} : {self.MSG_QUEUE[msg_idx]['msg']}")
                while not self.send_msg(self.MSG_QUEUE[msg_idx]["msg"], self.MSG_QUEUE[msg_idx]["recv"]):
                    print("Error sending msg, retrying...")
                print(f"Sent successfully")
                msg_idx+=1
                # time.sleep(1)
            elif(self.MSG_QUEUE[msg_idx]["recv"] == self.MY_USER_ID):
                # receive msg
                found_in_queue = False
                for idx, old_msg in enumerate(temp_queue):
                    if(old_msg["from"] == self.MSG_QUEUE[msg_idx]["sender"]):
                        print(f"Received msg from {old_msg['from']} : {old_msg['msg']}")
                        msg_idx+=1
                        del temp_queue[idx]
                        found_in_queue = True
                        break
                if(not found_in_queue):
                    while True:
                        client_socket, addr = listener_socket.accept()
                        full_msg = ""
                        while True:
                            chunk = client_socket.recv(1024).decode('utf-8')
                            if not chunk:
                                break
                            full_msg += chunk
                        ip, port = addr
                        if self.get_user_id(ip) == self.MSG_QUEUE[msg_idx]["sender"]:
                            print(f"Received msg from {self.MSG_QUEUE[msg_idx]['sender']} : {full_msg}")
                            msg_idx+=1
                            break
                        elif self.get_user_id(ip) != self.MSG_QUEUE[msg_idx]["sender"]:
                            print(f"(Waiting in queue) Received msg from {self.get_user_id(ip)} : {full_msg}")
                            temp_queue.append({"from":self.get_user_id(ip), "msg":full_msg})
                            break
                # time.sleep(1)
    def to_string(self):
        print(f"My User ID: {self.MY_USER_ID}")
        print(f"My IP: {self.MY_IP}")
        # print("My Port:", self.MY_PORT)
        print(f"Number of users: {self.NUM_USERS}")
        print(f"UserID to IP:\n {self.USERID_2_IP}")
        print(f"IP to UserID:\n {self.IP_2_USERID}")
        print(f"Message queue:\n {self.MSG_QUEUE}")
        print("="*80)

if __name__ == "__main__":
    user = User("input.txt")
    user.filter()
    user.to_string()
    user.start_receiving()