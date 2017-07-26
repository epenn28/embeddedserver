import sys
import socket
import threading
from enum import Enum
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QLabel
from PyQt5.QtNetwork import QTcpServer, QTcpSocket, QAbstractSocket, QHostAddress
from PyQt5.QtCore import QObject, QThread, QReadWriteLock, QDataStream, pyqtSignal
from PyQt5.QtGui import QPixmap
from ui_mainwindow import Ui_MainWindow


class Worker(QObject):

	sendData = pyqtSignal(bytes, str)

	def __init__(self, socketId):
		super().__init__()
		self.socketId = socketId
		self.running = True
		self.socket = QTcpSocket(self)

	def run(self):
		if not self.socket.setSocketDescriptor(self.socketId):  # initializes socket, puts into connected state
			self.emit(SIGNAL("error(int)"), self.socket.error())
			return
		self.socket.readyRead.connect(self.read)
		self.socket.disconnected.connect(self.stopWorker)

	def read(self):
		if self.running:
			address = QHostAddress(self.socket.peerAddress()).toString() + ":" + str(self.socket.peerPort())
			data = bytes(8)
			stream = QDataStream(self.socket)
			stream.setVersion(QDataStream.Qt_5_9)
			if self.socket.bytesAvailable() >= 8:
				data = stream.readRawData(8)
				outputData = b"AA00FF" # outputting data like this works- handle algorithm at this point?
				self.socket.write(outputData)
				self.sendData.emit(data, address)

	def send(self): # must be called from worker object's thread, not within worker itself
		data = b"AA00FF"
		self.socket.write(data)

	def stopWorker(self):
		self.running = False


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
		# Direct function calls to worker objects occur on main thread
		# To avoid this, signal the worker slots only from queued connection

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
		self.irImage = QPixmap()

		super().__init__(parent)
		self.serverState = "Init"
		self.stateChanged.emit(self.serverState)
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		self.ui.stopButton.setEnabled(False)

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
		self.ui.stopButton.setEnabled(True)
		self.ui.startButton.setEnabled(False)
		self.serverState = "Started"
		self.stateChanged.emit(self.serverState)
		if not self.server.listen(QHostAddress("0.0.0.0"), port_num):
			QMessageBox.critical(self, "Pac-Man server", "Failed to start server")
			self.close()
			return

	def stopServer(self):
		self.ui.stopButton.setEnabled(False)
		self.ui.startButton.setEnabled(True)
		self.serverState = "Stopped"
		self.stateChanged.emit(self.serverState)
		self.server.closeServer()

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
			self.drawImage()
			self.displaySensorValues(self.rover)
		elif source == 1:  # encoder
			self.x, self.y, self.heading, self.previous, dontcare = values[:2], values[2:4], values[4:6], values[6:8], values[8:10]
			self.displayEncoderValues(self.rover)

		# check footer

	def drawImage(self):
		if self.irState == "00":
			self.irImage.load("C:/Users/Elliot/Documents/Embedded/embeddedserver/qtfiles/images/irstate0.png")
		elif self.irState == "01":
			self.irImage.load("C:/Users/Elliot/Documents/Embedded/embeddedserver/qtfiles/images/irstate1.png")
		elif self.irState == "02":
			self.irImage.load("C:/Users/Elliot/Documents/Embedded/embeddedserver/qtfiles/images/irstate2.png")
		elif self.irState == "03":
			self.irImage.load("C:/Users/Elliot/Documents/Embedded/embeddedserver/qtfiles/images/irstate3.png")
		elif self.irState == "04":
			self.irImage.load("C:/Users/Elliot/Documents/Embedded/embeddedserver/qtfiles/images/irstate4.png")
		elif self.irState == "05":
			self.irImage.load("C:/Users/Elliot/Documents/Embedded/embeddedserver/qtfiles/images/irstate5.png")
		elif self.irState == "06":
			self.irImage.load("C:/Users/Elliot/Documents/Embedded/embeddedserver/qtfiles/images/irstate6.png")
		elif self.irState == "07":
			self.irImage.load("C:/Users/Elliot/Documents/Embedded/embeddedserver/qtfiles/images/irstate7.png")


	def displaySensorValues(self, rover):
		if rover == "pacman":
			self.ui.ipValue.setText(self.ip)
			self.ui.forwardValue.setText(self.front)
			self.ui.leftValue.setText(self.left)
			self.ui.rightValue.setText(self.right)
			self.ui.lineValue.setText(self.lfState)
			self.ui.irStatusImage.setPixmap(self.irImage)
		elif rover == "ghost1":
			self.ui.ipValue_2.setText(self.ip)
			self.ui.forwardValue_2.setText(self.front)
			self.ui.leftValue_2.setText(self.left)
			self.ui.rightValue_2.setText(self.right)
			self.ui.lineValue_2.setText(self.lfState)
			self.ui.irStatusImage_2.setPixmap(self.irImage)
		elif rover == "ghost2":
			self.ui.ipValue_3.setText(self.ip)
			self.ui.forwardValue_3.setText(self.front)
			self.ui.leftValue_3.setText(self.left)
			self.ui.rightValue_3.setText(self.right)
			self.ui.lineValue_3.setText(self.lfState)
			self.ui.irStatusImage_3.setPixmap(self.irImage)

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
