#!/usr/bin/python3

import sys
import socket
from lib import Lib

HEADER = 1000
SERVER = "192.168.8.101"
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
	if(msgFromServer.decode() == 'U'):
		fileMsg = "uptime.txt"
	elif(msgFromServer.decode() == 'L'):
		fileMsg = "loadavg.txt"

	with open(fileMsg, "wb") as file:
		print("Getting file...")
		while True:
			data = client.recvfrom(HEADER)
			file.write(data)
			if not data:
				break

		print("File received.")

	client.close()

if __name__ == "__main__":
   main(sys.argv[1:])
