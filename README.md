# Distributed-chat-system

## Input file generator

How to generate inputfile

```
python.exe gen.py <n> <m> <ips>
```
 - `n`: number of users in chat system
 - `m`: number of messages to be sent
 - `ips`: space separated list of n IP addresses [only IP, please do not pass Port number]
 - `Input.txt` file is created after running `gen.py`

 Example:
 `./gen.py 5 10 192.168.29.1 192.168.29.2 192.168.29.3 192.168.29.4 192.168.29.5`

---

## Part 1: Distributed Chat Simulation

How to run chat app:
```
./app.py 
```
 - Program will automatically figure out you IP and assign a UserID.
 - Keep `input.txt` in same directory as `app.py`.
 - Make sure to connect devices to same network/Wi-Fi. (Hack: turn hotspot in one of the phone and connect all devices to it. This probably won't have any issues due to different proxies on same network.)

ToDo:

 - [ ] Improve terminal output using [Py-console library](https://towardsdatascience.com/python-printing-colorful-outputs-with-ease-b4e2a183db7c).
