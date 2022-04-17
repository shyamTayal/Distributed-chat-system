import socket


# Class to manage functions needed to simulate Leader election
class Leader:
    HOST = ''
    PORT = 8000

    # constructor: initiates class with default variables
    def __init__(self, file_name):
        self.NUM_USERS = 0
        self.CYCLE = []
        self.USERID_2_IP = {}
        self.IP_2_USERID = {}
        self.MSG_QUEUE = []
        self.NEXT_ID = 0
        self.parse(file_name)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 1))
        local_ip_address = s.getsockname()[0]
        self.MY_IP = local_ip_address
        self.MY_USER_ID = self.IP_2_USERID[self.MY_IP]
        self.get_id_of_my_next_neighbour()
        '''
        COLOR:
         - RED: initiator and takes part in leader election
         - BLACK: follower and doesn't take part in leader election, only passes received messages
        '''
        # initially every process is initiator i.e. COLOR=RED
        self.COLOR = 'RED'

    # finds ID of next process in unidirectional ring or Successor of current Process in ring
    def get_id_of_my_next_neighbour(self):
        for ID in self.CYCLE:
            if ID == self.MY_USER_ID:
                self.NEXT_ID = self.CYCLE[self.CYCLE.index(ID) + 1]

    # returns USER ID from provided IP
    def get_user_id(self, ip):
        return self.IP_2_USERID[ip]

    # returns IP from user's ID
    def get_ip(self, user_id):
        return self.USERID_2_IP[user_id]

    # sends LEADER message ('I am Leader.') to every other process
    def send_leader_msg(self):
        print("👑 | I am the leader.")
        for id in self.USERID_2_IP:
            if id != self.MY_USER_ID:
                while not self.send_msg(f"LEADER|{self.MY_USER_ID}", id):
                    print(f"Retrying..., Sending LEADER msg to user: {id}")
                print(f"Sent LEADER msg to user: {id}")

    # sends normal message(msg) to receiver. returns True if successful else returns False
    def send_msg(self, msg, receiver):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_socket.connect((self.get_ip(receiver), self.PORT))
            client_socket.sendall(msg.encode('utf-8'))
            return True
        except socket.error as e:
            print(f"Error sending msg: {e}")
            return False

    # Main function of algo/simulation
    # manages Token passng and sending Leader messgae to other nodes
    def start_receiving(self):
        # start listening to message on port 8000
        listener_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener_socket.bind((self.HOST, self.PORT))
        listener_socket.listen(999)
        print(f"📞 | Listening started... on port {self.PORT}")
        print("")
        # If process is initiator, send initial toke to your successor
        if self.COLOR == "RED":
            while not self.send_msg(f"TOKEN|{self.MY_USER_ID}", self.NEXT_ID):
                print(
                    f"Retrying..., Sending Token msg to user: {self.NEXT_ID}")
            print(f"Sent Token msg to user: {self.NEXT_ID}")
        leader_found = False
        # run till leader is not found
        while True:
            # accepting incoming messages
            client_socket, addr = listener_socket.accept()
            full_msg = ""
            # collect entire msg as it contains token
            while True:
                chunk = client_socket.recv(1024).decode('utf-8')
                if not chunk:
                    break
                full_msg += chunk
            # split msg by '|'
            # first half of msg contains whether it is Normal message or Leader's message
            # second half of msg contains ID of initiating process
            [type, id] = full_msg.split("|")
            id = int(id)
            # If msg type is LEADER then leader was found.
            if type == "LEADER" and not leader_found:
                leader_found = True
                print("👑 | Leader found!")
                print(f"{id} is our leader.")
                break
            # if msg type is TOKEN and Leader is not found yet
            elif type == "TOKEN" and not leader_found:
                # if you are colored black i.e. currently you are Non-initiator. Simply pass token to successor process
                if self.COLOR == "BLACK":
                    while not self.send_msg(f"{full_msg}", self.NEXT_ID):
                        print(
                            f"Retrying..., Passing Token msg to user: {self.NEXT_ID}"
                        )
                    print(
                        f"Passed Token msg ('{full_msg}') to user: {self.NEXT_ID}"
                    )
                # if you are currently a Initiator.
                elif self.COLOR == "RED":
                    # if ID in token is greater than your ID then, you become non-initiator and pass token to successor
                    if id > self.MY_USER_ID:
                        self.COLOR = "BLACK"
                        while not self.send_msg(f"{full_msg}", self.NEXT_ID):
                            print(
                                f"Retrying..., Passing Token msg to user: {self.NEXT_ID}"
                            )
                        print(
                            f"Passed Token msg ('{full_msg}') to user: {self.NEXT_ID}"
                        )
                    # if ID in token is less than your ID then, do nothing
                    elif id < self.MY_USER_ID:
                        # do nothing
                        print(f"Skipped token {full_msg}")
                        pass
                    # if ID in token and your ID are same then you are leader.
                    # send Leader message to every Node.
                    elif id == self.MY_USER_ID:
                        leader_found = True
                        self.send_leader_msg()
                        break

    # reads and parses the input file
    # scraps out details from input file
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

    # prints Initial detail of user and system
    def to_string(self):
        print("")
        print("=" * 50)
        print(f"🆔 | User ID: {self.MY_USER_ID}")
        print(f"📍 | User IP: {self.MY_IP}")
        print(
            f"🌈 | Curr Color: {'🔴(RED)' if self.COLOR=='RED' else '⚫(BLACK)'}")
        print(f"👥 | # of users: {self.NUM_USERS}")
        print(f"🔁 | Unidirectional Ring: {' -> '.join(map(str,self.CYCLE))}")
        print(f"👉 | My Next ID: {self.NEXT_ID}")
        print("=" * 50)
        print("")


if __name__ == "__main__":
    header_text = '''
+-+-+-+-+-+-+ +-+-+-+-+-+-+-+-+
|L|e|a|d|e|r| |E|l|e|c|t|i|o|n|
+-+-+-+-+-+-+ +-+-+-+-+-+-+-+-+
    '''
    print(header_text)
    leader = Leader('input.txt')
    leader.to_string()
    leader.start_receiving()