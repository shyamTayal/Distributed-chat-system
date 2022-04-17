# libraries
from math import floor
import random
import sys

# ./generator.py <number of users: n> <n ipaddresses>
num_users = int(sys.argv[1])

# list of passed IP addresses
ip_address = []
for i in range(2, len(sys.argv)):
    ip_address.append(sys.argv[i])

f = open("input.txt", "w")

# write number of users
f.write(str(num_users) + "\n")

# write ID and their IP to file
for idx, ip in enumerate(ip_address):
    f.write("%s %s\n" % (idx + 1, ip))

# randomly arrange IDs to generate ring order
ids_order = random.sample(range(1, num_users + 1), num_users)
# write ring order to file
for ID in ids_order:
    f.write(f"{ID} ")
f.write(f"{ids_order[0]}\n")

# randomly generate 5 rows with num_users binary values
round_cnt = 5
for idx in range(0, round_cnt):
    tmp = []
    for i in range(num_users):
        # 1 means process i+1 wants to enter critical section in round idx
        # 0 means process i+1 do not want to enter critical section in round idx
        tmp.append(str(floor(random.random() * 100) % 2))
    f.write(f"{' '.join(tmp)}\n")
f.close()