# libraries
import random
import sys

# ./generator.py <number of users: n> <number of messages: m> <n ipaddress(es)>
num_users = int(sys.argv[1])
msgs = int(sys.argv[2])
ip_address = []

for i in range(3, len(sys.argv)):
    ip_address.append(sys.argv[i])

f = open("input.txt", "w")

f.write(str(num_users) + "\n")
for idx, ip in enumerate(ip_address):
    f.write("%s %s\n" % (idx+1, ip))

user_ids = [x for x in range(1, num_users+1)]
for i in range(0, msgs):
    src = random.choice(user_ids)
    dst=0
    while True:
        dst = random.choice(user_ids)
        if dst != src:
            break
    message = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz ,.-', k=random.randint(6, 20)))
    f.write("%s|%s|%s\n" % (src, dst, message))