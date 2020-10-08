#!/usr/bin/python3

import sys
import socket
from lib import Lib

HEADER = 1000
SERVER = "192.168.8.101" # local ip
PORT = 5050
ADDR = (SERVER, PORT)
FORMAT = 'utf-4'

def main(argv):

	print("Server set to ", ADDR)
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	server.bind(ADDR)
	server.listen()

	while 1:
		print("Server er klar.")
		conn, addr = server.accept()
		print("Socket accept", addr)

		msg = conn.recv(HEADER)
		print("Besked modtaget fra klient:", msg.decode())
		
		sendFile(msg.decode(), conn)

		conn.close()

def sendFile(fileName, conn):
	try:
		msg = "File size: " + str(Lib.check_File_Exists(fileName))
		conn.send(msg.encode())
	except:
		conn.send("File not found!".encode())

	with open(fileName, "rb") as file:
		data = file.read(HEADER)
		print("Sending...")
		while data:
			conn.send(data)
			data = file.read(HEADER)
	print("File sent.")

if __name__ == "__main__":
	main(sys.argv[1:])
