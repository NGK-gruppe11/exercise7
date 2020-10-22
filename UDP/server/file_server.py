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
	server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # setup server som ipv4 og UDP
	server.bind(ADDR) # find adresse til server

	while 1:
		print("Server er klar.")
		bytesAddrPair = server.recvfrom(HEADER) # modtag besked fra en klient
		msg = bytesAddrPair[0] # index 0 indeholder selve besked
		clientAddr = bytesAddrPair[1] # index 1 indeholder client addressen
		print("Message received", clientAddr, ":", msg.decode()) # print addresse samt besked
		server.sendto(msg, clientAddr) # send besked retur som verification. klient addresse specificeres nu som argument

		# hvis besked er 'u' sættes fil til uptime og hvis den er 'l' sættes den til loadavg
		if msg.decode() == 'U' or msg.decode() == 'u':
			fileMsg = "/proc/uptime"
		elif msg.decode() == 'L' or msg.decode() == 'l':
			fileMsg = "/proc/loadavg"
		
		print("File to send:", fileMsg)

		sendFile(fileMsg, clientAddr, server) # funktion der sender fil. client addresse og server er argumenter, da funktion skal vide hvem der sender/modtager


def sendFile(fileName, clientAddr, server):
	try:
		# send size af fil
		msg = "File size: " + str(Lib.check_File_Exists(fileName))
		server.sendto(msg.encode(), clientAddr)
	except:
		# send fejl besked
		server.sendto("File not found!".encode(), clientAddr)

	with open(fileName, "rb") as file: # læs fra filen
		data = file.read(HEADER) # læs første 1000 bytes
		print("Sending...")
		while data: # send mens der er data tilbage
			server.sendto(data, clientAddr)
			data = file.read(HEADER)
	print("File sent.")

if __name__ == "__main__":
	main(sys.argv[1:])
