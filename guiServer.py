import sys
import socket
import threading
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtNetwork import QTcpServer, QTcpSocket, QAbstractSocket, QHostAddress
from PyQt5.QtCore import QThread, QReadWriteLock, QDataStream, pyqtSignal
from ui_mainwindow import Ui_MainWindow


class Thread(QThread):

	sendData = pyqtSignal(bytes, str)

	def __init__(self, socketId, parent = None):
		super().__init__(parent)
		self.socketId = socketId
		self.guiDisplay = False

	def run(self):
		socket = QTcpSocket()
		if not socket.setSocketDescriptor(self.socketId):  # initializes socket, puts into connected state
			self.emit(SIGNAL("error(int)"), socket.error())
			return
		address = QHostAddress(socket.peerAddress()).toString()
		while socket.state() == QAbstractSocket.ConnectedState:
			data = bytes(5)
			stream = QDataStream(socket)
			stream.setVersion(QDataStream.Qt_5_9)
			while True:
				socket.waitForReadyRead(-1)
				if socket.bytesAvailable() >= 5:
					data = stream.readRawData(5)
					self.sendData.emit(data, address)
					break


class ThreadedServer(QTcpServer):
	dataOut = pyqtSignal(bytes, str)

	def __init__(self, parent = None):
		super().__init__(parent)
		self.client_list = []

	def incomingConnection(self, socketId):
		thread = Thread(socketId, self)
		thread.finished.connect(thread.deleteLater)
		self.client_list.append(thread)
		thread.sendData.connect(self.newData)
		thread.start()

	def newData(self, data, ip):
		self.dataOut.emit(data, ip)

	def newClient(self, ip):
		self.client_list.append(ip)
		self.ipOut.emit(ip)


class MyWindow(QMainWindow):
	def __init__(self, parent = None):
		super().__init__(parent)
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)

		# Set up server
		self.server = ThreadedServer(self)

		# Connect buttons
		self.ui.startButton.clicked.connect(self.startServer)
		self.ui.stopButton.clicked.connect(self.server.close)

		self.server.newConnection.connect(self.handleClient)

	def startServer(self):
		if not self.server.listen(QHostAddress("0.0.0.0"), port_num):
			# TODO: fix this message box
			QMessageBox.critical(self, "Raspberry Pi server", QString("Failed to start server: %1").arg(self.server.errorString()))
			self.close()
			return

	def debug(self):
		print("New connection")

	def handleClient(self):
		for thread in self.server.client_list:
			if thread.guiDisplay == False:
				self.server.dataOut.connect(self.convertData)
				thread.guiDisplay = True
			else:  # if already running, do nothing
				pass

	def convertData(self, data, ip):
		output = data.hex()
		#print(repr(output))
		header, packetCount, source, value, footer = output[:2], str(int(output[2:4], 16)), output[4:6], output[6:8], output[8:]

		# Determine which rover is sending data using static ip address from wifly
		if "103" in ip:
			self.ui.ipValue.setText(ip)
			self.ui.forwardValue.setText(header)
			self.ui.leftValue.setText(packetCount)
			self.ui.rightValue.setText(source)
			self.ui.lineValue.setText(value)
			self.ui.xValue.setText(footer)
		elif "104" in ip:
			self.ui.ipValue_2.setText(ip)
			self.ui.forwardValue_2.setText(header)
			self.ui.leftValue_2.setText(packetCount)
			self.ui.rightValue_2.setText(source)
			self.ui.lineValue_2.setText(value)
			self.ui.xValue_2.setText(footer)


port_num = 2000
app = QApplication(sys.argv)
window = MyWindow()

window.show()
sys.exit(app.exec_())
