# CNT 4400 Computer Networks
# Final Project - GetStock Protocol Application
# 2015-12-02

# udpc.py
# UDP Client

import socket
import string
import sys
import io
import select

UDP_IP = "192.168.1.101"
UDP_PORT = 1050


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setblocking(0)


while True:
	MESSAGE = raw_input()
	sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
	count = 0
	for i in range(0,2):
		ready = select.select([sock], [], [], 5)
		if ready[0]:
			data, addr = sock.recvfrom(1024)
			print(data.decode())
			break
		else:
			print('resending')
			sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
	