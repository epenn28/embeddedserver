import sys
import socket
import threading
from enum import Enum
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtNetwork import QTcpServer, QTcpSocket, QAbstractSocket, QHostAddress
from PyQt5.QtCore import QObject, QThread, QReadWriteLock, QDataStream, pyqtSignal
from ui_mainwindow import Ui_MainWindow


class Worker(QObject):

	sendData = pyqtSignal(bytes, str)

	def __init__(self, socketId):
		super().__init__()
		self.socketId = socketId
		self.running = True
		self.socket = None

	def run(self):
		self.socket = QTcpSocket()
		if not self.socket.setSocketDescriptor(self.socketId):  # initializes socket, puts into connected state
			self.emit(SIGNAL("error(int)"), self.socket.error())
			return
		address = QHostAddress(self.socket.peerAddress()).toString() + ":" + str(self.socket.peerPort())
		while self.socket.state() == QAbstractSocket.ConnectedState and self.running:
			data = bytes(8)
			stream = QDataStream(self.socket)
			stream.setVersion(QDataStream.Qt_5_9)
			while True:
				self.socket.waitForReadyRead(-1)
				if self.socket.bytesAvailable() >= 8:
					data = stream.readRawData(8)
					self.sendData.emit(data, address)
					break

	def stopWorker(self):
		self.running = False
		data = b"AA00FF"
		self.socket.write(data)


class ThreadedServer(QTcpServer):
	dataOut = pyqtSignal(bytes, str)
	serverRunning = pyqtSignal(str)

	def __init__(self, parent = None):
		super().__init__(parent)
		self.client_list = []

	def incomingConnection(self, socketId):
		worker = Worker(socketId)
		thread = QThread()
		self.client_list.append((thread, worker))
		worker.moveToThread(thread)
		thread.finished.connect(worker.deleteLater)
		worker.sendData.connect(self.newData)
		thread.started.connect(worker.run)
		thread.start()
		self.serverRunning.emit("Running")# ({})".format(len(self.client_list)))

	def newData(self, data, ip):
		self.dataOut.emit(data, ip)

	def closeServer(self):
		for (thread, worker) in self.client_list:
			worker.stopWorker()
		self.close()


class MyWindow(QMainWindow):
	stateChanged = pyqtSignal(str)

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
		self.serverState = "Init"
		self.stateChanged.emit(self.serverState)
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)

		# Set up server
		self.server = ThreadedServer(self)

		# Connect buttons
		self.ui.startButton.clicked.connect(self.startServer)
		self.ui.stopButton.clicked.connect(self.stopServer)
		self.stateChanged.connect(self.ui.statusValue.setText)

		self.server.dataOut.connect(self.calculateNextCommand)
		self.server.serverRunning.connect(self.ui.statusValue.setText)

		self.serverState = "Stopped"
		self.stateChanged.emit(self.serverState)

	def startServer(self):
		self.serverState = "Started"
		self.stateChanged.emit(self.serverState)
		if not self.server.listen(QHostAddress("0.0.0.0"), port_num):
			QMessageBox.critical(self, "Pac-Man server", "Failed to start server")
			self.close()
			return

	def stopServer(self):
		self.serverState = "Stopped"
		self.stateChanged.emit(self.serverState)
		self.server.closeServer()

	"""
	def handleClient(self):
		for thread in self.server.client_list:
			if worker.guiDisplay == False:
				self.server.dataOut.connect(self.calculateNextCommand)
				worker.guiDisplay = True
			else:  # if already running, do nothing
				pass
	"""

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
