# Distributed-chat-system

## Input file generator

How to generate inputfile for Chat app

```
python.exe gen.py <n> <m> <ips>
```

 - `n`: number of users in chat system
 - `m`: number of messages to be sent
 - `ips`: space separated list of n IP addresses [only IP, please do not pass Port number]
 - `input.txt` file is created after running `gen.py`

 Example:
 `./gen.py 5 10 192.168.29.1 192.168.29.2 192.168.29.3 192.168.29.4 192.168.29.5`

How to generate inputfile for Leader election

```
python gen_leader.py <n> <ips>
```

 - `n`: number of users in unidirectional ring
 - `ips`: space separated list of n IP address.
 - `leader_input.txt` file is created after running `gen_leader.py`

---

## Part 1: Distributed Chat Simulation

How to run chat app:
```
./app.py 
```
 - Program will automatically figure out your IP and assign a corresponding UserID.
 - Keep `input.txt` in same directory as `app.py`.
 - `input.txt` must be exactly same for each node.
 - Make sure to connect devices to same network/Wi-Fi. (Hack: turn on hotspot in one of the phone and connect all devices to it. This probably won't have any issues due to different proxies on same network.)

ToDo:

 - [X] Improve terminal output using [Py-console library](https://towardsdatascience.com/python-printing-colorful-outputs-with-ease-b4e2a183db7c).

Output:

<img src="Output.png">

## Part 2: Leader election Simulation

We implemented **Chang-Roberts Algorithm** on unidirectional ring.

How to run leader election:
```
./leader.py
```
 - All instructions remain same as chat app.
 - Same network.
 - Keep `leader_input.txt` and `leader.py` in same folder

Output:
<img src="Leader Election/leader output.png">