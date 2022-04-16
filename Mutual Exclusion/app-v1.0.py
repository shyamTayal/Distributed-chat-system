import random
import socket
import time

class MutualEx:
    HOST = ''
    PORT = 8000

    def __init__(self, file_name):
        self.NUM_USERS = 0
        self.CYCLE = []
        self.USERID_2_IP = {}
        self.IP_2_USERID = {}
        self.MSG_QUEUE = []
        self.NEXT_ID = 0
        self.curr_round = 0
        self.cs_rounds = []
        self.parse(file_name)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 1))
        local_ip_address = s.getsockname()[0]
        self.MY_IP = local_ip_address
        self.MY_USER_ID = self.IP_2_USERID[self.MY_IP]
        self.get_id_of_my_next_neighbour()
        self.has_token = self.MY_USER_ID == 1

    def get_id_of_my_next_neighbour(self):
        for ID in self.CYCLE:
            if ID == self.MY_USER_ID:
                self.NEXT_ID = self.CYCLE[self.CYCLE.index(ID) + 1]

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

    def critical_section(self):
        print('\t🏃 Executing CS...')
        time.sleep(random.random() * 5)

    def start_receiving(self):
        listener_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener_socket.bind((self.HOST, self.PORT))
        listener_socket.listen(999)
        print(f"📞 | Listening started... on port {self.PORT}")
        print("")

        while True:
            if self.has_token:
                # if this round needs CS execution, then execute
                # send token to successor
                # has_token=false
                # increment round
                print('I have TOKEN.')
                if self.curr_round < len(self.cs_rounds) and self.cs_rounds[self.curr_round][self.MY_USER_ID - 1] == '1':
                    print('I NEED to enter CS.')
                    self.critical_section()
                    print('\t✅ Done with CS.')
                elif self.curr_round < len(self.cs_rounds) and self.cs_rounds[self.curr_round][self.MY_USER_ID -
                                                     1] == '0':
                    print('I DO NOT need to enter CS.')
                self.curr_round += 1
                if self.curr_round <= len(self.cs_rounds):
                    while self.curr_round <= len(
                            self.cs_rounds) and not self.send_msg(
                                f"TOKEN", self.NEXT_ID):
                        print(
                            f"Retrying..., Passing TOKEN to user: {self.NEXT_ID}."
                        )
                    print(f"Passed TOKEN to user: {self.NEXT_ID}.")
                    if(self.curr_round == len(self.cs_rounds)):
                        print(f'Round {self.curr_round-1} over.')
                        break
                    
                self.has_token = False
                print(f'Round {self.curr_round-1} over.')
                print('-' * 50)
            elif not self.has_token:
                # receive token
                # set has_token=true
                client_socket, addr = listener_socket.accept()
                [ip, port] = addr
                full_msg = ""
                while True:
                    chunk = client_socket.recv(1024).decode('utf-8')
                    if not chunk:
                        break
                    full_msg += chunk
                if full_msg == "TOKEN":
                    self.has_token = True
                print(f"Recieved TOKEN from {self.get_user_id(ip)}.")

    def parse(self, file):
        with open(file, "r") as f:
            data = f.read().splitlines()
            self.NUM_USERS = int(data[0])
            for i in range(1, self.NUM_USERS + 1):
                id, ip = data[i].split(' ')
                self.USERID_2_IP[int(id)] = str(ip)
                self.IP_2_USERID[str(ip)] = int(id)
            tmp_cycle = data[self.NUM_USERS + 1].split(' ')
            self.CYCLE = [int(i) for i in tmp_cycle]
            for i in range(self.NUM_USERS + 2, len(data)):
                tmp_cs_req = data[i].split(' ')
                self.cs_rounds.append(tmp_cs_req)

    def to_string(self):
        print("")
        print("=" * 50)
        print(f"🆔 | User ID: {self.MY_USER_ID}")
        print(f"📍 | User IP: {self.MY_IP}")
        print(f"👥 | # of users: {self.NUM_USERS}")
        print(f"🔁 | Unidirectional Ring: {' -> '.join(map(str,self.CYCLE))}")
        print(f"👉 | My Next ID: {self.NEXT_ID}")
        print(f"🔑 | Has token: {'Yes' if self.has_token else 'No'}")
        print("=" * 50)
        print("")


if __name__ == "__main__":
    header_text = 'Mutual Exclusion'
    print(header_text)
    mutex = MutualEx('input.txt')
    mutex.to_string()
    mutex.start_receiving()