# libraries
import random
import sys

# ./generator.py <number of users: n> <n ipaddresses>
num_users = int(sys.argv[1])
# msgs = int(sys.argv[2])
ip_address = []
MAX_USERS = 1000
for i in range(2, len(sys.argv)):
    ip_address.append(sys.argv[i])

f = open("leader_input.txt", "w")

rand_IDs = random.sample(range(1, MAX_USERS+1), num_users)

f.write(str(num_users) + "\n")
for idx, ip in enumerate(ip_address):
    f.write("%s %s\n" % (rand_IDs[idx], ip))

for ID in rand_IDs:
    f.write(f"{ID} ")

f.write(f"{rand_IDs[0]}")
f.close()