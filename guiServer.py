import sys
import socket
import threading
import binascii
from enum import Enum
from random import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QLabel
from PyQt5.QtNetwork import QTcpServer, QTcpSocket, QAbstractSocket, QHostAddress
from PyQt5.QtCore import QObject, QThread, QReadWriteLock, QDataStream, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPixmap
from ui_mainwindow import Ui_MainWindow

LOCALTESTING = False

class Command(Enum):
	FORWARD = 0
	STOP_LEFT_FORWARD = 1
	STOP_RIGHT_FORWARD = 2
	ADJUST_LEFT = 3
	ADJUST_RIGHT = 4
	STOP = 5

class Values:
	front = None
	left = None
	right = None
	irState = None
	lfState = None
	xPos = None
	yPos = None
	heading = None
	prevState = None


class Worker(QObject):

	sendData = pyqtSignal(bytes, str)

	def __init__(self, socketId):
		super().__init__()
		self.socketId = socketId
		self.running = True
		self.socket = QTcpSocket(self)
		self.socket.setReadBufferSize(8)

	def run(self):
		if not self.socket.setSocketDescriptor(self.socketId):  # initializes socket, puts into connected state
			self.emit(SIGNAL("error(int)"), self.socket.error())
			return
		self.socket.readyRead.connect(self.read)
		self.socket.disconnected.connect(self.stopWorker)

	def read(self):
		if self.running and self.socket.state() == QAbstractSocket.ConnectedState:
			address = QHostAddress(self.socket.peerAddress()).toString()
			self.setObjectName(address)
			data = bytes(8)
			stream = QDataStream(self.socket)
			stream.setVersion(QDataStream.Qt_5_3)
			if self.socket.bytesAvailable() >= 8:
				data = stream.readRawData(8)
				self.sendData.emit(data, address)

	@pyqtSlot(Command)
	def send(self, command): # connect this slot to a signal in the main thread
		header = b"AA"
		footer = b"FF"
		value = str(command.value).rjust(2, '0').encode()
		data = binascii.unhexlify(header + value + footer)
		self.socket.write(data)
		if command == Command.STOP:
			self.socket.disconnectFromHost()

	def stopWorker(self):
		self.running = False


class ThreadedServer(QTcpServer):
	dataOut = pyqtSignal(bytes, str)
	serverRunning = pyqtSignal(str)
	testSend = pyqtSignal(Command)

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
		self.testSend.emit(Command.FORWARD)
		self.serverRunning.emit("Running")

	def newData(self, data, ip):
		self.dataOut.emit(data, ip)

	def closeServer(self):
		for (thread, worker) in self.client_list:
			self.testSend.emit(Command.STOP)
			worker.stopWorker()
		self.close()

	def passCommand(self, command, name):
		for (thread, worker) in self.client_list:
			if worker.objectName() == name:
				self.testSend.emit(command)
			else:
				pass

