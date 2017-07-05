from __future__ import print_function
import socket
import threading
import sys
import codecs
import binascii
#import message_pb2

class ThreadedServer(object):
	def __init__(self, host, port):
		self.host = host
		self.port = port
		self.running = True
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.sock.bind((self.host, self.port))

	def listen(self):
		self.sock.listen(5)
		print ('Server started and listening')
		while self.running:
			client, address = self.sock.accept()
			client.settimeout(60)
			client_thread = threading.Thread(target = self.listenToClient, args = (client, address))
			client_thread.start()

	def listenToClient(self, client, address):
		size = 5
		while True:
			try:
				data = client.recv(size)
				#print("Raw data:", repr(data), "Decoded data:", hexData)
				# data is a string representing the data received
				if data:
					hexData = binascii.hexlify(data).decode('utf8')  # turns into string of length 10
					header, packetCount, source, value, footer = hexData[:2], hexData[2:4], hexData[4:6], hexData[6:8], hexData[8:]
					host, port = address

					print("Received message from address {}".format(host))
					print("Message header: {} | Packet count: {} | Source: {} | Value: {} | Footer: {}\n".format(header, int(packetCount, 16), source, value, footer))
					response = data
					client.send(response)
				else:
					raise Exception('Client disconnected')  # this occurs when socket.close happens on the client side
			except Exception as e:
				#dataToSend = "0F000000F0"
				#response = binascii.unhexlify(dataToSend)
				#client.send(response)
				#client.close()
				print("Stopping server, reason:", e)
				self.stopServer()
				return False
				
	def stopServer(self):
		self.running = False

if __name__ == "__main__":
	port_num = 2000
	try:
		ThreadedServer('',port_num).listen()
	except KeyboardInterrupt:
		print("Program interrupted, exiting now")
		sys.exit()
