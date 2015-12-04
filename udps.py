# CNT 4400 Computer Networks
# Final Project - GetStock Protocol Application
# 2015-12-02

# udps.py
# UDP Server

import socket
import string
import sys
import os


UDP_IP = "192.168.1.101"
UDP_PORT = 1050
USERS = []
STOCKS = {}

with open('stockfile.txt') as stockfile:
	for line in stockfile:
		name, val = line.partition(" ")[::2]
		STOCKS[name.strip()] = float(val)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

if os.path.isfile('users.txt'):
	with open('users.txt') as userfile:
		USERS = userfile.read().splitlines()

while True:
	data, addr = sock.recvfrom(1024)
	print(data.decode())
	if data[-1] == ';':
		data = data[:-1]
		data = data.split(',')
		if data[0] == "REG":
			if len(data) == 2:
				if data[1].isalnum() and len(data[1]) <= 32:
					if data[1].lower() not in USERS:
						USERS.append(data[1].lower())
						userfile = open('users.txt', 'w')
						for user in USERS:
							userfile.write(user+'\n')
						userfile.close()
						MESSAGE = "ROK;"
					else:
						MESSAGE = "UAE;"
				else:
					MESSAGE = "INU;"
			else:
				MESSAGE = "INP;"
		elif data[0] == "UNR":
			if len(data) == 2:
				if data[1].lower() in USERS:
					USERS.remove(data[1].lower())
					userfile = open('users.txt', 'w')
					for user in USERS:
						userfile.write(user+'\n')
					userfile.close()
					MESSAGE = "ROK;"
				else:
					MESSAGE = "UNR;"
			else:
				MESSAGE = "INP;"
		elif data[0] == "QUO":
			if len(data) > 2:
				if data[1].lower() in USERS:
					rok = "ROK,"
					for i in range(2,len(data)):
						if data[i].upper() in STOCKS:
							rok = rok + str(STOCKS[data[i].upper()]) + ','
						else:
							rok = rok + "-1,"
					MESSAGE = rok[:-1] + ';'
				else:
					MESSAGE = "UNR;"
			else:
				MESSAGE = "INP;"

		else:
			MESSAGE = "INC;"
	else:
		MESSAGE = "INP;"
	sock.sendto(MESSAGE, addr)