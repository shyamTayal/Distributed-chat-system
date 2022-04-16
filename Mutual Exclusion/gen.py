# libraries
from math import floor
import random
import sys

# ./generator.py <number of users: n> <n ipaddresses>
num_users = int(sys.argv[1])
# msgs = int(sys.argv[2])
ip_address = []
for i in range(2, len(sys.argv)):
    ip_address.append(sys.argv[i])

f = open("input.txt", "w")

f.write(str(num_users) + "\n")
for idx, ip in enumerate(ip_address):
    f.write("%s %s\n" % (idx+1, ip))

ids_order = random.sample(range(1, num_users+1), num_users)
for ID in ids_order:
    f.write(f"{ID} ")

f.write(f"{ids_order[0]}\n")

round_cnt = 5
for idx in range(0, round_cnt):
    tmp = []
    for i in range(num_users):
        tmp.append(str(floor(random.random()*100)%2))
    f.write(f"{' '.join(tmp)}\n")
f.close()

# Generated file format
'''
n -> number of users
next n lines contain "ID IPAddress"
Ring: order of users in ring 
next 5 lines contain n binary values. 
0 at index i in row j means: in round j user with ID=i+1 do not WANT to enter critical section
1 at index i in row j means: in round j user with ID=i+1 WANT to enter critical section
'''