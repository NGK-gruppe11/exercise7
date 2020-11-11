#!/usr/bin/python3

import sys
import socket
from lib import Lib

HEADER = 1000
SERVER = "10.0.0.1"
PORT = 9000
ADDR = (SERVER, PORT)

def main(argv):
	client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	print("Klient connecter til ", ADDR)

	print("Klient connected.")
	msg = input("Input: ")

	# file size
	client.sendto(msg.encode(), ADDR)
	bytesAdrPair = client.recvfrom(HEADER)
	msgFromServer = bytesAdrPair[0]
	print(msgFromServer.decode())

	# receive file
	if msgFromServer.decode() == 'U' or msgFromServer.decode() == 'u':
		fileMsg = "uptime"
	elif msgFromServer.decode() == 'L' or msgFromServer.decode() == 'l':
		fileMsg = "loadavg"

	print("Getting file: ", fileMsg)
	data, addr = client.recvfrom(HEADER)
	while data:
		print(data.decode());
		# client.settimeout(2)
		data, addr = client.recvfrom(HEADER)
		if not data:
			break

	print("File received.")

	client.close()

if __name__ == "__main__":
   main(sys.argv[1:])
