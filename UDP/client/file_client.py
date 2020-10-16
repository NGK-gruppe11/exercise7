#!/usr/bin/python3

import sys
import socket
from lib import Lib

HEADER = 1000
SERVER = "192.168.199.137"
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
		fileMsg = "uptime.txt"
	elif msgFromServer.decode() == 'L' or msgFromServer.decode() == 'l':
		fileMsg = "loadavg.txt"

	with open(fileMsg, "wb") as file:
		print("Getting file...")
		data, addr = client.recvfrom(HEADER)
		while data:
			print(data.decode());
			client.settimeout(2)
			data, addr = client.recvfrom(HEADER)

		print("File received.")

	client.close()

if __name__ == "__main__":
   main(sys.argv[1:])
