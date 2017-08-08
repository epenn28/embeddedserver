import sys
import socket
import threading
import binascii
import time
from enum import Enum
from random import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QLabel, QPushButton
from PyQt5.QtNetwork import QTcpServer, QTcpSocket, QAbstractSocket, QHostAddress
from PyQt5.QtCore import QObject, QThread, QReadWriteLock, QDataStream, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPixmap
from ui_mainwindow import Ui_PacMan

LOCALTESTING = False

class Command(Enum):
	FORWARD = 0
	STOP_LEFT_FORWARD = 1
	STOP_RIGHT_FORWARD = 2
	ADJUST_LEFT = 3
	ADJUST_RIGHT = 4
	STOP = 5
	MANUAL_FORWARD = 6
	MANUAL_ADJUST_RIGHT = 7
	MANUAL_ADJUST_LEFT = 8
	MANUAL_LEFT = 9
	MANUAL_RIGHT = 10
	PAUSE = 11

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

	@pyqtSlot(Command, str)
	def send(self, command, name): # connect this slot to a signal in the main thread
		if self.objectName() == name or name == "all":
			header = b"AA"
			footer = b"FF"
			if command == Command.PAUSE:
				value = str(5).rjust(2, '0').encode()
			elif command == Command.MANUAL_RIGHT:
				value = "A".rjust(2, '0').encode()
			else:
				value = str(command.value).rjust(2, '0').encode()
			data = binascii.unhexlify(header + value + footer)
			self.socket.write(data)
			if command == Command.STOP:
				self.socket.disconnectFromHost()
		else:
			pass

	def stopWorker(self):
		self.running = False


class ThreadedServer(QTcpServer):
	dataOut = pyqtSignal(bytes, str)
	serverRunning = pyqtSignal(str)
	testSend = pyqtSignal(Command, str)

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
		self.serverRunning.emit("Running")

	def newData(self, data, ip):
		self.dataOut.emit(data, ip)

	def closeServer(self):
		for (thread, worker) in self.client_list:
			self.testSend.emit(Command.STOP, "all")
			worker.stopWorker()
		self.close()

	def passCommand(self, command, name):
		self.testSend.emit(command, name)

