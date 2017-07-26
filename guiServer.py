import sys
import socket
import threading
from enum import Enum
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QLabel
from PyQt5.QtNetwork import QTcpServer, QTcpSocket, QAbstractSocket, QHostAddress
from PyQt5.QtCore import QObject, QThread, QReadWriteLock, QDataStream, pyqtSignal
from PyQt5.QtGui import QPixmap
from ui_mainwindow import Ui_MainWindow

LOCALTESTING = True


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
				stream.writeRawData(outputData)
				self.sendData.emit(data, address)

	def send(self): # connect this slot to a signal in the main thread
		data = b"FF00AA"
		self.socket.write(data)

	def stopWorker(self):
		self.running = False


class ThreadedServer(QTcpServer):
	dataOut = pyqtSignal(bytes, str)
	serverRunning = pyqtSignal(str)
	testSend = pyqtSignal()

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
		self.testSend.connect(worker.send)
		self.serverRunning.emit("Running")# ({})".format(len(self.client_list)))
		# Direct function calls to worker objects occur on main thread
		# To avoid this, signal the worker slots only from queued connection

	def newData(self, data, ip):
		self.dataOut.emit(data, ip)

	def closeServer(self):
		for (thread, worker) in self.client_list:
			self.testSend.emit()
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
		self.irImage0 = QPixmap("C:/Users/Elliot/Documents/Embedded/embeddedserver/qtfiles/images/irstateinit.png")
		self.irImage1 = QPixmap("C:/Users/Elliot/Documents/Embedded/embeddedserver/qtfiles/images/irstate1.png")
		self.irImage2 = QPixmap("C:/Users/Elliot/Documents/Embedded/embeddedserver/qtfiles/images/irstate2.png")
		self.irImage3 = QPixmap("C:/Users/Elliot/Documents/Embedded/embeddedserver/qtfiles/images/irstate3.png")
		self.irImage4 = QPixmap("C:/Users/Elliot/Documents/Embedded/embeddedserver/qtfiles/images/irstate4.png")
		self.irImage5 = QPixmap("C:/Users/Elliot/Documents/Embedded/embeddedserver/qtfiles/images/irstate5.png")
		self.irImage6 = QPixmap("C:/Users/Elliot/Documents/Embedded/embeddedserver/qtfiles/images/irstate6.png")
		self.irImage7 = QPixmap("C:/Users/Elliot/Documents/Embedded/embeddedserver/qtfiles/images/irstate7.png")
		self.irImage8 = QPixmap("C:/Users/Elliot/Documents/Embedded/embeddedserver/qtfiles/images/irstate8.png")
		self.pixmap = QPixmap()
		self.listOfAddresses = []
		self.whichRover = 0

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
		global LOCALTESTING
		# data = b'\x0f\x12\x14\x05\x04'
		output = data.hex()
		# output = 0F002005050000F0 as a string from localhost
		# output = aa000f12140504ff as a string from rover
		header, source, values, footer = output[:2], int(output[2:4], 16), output[4:14], output[14:]
		# values = 2005050000 as a string from localhost
		# values = 0f12140504 as a string from rover
		# should = 1518200504

		if LOCALTESTING:
			if address in self.listOfAddresses:
				self.whichRover = self.listOfAddresses.index(address)
			else:
				self.listOfAddresses.append(address)

			if self.whichRover == 0:
				self.rover = "pacman"
			elif self.whichRover == 1:
				self.rover = "ghost1"
			elif self.whichRover == 2:
				self.rover = "ghost2"
			else:
				self.rover = "pacman"

		else:
			newVal = str(int(values[:2], 16)).rjust(2, '0')
			newVal2 = str(int(values[2:4], 16)).rjust(2, '0')
			newVal3 = str(int(values[4:6], 16)).rjust(2, '0')
			newVal4 = str(int(values[6:8], 16)).rjust(2, '0')
			newVal5 = str(int(values[8:10], 16)).rjust(2, '0')

			values = ''.join((newVal, newVal2, newVal3, newVal4, newVal5))

			if "103" in address:
				self.rover = "pacman"
			elif "104" in address:
				self.rover = "ghost1"
			elif "105" in address:
				self.rover = "ghost2"
			else:
				self.rover = "pacman"

		self.ip = address

		# check header

		if source == 0:  # sensors
			self.front, self.left, self.right, self.irState, self.lfState = values[:2], values[2:4], values[4:6], values[6:8], values[8:10]
			self.convertLFState()
			self.drawImage()
			self.displaySensorValues(self.rover, self.pixmap)
		elif source == 1:  # encoder
			self.x, self.y, self.heading, self.previous, dontcare = values[:2], values[2:4], values[4:6], values[6:8], values[8:10]
			self.displayEncoderValues(self.rover)

		# check footer

	def drawImage(self):
		if self.irState == "00":
			self.pixmap = self.irImage0
		elif self.irState == "01":
			self.pixmap = self.irImage1
		elif self.irState == "02":
			self.pixmap = self.irImage2
		elif self.irState == "03":
			self.pixmap = self.irImage3
		elif self.irState == "04":
			self.pixmap = self.irImage4
		elif self.irState == "05":
			self.pixmap = self.irImage5
		elif self.irState == "06":
			self.pixmap = self.irImage6
		elif self.irState == "07":
			self.pixmap = self.irImage7
		elif self.irState == "08":
			self.pixmap = self.irImage8

	def convertLFState(self):
		if self.lfState == "00":
			self.lfState = "ON PATH"
		elif self.lfState == "01":
			self.lfState = "SKEWED LEFT"
		elif self.lfState == "02":
			self.lfState = "SKEWED RIGHT"
		elif self.lfState == "03":
			self.lfState = "OFF PATH"
		elif self.lfState == "04":
			self.lfState = "INTERSECTION"


	def displaySensorValues(self, rover, pixmap):
		if rover == "pacman":
			self.ui.ipValue.setText(self.ip)
			self.ui.forwardValue.setText(self.front)
			self.ui.leftValue.setText(self.left)
			self.ui.rightValue.setText(self.right)
			self.ui.lineValue.setText(self.lfState)
			self.ui.irStatusImage.setPixmap(self.pixmap)
		elif rover == "ghost1":
			self.ui.ipValue_2.setText(self.ip)
			self.ui.forwardValue_2.setText(self.front)
			self.ui.leftValue_2.setText(self.left)
			self.ui.rightValue_2.setText(self.right)
			self.ui.lineValue_2.setText(self.lfState)
			self.ui.irStatusImage_2.setPixmap(self.pixmap)
		elif rover == "ghost2":
			self.ui.ipValue_3.setText(self.ip)
			self.ui.forwardValue_3.setText(self.front)
			self.ui.leftValue_3.setText(self.left)
			self.ui.rightValue_3.setText(self.right)
			self.ui.lineValue_3.setText(self.lfState)
			self.ui.irStatusImage_3.setPixmap(self.pixmap)

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
