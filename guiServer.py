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
		address = QHostAddress(socket.peerAddress()).toString() + ":" + str(socket.peerPort())
		while socket.state() == QAbstractSocket.ConnectedState:
			data = bytes(8)
			stream = QDataStream(socket)
			stream.setVersion(QDataStream.Qt_5_9)
			while True:
				socket.waitForReadyRead(-1)
				if socket.bytesAvailable() >= 8:
					data = stream.readRawData(8)
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


class MyWindow(QMainWindow):
	def __init__(self, parent = None):
		self.ip = ""
		self.front = ""
		self.left = ""
		self.right = ""
		self.irState = ""
		self.lfState = ""
		self.x = ""
		self.y = ""
		self.heading = ""
		self.previous = ""
		self.rover = ""

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

	def handleClient(self):
		for thread in self.server.client_list:
			if thread.guiDisplay == False:
				self.server.dataOut.connect(self.calculateNextCommand)
				thread.guiDisplay = True
			else:  # if already running, do nothing
				pass

	def calculateNextCommand(self, data, address):
		output = data.hex()
		header, source, values, footer = output[:2], int(output[2:4], 16), output[4:14], output[14:]

		if "100" in address:
			self.rover = "pacman"
		elif "104" in address:
			self.rover = "ghost1"
		elif "105" in address:
			self.rover = "ghost2"
		self.ip = address

		# check header

		if source == 0:  # sensors
			self.front, self.left, self.right, self.irState, self.lfState = values[:2], values[2:4], values[4:6], values[6:8], values[8:10]
			self.displaySensorValues(self.rover)
		elif source == 1:  # encoder
			self.x, self.y, self.heading, self.previous, dontcare = values[:2], values[2:4], values[4:6], values[6:8], values[8:10]
			self.displayEncoderValues(self.rover)

		# check footer


	def displaySensorValues(self, rover):
		if rover == "pacman":
			self.ui.ipValue.setText(self.ip)
			self.ui.forwardValue.setText(self.front)
			self.ui.leftValue.setText(self.left)
			self.ui.rightValue.setText(self.right)
			self.ui.lineValue.setText(self.lfState)
		elif rover == "ghost1":
			self.ui.ipValue_2.setText(self.ip)
			self.ui.forwardValue_2.setText(self.front)
			self.ui.leftValue_2.setText(self.left)
			self.ui.rightValue_2.setText(self.right)
			self.ui.lineValue_2.setText(self.lfState)
		elif rover == "ghost2":
			self.ui.ipValue_3.setText(self.ip)
			self.ui.forwardValue_3.setText(self.front)
			self.ui.leftValue_3.setText(self.left)
			self.ui.rightValue_3.setText(self.right)
			self.ui.lineValue_3.setText(self.lfState)

	def displayEncoderValues(self, rover):
		if rover == "pacman":
			self.ui.ipValue.setText(self.ip)
			self.ui.xValue.setText(self.x)
			self.ui.yValue.setText(self.y)
			self.ui.headingValue.setText(self.heading)
			self.ui.piValue.setText(self.previous)
		elif rover == "ghost1":
			self.ui.ipValue_2.setText(self.ip)
			self.ui.xValue_2.setText(self.x)
			self.ui.yValue_2.setText(self.y)
			self.ui.headingValue_2.setText(self.heading)
			self.ui.piValue_2.setText(self.previous)
		elif rover == "ghost2":
			self.ui.ipValue_3.setText(self.ip)
			self.ui.xValue_3.setText(self.x)
			self.ui.yValue_3.setText(self.y)
			self.ui.headingValue_3.setText(self.heading)
			self.ui.piValue_3.setText(self.previous)


if __name__ == '__main__':
	port_num = 2000
	app = QApplication(sys.argv)
	window = MyWindow()

	window.show()
	sys.exit(app.exec_())