class MyWindow(QMainWindow):
	stateChanged = pyqtSignal(str)
	sendCommand = pyqtSignal(Command, str)

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
		self.irImage0 = QPixmap("/home/pi/Desktop/embeddedserver/qtfiles/Images/irstateinit.png")
		self.irImage1 = QPixmap("/home/pi/Desktop/embeddedserver/qtfiles/Images/irstate1.png")
		self.irImage2 = QPixmap("/home/pi/Desktop/embeddedserver/qtfiles/Images/irstate2.png")
		self.irImage3 = QPixmap("/home/pi/Desktop/embeddedserver/qtfiles/Images/irstate3.png")
		self.irImage4 = QPixmap("/home/pi/Desktop/embeddedserver/qtfiles/Images/irstate4.png")
		self.irImage5 = QPixmap("/home/pi/Desktop/embeddedserver/qtfiles/Images/irstate5.png")
		self.irImage6 = QPixmap("/home/pi/Desktop/embeddedserver/qtfiles/Images/irstate6.png")
		self.irImage7 = QPixmap("/home/pi/Desktop/embeddedserver/qtfiles/Images/irstate7.png")
		self.irImage8 = QPixmap("/home/pi/Desktop/embeddedserver/qtfiles/Images/irstate8.png")
		self.lfImage0 = QPixmap("/home/pi/Desktop/embeddedserver/qtfiles/Images/lfstate0.png")
		self.lfImage1 = QPixmap("/home/pi/Desktop/embeddedserver/qtfiles/Images/lfstate1.png")
		self.lfImage2 = QPixmap("/home/pi/Desktop/embeddedserver/qtfiles/Images/lfstate2.png")
		self.lfImage3 = QPixmap("/home/pi/Desktop/embeddedserver/qtfiles/Images/lfstate3.png")
		self.lfImage4 = QPixmap("/home/pi/Desktop/embeddedserver/qtfiles/Images/lfstate4.png")
		self.irPixmap = QPixmap()
		self.lfPixmap = QPixmap()
		self.listOfAddresses = []
		self.whichRover = 0
		self.pacman = Values()
		self.ghost1 = Values()
		self.ghost2 = Values()

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
		self.sendCommand.connect(self.server.passCommand)

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
		output = binascii.hexlify(data)
		header, source, values, footer = output[:2], int(output[2:4], 16), output[4:14], output[14:]

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
			self.updateValues()
			self.newCommand()
			self.drawImage()
			self.displaySensorValues(self.rover)
		#elif source == 1:  # encoder
			#self.x, self.y, self.heading, self.previous, dontcare = values[:2], values[2:4], values[4:6], values[6:8], values[8:10]
			#self.updateValues()
			#self.newCommand()
			#self.displayEncoderValues(self.rover)

		# check footer

	def updateValues(self):
		if self.rover == "pacman":
			self.pacman.irState = self.irState
			#self.pacman.prevState = self.previous
		elif self.rover == "ghost1":
			self.ghost1.irState = self.irState
			#self.ghost1.prevState = self.previous
		elif self.rover == "ghost2":
			self.ghost2.irState = self.irState
			#self.ghost2.prevState = self.previous

	def newCommand(self):
		if self.rover == "pacman":
                        if self.pacman.irState == "01":
                                pass
                        if self.pacman.irState == "02":
                                commands = [Command.FORWARD, Command.STOP_LEFT_FORWARD, Command.STOP_RIGHT_FORWARD]
                                if self.pacman.prevState == "01" or self.pacman.prevState == "00":
                                        x = randint(0, 2)
                                        choice = commands[x]
                                        self.sendCommand.emit(choice)
                        if self.pacman.irState == "03":
                                commands = [Command.STOP_LEFT_FORWARD, Command.STOP_RIGHT_FORWARD]
                                if self.pacman.prevState == "01" or self.pacman.prevState == "00":
                                        x = randint(0, 1)
                                        choice = commands[x]
                                        self.sendCommand.emit(choice)
                        if self.pacman.irState == "04":
                                if self.pacman.prevState == "01" or self.pacman.prevState == "00":
                                        self.sendCommand.emit(Command.STOP_LEFT_FORWARD)
                        if self.pacman.irState == "05":
                                if self.pacman.prevState == "01" or self.pacman.prevState == "00":
                                        self.sendCommand.emit(Command.STOP_RIGHT_FORWARD)
                        if self.pacman.irState == "06":
                                commands = [Command.FORWARD, Command.STOP_LEFT_FORWARD]
                                if self.pacman.prevState == "01" or self.pacman.prevState == "00":
                                        x = randint(0, 1)
                                        choice = commands[x]
                                        self.sendCommand.emit(choice)
                        if self.pacman.irState == "07":
                                commands = [Command.FORWARD, Command.STOP_RIGHT_FORWARD]
                                if self.pacman.prevState == "01" or self.pacman.prevState == "00":
                                        x = randint(0, 1)
                                        choice = commands[x]
                                        self.sendCommand.emit(choice)
                        self.pacman.prevState = self.pacman.irState

		if self.rover == "ghost1":
			if self.ghost1.irState == 7:
				if self.ghost1.prevState == 0 or self.ghost1.prevState == 1:
					self.sendCommand.emit(Command.FORWARD)
			elif self.ghost1.irState == 5:
				self.sendCommand.emit(Command.STOP)
			self.ghost1.prevState = self.ghost1.irState


	def drawImage(self):
		if self.irState == "00":
			self.irPixmap = self.irImage0
		elif self.irState == "01":
			self.irPixmap = self.irImage1
		elif self.irState == "02":
			self.irPixmap = self.irImage2
		elif self.irState == "03":
			self.irPixmap = self.irImage3
		elif self.irState == "04":
			self.irPixmap = self.irImage4
		elif self.irState == "05":
			self.irPixmap = self.irImage5
		elif self.irState == "06":
			self.irPixmap = self.irImage6
		elif self.irState == "07":
			self.irPixmap = self.irImage7
		elif self.irState == "08":
			self.irPixmap = self.irImage8

		if self.lfState == "00":
			self.lfPixmap = self.lfImage0
		elif self.lfState == "01":
			self.lfPixmap = self.lfImage1
		elif self.lfState == "02":
			self.lfPixmap = self.lfImage2
		elif self.lfState == "03":
			self.lfPixmap = self.lfImage3
		elif self.lfState == "04":
			self.lfPixmap = self.lfImage4


	def displaySensorValues(self, rover):
		if rover == "pacman":
			self.ui.ipValue.setText(self.ip)
			self.ui.forwardValue.setText(self.front)
			self.ui.leftValue.setText(self.left)
			self.ui.rightValue.setText(self.right)
			self.ui.irStatusImage.setPixmap(self.irPixmap)
			self.ui.lfStatusImage.setPixmap(self.lfPixmap)
		elif rover == "ghost1":
			self.ui.ipValue_2.setText(self.ip)
			self.ui.forwardValue_2.setText(self.front)
			self.ui.leftValue_2.setText(self.left)
			self.ui.rightValue_2.setText(self.right)
			self.ui.irStatusImage_2.setPixmap(self.irPixmap)
			self.ui.lfStatusImage_2.setPixmap(self.lfPixmap)
		elif rover == "ghost2":
			self.ui.ipValue_3.setText(self.ip)
			self.ui.forwardValue_3.setText(self.front)
			self.ui.leftValue_3.setText(self.left)
			self.ui.rightValue_3.setText(self.right)
			self.ui.irStatusImage_3.setPixmap(self.irPixmap)
			self.ui.lfStatusImage_3.setPixmap(self.lfPixmap)

	def displayEncoderValues(self, rover):
		if rover == "pacman":
			self.ui.ipValue.setText(self.ip)
			self.ui.xValue.setText(self.x)
			self.ui.yValue.setText(self.y)
			self.ui.headingValue.setText(self.heading)
			self.ui.commandValue.setText(self.previous)
		elif rover == "ghost1":
			self.ui.ipValue_2.setText(self.ip)
			self.ui.xValue_2.setText(self.x)
			self.ui.yValue_2.setText(self.y)
			self.ui.headingValue_2.setText(self.heading)
			self.ui.commandValue_2.setText(self.previous)
		elif rover == "ghost2":
			self.ui.ipValue_3.setText(self.ip)
			self.ui.xValue_3.setText(self.x)
			self.ui.yValue_3.setText(self.y)
			self.ui.headingValue_3.setText(self.heading)
			self.ui.commandValue_3.setText(self.previous)


if __name__ == '__main__':
	port_num = 2000
	app = QApplication(sys.argv)
	window = MyWindow()

	window.show()
	sys.exit(app.exec_())
