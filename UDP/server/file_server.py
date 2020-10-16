#!/usr/bin/python3

import sys
import socket
from lib import Lib

HEADER = 1000
SERVER = "192.168.199.137" # local ip
PORT = 9000
ADDR = (SERVER, PORT)
FORMAT = 'utf-4'

def main(argv):
	print("Server set to ", ADDR)
	server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	server.bind(ADDR)

	while 1:
		print("Server er klar.")
		bytesAddrPair = server.recvfrom(HEADER)
		msg = bytesAddrPair[0]
		clientAddr = bytesAddrPair[1]
		print("Message received", clientAddr, ":", msg.decode())
		server.sendto(msg, clientAddr)

		if msg.decode() == 'U' or msg.decode() == 'u':
			fileMsg = "uptime.txt"
		elif msg.decode() == 'L' or msg.decode() == 'l':
			fileMsg = "loadavg.txt"
		
		print("File to send:", fileMsg)

		sendFile(fileMsg, clientAddr, server) # send file


def sendFile(fileName, clientAddr, server):
	try:
		msg = "File size: " + str(Lib.check_File_Exists(fileName))
		server.sendto(msg.encode(), clientAddr)
	except:
		server.sendto("File not found!".encode(), clientAddr)

	with open(fileName, "rb") as file:
		data = file.read(HEADER)
		print("Sending...")
		while data:
			server.sendto(data, clientAddr)
			data = file.read(HEADER)
	print("File sent.")

if __name__ == "__main__":
	main(sys.argv[1:])
