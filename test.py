import sys
import socket
import select
import threading
import codecs
import binascii
from PyQt5.QtWidgets import QApplication, QMainWindow
from ui_mainwindow import Ui_MainWindow

class ThreadedServer(object):
	def __init__(self, host, port):
		self.host = host
		self.port = port
		self.stopPressed = False
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.sock.bind((self.host, self.port))

	def listen(self):
		self.sock.listen(5)
		self.sock.setblocking(0)
		self.stopPressed = False
		print("Server started and listening")
			
		while not self.stopPressed:
			try:
				client, address = self.sock.accept()
				client_thread = threading.Thread(target = self.listenToClient, args = (client, address))
				client_thread.start()
			except:
				print("No connection")
				pass

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
				client.close()
				return False
				
	def stopServer(self):
		self.stopPressed = True
		print("Stopping server")

        
class MyWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		self.server = ThreadedServer('', port_num)
		self.ui.startButton.clicked.connect(self.server.listen)
		self.ui.stopButton.clicked.connect(self.server.stopServer)

		
port_num = 2000
app = QApplication(sys.argv)
window = MyWindow()

window.show()
sys.exit(app.exec_())