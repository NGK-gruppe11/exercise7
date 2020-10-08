#!/usr/bin/python3

import sys
import socket
from lib import Lib

HEADER = 1000
SERVER = "192.168.8.101"
PORT = 5050
ADDR = (SERVER, PORT)

def main(argv):
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print("Klient connecter til ", ADDR)

	client.connect(ADDR)
	print("Klient connected.")
	fileMsg = input("Input: ")

	# file size
	client.sendto(fileMsg.encode(), ADDR)
	bytesAdrPair = client.recvfrom(HEADER)
	msgFromServer = bytesAdrPair[0]
	print(msgFromServer.decode())

	# receive file
	with open(fileMsg, "wb") as file:
		print("Getting file...")
		while True:
			data = client.recv(HEADER)
			file.write(data)
			if not data:
				break

		print("File received.")
	client.close()

if __name__ == "__main__":
   main(sys.argv[1:])
