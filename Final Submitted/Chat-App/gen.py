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

# number of users
f.write(str(num_users) + "\n")

# write ID and its IP to input file. IDs are incremental in order 
for idx, ip in enumerate(ip_address):
    f.write("%s %s\n" % (idx+1, ip))

# list having IDs
user_ids = [x for x in range(1, num_users+1)]

# generate m random mesage with random sender and receiver
for i in range(0, msgs):
    # choose sender
    src = random.choice(user_ids)
    dst=0
    # choose a different receiver
    while True:
        dst = random.choice(user_ids)
        if dst != src:
            break
    # generate a random text(message) of random lenght [6-19]
    message = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz .,', k=random.randint(6, 20)))
    # write them to input file in format: `sender|receiver|message`
    f.write("%s|%s|%s\n" % (src, dst, message))