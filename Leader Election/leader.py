import pyfiglet
import socket
import time
from termcolor import colored

class Leader:
    HOST=''
    PORT=8000
    def __init__(self, file_name):
        self.NUM_USERS=0
        self.CYCLE = []
        self.USERID_2_IP={}
        self.IP_2_USERID={}
        self.MSG_QUEUE=[]
        self.NEXT_ID = 0
        self.parse(file_name)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 1))  
        local_ip_address = s.getsockname()[0]
        self.MY_IP = local_ip_address
        self.MY_USER_ID=self.IP_2_USERID[self.MY_IP]
        self.get_id_of_my_next_neighbour()
        '''
        COLOR:
         - RED: initiator and takes part in leader election
         - BLACK: follower and doesn't take part in leader election, only passes received messages
        '''
        self.COLOR = 'RED' 
    def get_id_of_my_next_neighbour(self):
        for ID in self.CYCLE:
            if ID == self.MY_USER_ID:
                self.NEXT_ID = self.CYCLE[self.CYCLE.index(ID)+1]
    def get_user_id(self, ip):
        return self.IP_2_USERID[ip]
    def get_ip(self, user_id):
        return self.USERID_2_IP[user_id]
    def send_leader_msg(self):
        print("👑 | I am the leader.")
        for id in self.USERID_2_IP:
            if id != self.MY_USER_ID:
                while not self.send_msg(f"LEADER|{self.MY_USER_ID}", id):
                    print(f"Retrying..., Sending LEADER msg to user: {id}")
                print(f"Sent LEADER msg to user: {id}")
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
        print(f"📞 | Listening started... on port {self.PORT}")
        print("")
        if self.COLOR == "RED":
            while not self.send_msg(f"TOKEN|{self.MY_USER_ID}", self.NEXT_ID):
                print(f"Retrying..., Sending Token msg to user: {self.NEXT_ID}")
            print(f"Sent Token msg to user: {self.NEXT_ID}")
        leader_found = False
        while True:
            client_socket, addr = listener_socket.accept()
            full_msg = ""
            while True:
                chunk = client_socket.recv(1024).decode('utf-8')
                if not chunk:
                    break
                full_msg+=chunk
            [type, id] = full_msg.split("|")
            id = int(id)
            if type == "LEADER" and not leader_found:
                leader_found = True
                print("👑 | Leader found!")
                print(f"{id} is our leader.")
                break
            elif type == "TOKEN" and not leader_found:
                if self.COLOR == "BLACK":
                    while not self.send_msg(f"{full_msg}", self.NEXT_ID):
                        print(f"Retrying..., Passing Token msg to user: {self.NEXT_ID}")
                    print(f"Passed Token msg ('{full_msg}') to user: {self.NEXT_ID}")
                elif self.COLOR == "RED":
                    if id > self.MY_USER_ID:
                        self.COLOR = "BLACK"
                        while not self.send_msg(f"{full_msg}", self.NEXT_ID):
                            print(f"Retrying..., Passing Token msg to user: {self.NEXT_ID}")
                        print(f"Passed Token msg ('{full_msg}') to user: {self.NEXT_ID}")
                    elif id < self.MY_USER_ID:
                        # do nothing
                        print(f"Skipped token {full_msg}")
                        pass
                    elif id == self.MY_USER_ID:
                        leader_found = True
                        self.send_leader_msg()
                        break
    def parse(self, file):
        with open(file, "r") as f:
            data = f.read().splitlines()
            self.NUM_USERS = int(data[0])
            for i in range(1, self.NUM_USERS+1):
                id, ip = data[i].split(' ')
                self.USERID_2_IP[int(id)] = str(ip)
                self.IP_2_USERID[str(ip)] = int(id)
            tmp_cycle = data[self.NUM_USERS+1].split(' ')
            self.CYCLE = [int(i) for i in tmp_cycle]
    def to_string(self):
        print("")
        print("="*50)
        print(f"🆔 | User ID: {self.MY_USER_ID}")
        print(f"📍 | User IP: {self.MY_IP}")
        print(f"🌈 | Curr Color: {'🔴(RED)' if self.COLOR=='RED' else '⚫(BLACK)'}")
        print(f"👥 | # of users: {self.NUM_USERS}")
        print(f"🔁 | Unidirectional Ring: {' -> '.join(map(str,self.CYCLE))}")
        print(f"👉 | My Next ID: {self.NEXT_ID}")
        print("="*50)
        print("")
        

if __name__ == "__main__":
    header_text = pyfiglet.figlet_format("Leader Election in Unidirectional Ring", font = "digital")
    print(header_text)
    leader = Leader('leader_input.txt')
    leader.to_string()
    leader.start_receiving()