class MyWindow(QMainWindow):
	stateChanged = pyqtSignal(str)
	sendCommand = pyqtSignal(Command, str)
	scoreChanged = pyqtSignal(int)

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
		self.pacman.xPos = 4
		self.pacman.yPos = 4
		self.pacman.heading = "north"
		self.ghost1.xPos = 0
		self.ghost1.yPos = 2
		self.ghost1.heading = "north"
		self.ghost2.xPos = 8
		self.ghost2.yPos = 2
		self.ghost2.heading = "south"
		self.manual = True
		self.score = 0

		super().__init__(parent)
		self.serverState = "Init"
		self.stateChanged.emit(self.serverState)
		self.ui = Ui_PacMan()
		self.ui.setupUi(self)
		self.ui.stopButton.setEnabled(False)
		#self.ui.automaticButton.setEnabled(False)
		self.buttons = self.ui.manualTab.findChildren(QPushButton)
		for button in self.buttons:
			thing = button.objectName()
			test = getattr(self.ui, thing)
			test.clicked.connect(self.manualCommand)
			test.setEnabled(False)

		# Set up server
		self.server = ThreadedServer(self)

		# Connect buttons
		self.sendCommand.connect(self.server.passCommand)
		self.ui.startButton.clicked.connect(self.startServer)
		self.ui.stopButton.clicked.connect(self.stopServer)
		self.ui.automaticButton.clicked.connect(self.autoMode)
		self.ui.overrideButton.clicked.connect(self.manualMode)
		self.stateChanged.connect(self.ui.statusValue.setText)

		self.server.dataOut.connect(self.calculateNextCommand)
		self.server.serverRunning.connect(self.ui.statusValue.setText)
		self.scoreChanged.connect(self.ui.scoreValue.setText)

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

	def autoMode(self):
		self.ui.overrideButton.setEnabled(True)
		self.ui.automaticButton.setEnabled(False)
		self.manual = False
		self.sendCommand.emit(Command.FORWARD, "all")
		for button in self.buttons:
			thing = button.objectName()
			test = getattr(self.ui, thing)
			test.setEnabled(False)

	def manualMode(self):
		self.ui.overrideButton.setEnabled(False)
		self.ui.automaticButton.setEnabled(True)
		self.manual = True
		self.sendCommand.emit(Command.PAUSE, "all")
		for button in self.buttons:
			thing = button.objectName()
			test = getattr(self.ui, thing)
			test.setEnabled(True)

	def manualCommand(self):
		pacIP = "192.168.1.103"
		ghost1IP = "192.168.1.104"
		ghost2IP = "192.168.1.105"
		whichButton = self.sender().objectName()
		if whichButton == "pacUpButton":
			self.sendCommand.emit(Command.MANUAL_FORWARD, pacIP)
		elif whichButton == "pacLeftButton":
			self.sendCommand.emit(Command.MANUAL_LEFT, pacIP)
		elif whichButton == "pacRightButton":
			self.sendCommand.emit(Command.MANUAL_RIGHT, pacIP)
		elif whichButton == "pacAdjustLeftButton":
			self.sendCommand.emit(Command.MANUAL_ADJUST_LEFT, pacIP)
		elif whichButton == "pacAdjustRightButton":
			self.sendCommand.emit(Command.MANUAL_ADJUST_RIGHT, pacIP)
		elif whichButton == "ghost1UpButton":
			self.sendCommand.emit(Command.MANUAL_FORWARD, ghost1IP)
		elif whichButton == "ghost1LeftButton":
			self.sendCommand.emit(Command.MANUAL_LEFT, ghost1IP)
		elif whichButton == "ghost1RightButton":
			self.sendCommand.emit(Command.MANUAL_RIGHT, ghost1IP)
		elif whichButton == "ghost1AdjustLeftButton":
			self.sendCommand.emit(Command.MANUAL_ADJUST_LEFT, ghost1IP)
		elif whichButton == "ghost1AdjustRightButton":
			self.sendCommand.emit(Command.MANUAL_ADJUST_RIGHT, ghost1IP)
		elif whichButton == "ghost2UpButton":
			self.sendCommand.emit(Command.MANUAL_FORWARD, ghost2IP)
		elif whichButton == "ghost2LeftButton":
			self.sendCommand.emit(Command.MANUAL_LEFT, ghost2IP)
		elif whichButton == "ghost2RightButton":
			self.sendCommand.emit(Command.MANUAL_RIGHT, ghost2IP)
		elif whichButton == "ghost2AdjustLeftButton":
			self.sendCommand.emit(Command.MANUAL_ADJUST_LEFT, ghost2IP)
		elif whichButton == "ghost2AdjustRightButton":
			self.sendCommand.emit(Command.MANUAL_ADJUST_RIGHT, ghost2IP)

		time.sleep(.5)
		self.sendCommand.emit(Command.PAUSE, "all")

		self.pacman.prevState = self.pacman.irState
		self.ghost1.prevState = self.ghost1.irState
		self.ghost2.prevState = self.ghost2.irState


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

	def decideCommandAI(self, x):
		if self.ghost1.xPos == self.pacman.xPos and self.ghost2.xPos == self.pacman.xPos:
			if self.ghost1.yPos == self.pacman.yPos or self.ghost2.yPos == self.pacman.yPos:
				self.sendCommand.emit(Command.PAUSE, "all")
				#return False
			elif self.ghost1.yPos > self.pacman.yPos and self.ghost2.yPos > self.pacman.yPos:
				#move south
				if self.pacman.heading == "north":
					x = 1
				elif self.pacman.heading == "south":
					x = 0
				elif self.pacman.heading == "east":
					x = 1
				elif self.pacman.heading == "west":
					x = 1
			elif self.ghost1.yPos > self.pacman.yPos and self.ghost2.yPos < self.pacman.yPos:
				#move east or west
				if self.pacman.heading == "north":
					x = 1
				elif self.pacman.heading == "south":
					x = 1
				elif self.pacman.heading == "east":
					x = 0
				elif self.pacman.heading == "west":
					x = 0
			elif self.ghost1.yPos < self.pacman.yPos and self.ghost2.yPos < self.pacman.yPos:
				#move north
				if self.pacman.heading == "north":
					x = 0
				elif self.pacman.heading == "south":
					x = 1
				elif self.pacman.heading == "east":
					x = 1
				elif self.pacman.heading == "west":
					x = 1
			elif self.ghost1.yPos < self.pacman.yPos and self.ghost2.yPos > self.pacman.yPos:
				#move east or west
				if self.pacman.heading == "north":
					x = 1
				elif self.pacman.heading == "south":
					x = 1
				elif self.pacman.heading == "east":
					x = 0
				elif self.pacman.heading == "west":
					x = 0
		elif self.ghost1.xPos == self.pacman.xPos and self.ghost2.xPos > self.pacman.xPos:
			if self.ghost1.yPos == self.pacman.yPos:
				self.sendCommand.emit(Command.PAUSE, "all")
				#return False
			#move west
			elif self.pacman.heading == "north":
				x = 1
			elif self.pacman.heading == "south":
				x = 1
			elif self.pacman.heading == "east":
				if self.pacman.irState == "02":
					x = 2
				else:
					x = 1
			elif self.pacman.heading == "west":
				x = 0
		elif self.ghost1.xPos == self.pacman.xPos and self.ghost2.xPos < self.pacman.xPos:
			if self.ghost1.yPos == self.pacman.yPos:
				self.sendCommand.emit(Command.PAUSE, "all")
				#return False
			#move east
			elif self.pacman.heading == "north":
				x = 1
			elif self.pacman.heading == "south":
				x = 1
			elif self.pacman.heading == "east":
				x = 0
			elif self.pacman.heading == "west":
				x = 1
		elif self.ghost1.xPos > self.pacman.xPos and self.ghost2.xPos == self.pacman.xPos:
			if self.ghost2.yPos == self.pacman.yPos:
				self.sendCommand.emit(Command.PAUSE, "all")
				#return False
			#move west
			elif self.pacman.heading == "north":
				x = 1
			elif self.pacman.heading == "south":
				x = 1
			elif self.pacman.heading == "east":
				x = 1
			elif self.pacman.heading == "west":
				x = 0
		elif self.ghost1.xPos < self.pacman.xPos and self.ghost2.xPos == self.pacman.xPos:
			if self.ghost2.yPos == self.pacman.yPos:
				self.sendCommand.emit(Command.PAUSE, "all")
				#return False
			#move east
			elif self.pacman.heading == "north":
				x = 1
			elif self.pacman.heading == "south":
				x = 1
			elif self.pacman.heading == "east":
				x = 0
			elif self.pacman.heading == "west":
				x = 1
		elif self.ghost1.xPos > self.pacman.xPos and self.ghost2.xPos > self.pacman.xPos:
			#move west
			if self.pacman.heading == "north":
				x = 1
			elif self.pacman.heading == "south":
				x = 1
			elif self.pacman.heading == "east":
				x = 1
			elif self.pacman.heading == "west":
				x = 0
		elif self.ghost1.xPos < self.pacman.xPos and self.ghost2.xPos < self.pacman.xPos:
			#move east
			if self.pacman.heading == "north":
				x = 1
			elif self.pacman.heading == "south":
				x = 1
			elif self.pacman.heading == "east":
				x = 0
			elif self.pacman.heading == "west":
				x = 1
		elif self.ghost1.xPos < self.pacman.xPos and self.ghost2.xPos > self.pacman.xPos:
			if self.ghost1.yPos == self.pacman.yPos and self.ghost2.yPos == self.pacman.yPos:
				#move north or south
				if self.pacman.heading == "north":
					x = 0
				elif self.pacman.heading == "south":
					x = 0
				elif self.pacman.heading == "east":
					x = 1
				elif self.pacman.heading == "west":
					x = 1
			elif self.ghost1.yPos == self.pacman.yPos and self.ghost2.yPos > self.pacman.yPos:
				#move south
				if self.pacman.heading == "north":
					x = 1
				elif self.pacman.heading == "south":
					x = 0
				elif self.pacman.heading == "east":
					x = 1
				elif self.pacman.heading == "west":
					x = 1
			elif self.ghost1.yPos == self.pacman.yPos and self.ghost2.yPos < self.pacman.yPos:
				#move north
				if self.pacman.heading == "north":
					x = 0
				elif self.pacman.heading == "south":
					x = 1
				elif self.pacman.heading == "east":
					x = 1
				elif self.pacman.heading == "west":
					x = 1
			elif self.ghost1.yPos > self.pacman.yPos and self.ghost2.yPos == self.pacman.yPos:
				#move south
				if self.pacman.heading == "north":
					x = 1
				elif self.pacman.heading == "south":
					x = 0
				elif self.pacman.heading == "east":
					x = 1
				elif self.pacman.heading == "west":
					x = 1
			elif self.ghost1.yPos < self.pacman.yPos and self.ghost2.yPos == self.pacman.yPos:
				#move north
				if self.pacman.heading == "north":
					x = 0
				elif self.pacman.heading == "south":
					x = 1
				elif self.pacman.heading == "east":
					x = 1
				elif self.pacman.heading == "west":
					x = 1
			elif self.ghost1.yPos > self.pacman.yPos and self.ghost2.yPos > self.pacman.yPos:
				#move south
				if self.pacman.heading == "north":
					x = 1
				elif self.pacman.heading == "south":
					x = 0
				elif self.pacman.heading == "east":
					x = 1
				elif self.pacman.heading == "west":
					x = 1
			elif self.ghost1.yPos < self.pacman.yPos and self.ghost2.yPos < self.pacman.yPos:
				#move north
				if self.pacman.heading == "north":
					x = 0
				elif self.pacman.heading == "south":
					x = 1
				elif self.pacman.heading == "east":
					x = 1
				elif self.pacman.heading == "west":
					x = 1
			elif self.ghost1.yPos > self.pacman.yPos and self.ghost2.yPos < self.pacman.yPos:
				if (xPos - self.ghost1.xPos) < (self.ghost2.xPos - self.pacman.xPos):
					#move east
					if self.pacman.heading == "north":
						x = 1
					elif self.pacman.heading == "south":
						x = 1
					elif self.pacman.heading == "east":
						x = 0
					elif self.pacman.heading == "west":
						x = 1
				else:
					#move west
					if self.pacman.heading == "north":
						x = 1
					elif self.pacman.heading == "south":
						x = 1
					elif self.pacman.heading == "east":
						x = 1
					elif self.pacman.heading == "west":
						x = 0
		elif self.ghost1.xPos > self.pacman.xPos and self.ghost2.xPos < self.pacman.xPos:
			if self.ghost1.yPos == self.pacman.yPos and self.ghost2.yPos == self.pacman.yPos:
				#move north or south
				if self.pacman.heading == "north":
					x = 0
				elif self.pacman.heading == "south":
					x = 0
				elif self.pacman.heading == "east":
					x = 1
				elif self.pacman.heading == "west":
					x = 1
			elif self.ghost1.yPos == self.pacman.yPos and self.ghost2.yPos > self.pacman.yPos:
				#move south
				if self.pacman.heading == "north":
					x = 1
				elif self.pacman.heading == "south":
					x = 0
				elif self.pacman.heading == "east":
					x = 1
				elif self.pacman.heading == "west":
					x = 1
			elif self.ghost1.yPos == self.pacman.yPos and self.ghost2.yPos < self.pacman.yPos:
				#move north
				if self.pacman.heading == "north":
					x = 0
				elif self.pacman.heading == "south":
					x = 1
				elif self.pacman.heading == "east":
					x = 1
				elif self.pacman.heading == "west":
					x = 1
			elif self.ghost1.yPos > self.pacman.yPos and self.ghost2.yPos == self.pacman.yPos:
				#move south
				if self.pacman.heading == "north":
					x = 1
				elif self.pacman.heading == "south":
					x = 0
				elif self.pacman.heading == "east":
					x = 1
				elif self.pacman.heading == "west":
					x = 1
			elif self.ghost1.yPos < self.pacman.yPos and self.ghost2.yPos == self.pacman.yPos:
				#move north
				if self.pacman.heading == "north":
					x = 0
				elif self.pacman.heading == "south":
					x = 1
				elif self.pacman.heading == "east":
					x = 1
				elif self.pacman.heading == "west":
					x = 1
			elif self.ghost1.yPos > self.pacman.yPos and self.ghost2.yPos > self.pacman.yPos:
				#move south
				if self.pacman.heading == "north":
					x = 1
				elif self.pacman.heading == "south":
					x = 0
				elif self.pacman.heading == "east":
					x = 1
				elif self.pacman.heading == "west":
					x = 1
			elif self.ghost1.yPos < self.pacman.yPos and self.ghost2.yPos < self.pacman.yPos:
				#move north
				if self.pacman.heading == "north":
					x = 0
				elif self.pacman.heading == "south":
					x = 1
				elif self.pacman.heading == "east":
					x = 1
				elif self.pacman.heading == "west":
					x = 1
			elif self.ghost1.yPos > self.pacman.yPos and self.ghost2.yPos < self.pacman.yPos:
				if (self.ghost1.xPos - self.pacman.xPos) < (xPos - self.ghost2.xPos):
					#move west
					if self.pacman.heading == "north":
						x = 1
					elif self.pacman.heading == "south":
						x = 1
					elif self.pacman.heading == "east":
						x = 1
					elif self.pacman.heading == "west":
						x = 0
				else:
					#move east
					if self.pacman.heading == "north":
						x = 1
					elif self.pacman.heading == "south":
						x = 1
					elif self.pacman.heading == "east":
						x = 0
					elif self.pacman.heading == "west":
						x = 1


	def decideCoordinate(self, command):
		if self.rover == "pacman":
			if self.pacman.heading == "north":
				if command == Command.FORWARD:
					#if self.left_distance <= 10 and self.right_distance <= 10:
					#        if self.previous_pacman_state == Pacman_States[0]:
					#                self.pacman.yPos += 1
					self.pacman.yPos += 2
				elif command == Command.STOP_LEFT_FORWARD:
					self.pacman.xPos -= 2
					self.pacman.heading = "west"
				elif command == Command.STOP_RIGHT_FORWARD:
					self.pacman.xPos += 2
					self.pacman.heading = "east"
			elif self.pacman.heading == "south":
				if command == Command.FORWARD:
					#if self.left_distance <= 10 and self.right_distance <= 10:
					#        self.pacman.yPos -= 1
					#        self.pacman.yPos -= 1
					#else:
					self.pacman.yPos -= 2
				elif command == Command.STOP_LEFT_FORWARD:
					self.pacman.xPos += 2
					self.pacman.heading = "east"
				elif command == Command.STOP_RIGHT_FORWARD:
					self.pacman.xPos -= 2
					self.pacman.heading = "west"
			elif self.pacman.heading == "east":
				if command == Command.FORWARD:
					#if self.left_distance <= 10 and self.right_distance <= 10:
					#        self.pacman.xPos += 1
					#        self.pacman.xPos += 1
					#else:
					self.pacman.xPos += 2
				elif command == Command.STOP_LEFT_FORWARD:
					self.pacman.yPos += 2
					self.pacman.heading = "north"
				elif command == Command.STOP_RIGHT_FORWARD:
					self.pacman.yPos -= 2
					self.pacman.heading = "south"
			elif self.pacman.heading == "west":
				if command == Command.FORWARD:
					#if self.left_distance <= 10 and self.right_distance <= 10:
					#        self.pacman.xPos -= 1
					#        self.pacman.xPos -= 1
					#else:
					self.pacman.xPos -= 2
				elif command == Command.STOP_LEFT_FORWARD:
					self.pacman.yPos -= 2
					self.pacman.heading = "south"
				elif command == Command.STOP_RIGHT_FORWARD:
					self.pacman.yPos += 2
					self.pacman.heading = "north"

		elif self.rover == "ghost1":
			if self.ghost1.heading == "north":
				if command == Command.FORWARD:
					#if self.left_distance <= 10 and self.right_distance <= 10:
					#        if self.previous_ghost1_state == ghost1_States[0]:
					#                self.ghost1.yPos += 1
					self.ghost1.yPos += 2
				elif command == Command.STOP_LEFT_FORWARD:
					self.ghost1.xPos -= 2
					self.ghost1.heading = "west"
				elif command == Command.STOP_RIGHT_FORWARD:
					self.ghost1.xPos += 2
					self.ghost1.heading = "east"
			elif self.ghost1.heading == "south":
				if command == Command.FORWARD:
					#if self.left_distance <= 10 and self.right_distance <= 10:
					#        self.ghost1.yPos -= 1
					#        self.ghost1.yPos -= 1
					#else:
					self.ghost1.yPos -= 2
				elif command == Command.STOP_LEFT_FORWARD:
					self.ghost1.xPos += 2
					self.ghost1.heading = "east"
				elif command == Command.STOP_RIGHT_FORWARD:
					self.ghost1.xPos -= 2
					self.ghost1.heading = "west"
			elif self.ghost1.heading == "east":
				if command == Command.FORWARD:
					#if self.left_distance <= 10 and self.right_distance <= 10:
					#        self.ghost1.xPos += 1
					#        self.ghost1.xPos += 1
					#else:
					self.ghost1.xPos += 2
				elif command == Command.STOP_LEFT_FORWARD:
					self.ghost1.yPos += 2
					self.ghost1.heading = "north"
				elif command == Command.STOP_RIGHT_FORWARD:
					self.ghost1.yPos -= 2
					self.ghost1.heading = "south"
			elif self.ghost1.heading == "west":
				if command == Command.FORWARD:
					#if self.left_distance <= 10 and self.right_distance <= 10:
					#        self.ghost1.xPos -= 1
					#        self.ghost1.xPos -= 1
					#else:
					self.ghost1.xPos -= 2
				elif command == Command.STOP_LEFT_FORWARD:
					self.ghost1.yPos -= 2
					self.ghost1.heading = "south"
				elif command == Command.STOP_RIGHT_FORWARD:
					self.ghost1.yPos += 2
					self.ghost1.heading = "north"

		elif self.rover == "ghost2":
			pass


	def newCommand(self):
		pacIP = "192.168.1.103"
		ghost1IP = "192.168.1.104"
		ghost2IP = "192.168.1.105"
		x = 0
		if self.manual:
			return

		if self.rover == "pacman":
			if self.pacman.irState == "01":  # Forward open, left blocked, right blocked
				self.decideCommandAI(x)
			if self.pacman.irState == "02":  # Forward open, left open, right open
				commands = [Command.FORWARD, Command.STOP_LEFT_FORWARD, Command.STOP_RIGHT_FORWARD]
				if self.pacman.prevState == "01" or self.pacman.prevState == "00":
					self.decideCommandAI(x)
					choice = commands[x]
					self.decideCoordinate(choice)
					self.sendCommand.emit(choice, pacIP)
					self.score += 1
			if self.pacman.irState == "03":  # Forward blocked, left open, right open
				commands = [Command.STOP_LEFT_FORWARD, Command.STOP_RIGHT_FORWARD]
				if self.pacman.prevState == "01" or self.pacman.prevState == "00":
					self.decideCommandAI(x)
					choice = commands[x]
					self.decideCoordinate(choice)
					self.sendCommand.emit(choice, pacIP)
					self.score += 1
			if self.pacman.irState == "04":  # Forward blocked, left open, right blocked
				if self.pacman.prevState == "01" or self.pacman.prevState == "00":
					self.decideCommandAI(x)
					self.decideCoordinate(Command.STOP_LEFT_FORWARD)
					self.sendCommand.emit(Command.STOP_LEFT_FORWARD, pacIP)
					self.score += 1
			if self.pacman.irState == "05":  # Forward blocked, left blocked, right open
				if self.pacman.prevState == "01" or self.pacman.prevState == "00":
					self.decideCommandAI(x)
					self.decideCoordinate(Command.STOP_RIGHT_FORWARD)
					self.sendCommand.emit(Command.STOP_RIGHT_FORWARD, pacIP)
					self.score += 1
			if self.pacman.irState == "06":  # Forward open, left open, right blocked
				commands = [Command.FORWARD, Command.STOP_LEFT_FORWARD]
				if self.pacman.prevState == "01" or self.pacman.prevState == "00":
					self.decideCommandAI(x)
					choice = commands[x]
					self.decideCoordinate(choice)
					self.sendCommand.emit(choice, pacIP)
					self.score += 1
			if self.pacman.irState == "07":  # Forward open, left blocked, right open
				commands = [Command.FORWARD, Command.STOP_RIGHT_FORWARD]
				if self.pacman.prevState == "01" or self.pacman.prevState == "00":
					self.decideCommandAI(x)
					choice = commands[x]
					self.decideCoordinate(choice)
					self.sendCommand.emit(choice, pacIP)
					self.score += 1
			self.pacman.prevState = self.pacman.irState
			self.scoreChanged.emit(self.score)

		if self.rover == "ghost1":
			if self.ghost1.irState == "01":  # Forward open, left blocked, right blocked
				self.decideCommandAI(x)
			if self.ghost1.irState == "02":  # Forward open, left open, right open
				commands = [Command.FORWARD, Command.STOP_LEFT_FORWARD, Command.STOP_RIGHT_FORWARD]
				if self.ghost1.prevState == "01" or self.ghost1.prevState == "00":
					self.decideCommandAI(x)
					x = randint(0, 2)
					choice = commands[x]
					self.decideCoordinate(choice)
					self.sendCommand.emit(choice, ghost1IP)
			if self.ghost1.irState == "03":  # Forward blocked, left open, right open
				commands = [Command.STOP_LEFT_FORWARD, Command.STOP_RIGHT_FORWARD]
				if self.ghost1.prevState == "01" or self.ghost1.prevState == "00":
					self.decideCommandAI(x)
					x = randint(0, 1)
					choice = commands[x]
					self.decideCoordinate(choice)
					self.sendCommand.emit(choice, ghost1IP)
			if self.ghost1.irState == "04":  # Forward blocked, left open, right blocked
				if self.ghost1.prevState == "01" or self.ghost1.prevState == "00":
					self.decideCommandAI(x)
					self.decideCoordinate(Command.STOP_LEFT_FORWARD)
					self.sendCommand.emit(Command.STOP_LEFT_FORWARD, ghost1IP)
			if self.ghost1.irState == "05":  # Forward blocked, left blocked, right open
				if self.ghost1.prevState == "01" or self.ghost1.prevState == "00":
					self.decideCommandAI(x)
					self.decideCoordinate(Command.STOP_RIGHT_FORWARD)
					self.sendCommand.emit(Command.STOP_RIGHT_FORWARD, ghost1IP)
			if self.ghost1.irState == "06":  # Forward open, left open, right blocked
				commands = [Command.FORWARD, Command.STOP_LEFT_FORWARD]
				if self.ghost1.prevState == "01" or self.ghost1.prevState == "00":
					self.decideCommandAI(x)
					x = randint(0, 1)
					choice = commands[x]
					self.decideCoordinate(choice)
					self.sendCommand.emit(choice, ghost1IP)
			if self.ghost1.irState == "07":  # Forward open, left blocked, right open
				commands = [Command.FORWARD, Command.STOP_RIGHT_FORWARD]
				if self.ghost1.prevState == "01" or self.ghost1.prevState == "00":
					self.decideCommandAI(x)
					x = randint(0, 1)
					choice = commands[x]
					self.decideCoordinate(choice)
					self.sendCommand.emit(choice, ghost1IP)
			self.ghost1.prevState = self.ghost1.irState

		if self.rover == "ghost2":
			if self.ghost2.irState == "01":  # Forward open, left blocked, right blocked
				self.decideCommandAI(x)
			if self.ghost2.irState == "02":  # Forward open, left open, right open
				commands = [Command.FORWARD, Command.STOP_LEFT_FORWARD, Command.STOP_RIGHT_FORWARD]
				if self.ghost2.prevState == "01" or self.ghost2.prevState == "00":
					self.decideCommandAI(x)
					choice = commands[x]
					self.decideCoordinate(choice)
					self.sendCommand.emit(choice, pacIP)
			if self.ghost2.irState == "03":  # Forward blocked, left open, right open
				commands = [Command.STOP_LEFT_FORWARD, Command.STOP_RIGHT_FORWARD]
				if self.ghost2.prevState == "01" or self.ghost2.prevState == "00":
					self.decideCommandAI(x)
					choice = commands[x]
					self.decideCoordinate(choice)
					self.sendCommand.emit(choice, pacIP)
			if self.ghost2.irState == "04":  # Forward blocked, left open, right blocked
				if self.ghost2.prevState == "01" or self.ghost2.prevState == "00":
					self.decideCommandAI(x)
					self.decideCoordinate(Command.STOP_LEFT_FORWARD)
					self.sendCommand.emit(Command.STOP_LEFT_FORWARD, pacIP)
			if self.ghost2.irState == "05":  # Forward blocked, left blocked, right open
				if self.ghost2.prevState == "01" or self.ghost2.prevState == "00":
					self.decideCommandAI(x)
					self.decideCoordinate(Command.STOP_RIGHT_FORWARD)
					self.sendCommand.emit(Command.STOP_RIGHT_FORWARD, pacIP)
			if self.ghost2.irState == "06":  # Forward open, left open, right blocked
				commands = [Command.FORWARD, Command.STOP_LEFT_FORWARD]
				if self.ghost2.prevState == "01" or self.ghost2.prevState == "00":
					self.decideCommandAI(x)
					choice = commands[x]
					self.decideCoordinate(choice)
					self.sendCommand.emit(choice, pacIP)
			if self.ghost2.irState == "07":  # Forward open, left blocked, right open
				commands = [Command.FORWARD, Command.STOP_RIGHT_FORWARD]
				if self.ghost2.prevState == "01" or self.ghost2.prevState == "00":
					self.decideCommandAI(x)
					choice = commands[x]
					self.decideCoordinate(choice)
					self.sendCommand.emit(choice, pacIP)
			self.ghost2.prevState = self.ghost2.irState


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

			self.x = str(self.pacman.xPos)
			self.y = str(self.pacman.yPos)
			self.heading = str(self.pacman.heading)
			self.previous = str(self.pacman.prevState)

			self.ui.xValue.setText(self.x)
			self.ui.yValue.setText(self.y)
			self.ui.headingValue.setText(self.heading)
			self.ui.commandValue.setText(self.previous)
		elif rover == "ghost1":
			self.ui.ipValue_2.setText(self.ip)
			self.ui.forwardValue_2.setText(self.front)
			self.ui.leftValue_2.setText(self.left)
			self.ui.rightValue_2.setText(self.right)
			self.ui.irStatusImage_2.setPixmap(self.irPixmap)
			self.ui.lfStatusImage_2.setPixmap(self.lfPixmap)

			self.x = str(self.ghost1.xPos)
			self.y = str(self.ghost1.yPos)
			self.heading = str(self.ghost1.heading)
			self.previous = str(self.ghost1.prevState)

			self.ui.xValue_2.setText(self.x)
			self.ui.yValue_2.setText(self.y)
			self.ui.headingValue_2.setText(self.heading)
			self.ui.commandValue_2.setText(self.previous)
		elif rover == "ghost2":
			self.ui.ipValue_3.setText(self.ip)
			self.ui.forwardValue_3.setText(self.front)
			self.ui.leftValue_3.setText(self.left)
			self.ui.rightValue_3.setText(self.right)
			self.ui.irStatusImage_3.setPixmap(self.irPixmap)
			self.ui.lfStatusImage_3.setPixmap(self.lfPixmap)

			self.x = str(self.ghost2.xPos)
			self.y = str(self.ghost2.yPos)
			self.heading = str(self.ghost2.heading)
			self.previous = str(self.ghost2.prevState)

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
