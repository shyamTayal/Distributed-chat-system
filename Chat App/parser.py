NUM_USERS = 0
USERID_2_IP = {}
IP_2_USERID = {}
MSG_QUEUE = []
with open("input.txt", "r") as f:
    data = f.read().splitlines()
    
    NUM_USERS = int(data[0])
    
    for i in range(1, NUM_USERS+1):
        id, ip = data[i].split(' ')
        USERID_2_IP[int(id)] = ip
        IP_2_USERID[ip] = int(id)
    for i in range(NUM_USERS+1, len(data)):
        sender, receiver, msg = data[i].split('|')
        MSG_QUEUE.append({"sender":int(sender), "recv":int(receiver), "msg":msg})

print("Number of users:", NUM_USERS)
print("UserID to IP:\n", USERID_2_IP)
print("IP to UserID:\n", IP_2_USERID)
print("Message queue:\n", MSG_QUEUE)