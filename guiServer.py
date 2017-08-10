import sys
import socket
import threading
import binascii
import time
import numpy
from enum import Enum
from random import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QLabel, QPushButton
from PyQt5.QtNetwork import QTcpServer, QTcpSocket, QAbstractSocket, QHostAddress
from PyQt5.QtCore import QObject, QThread, QReadWriteLock, QDataStream, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPixmap, QFont
from ui_mainwindow import Ui_PacMan


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
	GAME_OVER = 12

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
			elif command == Command.GAME_OVER:
				value = "C".rjust(2, '0').encode()
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
	scoreChanged = pyqtSignal(str)

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
		self.pacman.xPos = 2
		self.pacman.yPos = 2
		self.pacman.heading = "west"
		self.ghost1.xPos = 6
		self.ghost1.yPos = 4
		self.ghost1.heading = "east"
		self.ghost2.xPos = 6
		self.ghost2.yPos = 0
		self.ghost2.heading = "east"
		self.manual = True
		self.score = 0

		super().__init__(parent)
		self.serverState = "Init"
		self.stateChanged.emit(self.serverState)
		self.ui = Ui_PacMan()
		self.ui.setupUi(self)
		self.ui.stopButton.setEnabled(False)
		self.ui.automaticButton.setEnabled(False)
		self.ui.overrideButton.setEnabled(False)
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
		self.ui.scoreValue.setTextFormat(Qt.RichText)
		f = self.ui.scoreValue.font()
		f.setPointSize(20)
		self.ui.scoreValue.setFont(f)
		self.stateChanged.connect(self.ui.statusValue.setText)

		self.server.dataOut.connect(self.calculateNextCommand)
		self.server.serverRunning.connect(self.ui.statusValue.setText)
		self.scoreChanged.connect(self.ui.scoreValue.setText)

		self.serverState = "Stopped"
		self.stateChanged.emit(self.serverState)

	def startServer(self):
		self.ui.stopButton.setEnabled(True)
		self.ui.startButton.setEnabled(False)
		self.ui.automaticButton.setEnabled(True)
		self.ui.overrideButton.setEnabled(True)
		self.serverState = "Started"
		self.stateChanged.emit(self.serverState)
		if not self.server.listen(QHostAddress("0.0.0.0"), port_num):
			QMessageBox.critical(self, "Pac-Man server", "Failed to start server")
			self.close()
			return

	def stopServer(self):
		self.ui.stopButton.setEnabled(False)
		self.ui.startButton.setEnabled(True)
		self.ui.automaticButton.setEnabled(False)
		self.ui.overrideButton.setEnabled(False)
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
		output = binascii.hexlify(data)
		header, source, values, footer = output[:2], int(output[2:4], 16), output[4:14], output[14:]

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
		
		if source == 0:  # sensors
			self.front, self.left, self.right, self.irState, self.lfState = values[:2], values[2:4], values[4:6], values[6:8], values[8:10]
			self.updateValues()
			self.newCommand()
			self.game_over()
			self.drawImage()
			self.displaySensorValues(self.rover)

	def updateValues(self):
		if self.rover == "pacman":
			self.pacman.irState = self.irState
			#if(int(self.left) <= int(12)):
			#	print("Pacman state changed", self.left)
			#self.pacman.prevState = self.previous
		elif self.rover == "ghost1":
			self.ghost1.irState = self.irState
			#if(int(self.right) <= int(12)):
			#	print("Ghost 1 state changed", self.right)
			#self.ghost1.prevState = self.previous
		elif self.rover == "ghost2":
			self.ghost2.irState = self.irState
			#self.ghost2.prevState = self.previous
			
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
			if self.ghost2.heading == "north":
				if command == Command.FORWARD:
					#if self.left_distance <= 10 and self.right_distance <= 10:
					#        if self.previous_ghost2_state == ghost2_States[0]:
					#                self.ghost2.yPos += 1
					self.ghost2.yPos += 2
				elif command == Command.STOP_LEFT_FORWARD:
					self.ghost2.xPos -= 2
					self.ghost2.heading = "west"
				elif command == Command.STOP_RIGHT_FORWARD:
					self.ghost2.xPos += 2
					self.ghost2.heading = "east"
			elif self.ghost2.heading == "south":
				if command == Command.FORWARD:
					#if self.left_distance <= 10 and self.right_distance <= 10:
					#        self.ghost2.yPos -= 1
					#        self.ghost2.yPos -= 1
					#else:
					self.ghost2.yPos -= 2
				elif command == Command.STOP_LEFT_FORWARD:
					self.ghost2.xPos += 2
					self.ghost2.heading = "east"
				elif command == Command.STOP_RIGHT_FORWARD:
					self.ghost2.xPos -= 2
					self.ghost2.heading = "west"
			elif self.ghost2.heading == "east":
				if command == Command.FORWARD:
					#if self.left_distance <= 10 and self.right_distance <= 10:
					#        self.ghost2.xPos += 1
					#        self.ghost2.xPos += 1
					#else:
					self.ghost2.xPos += 2
				elif command == Command.STOP_LEFT_FORWARD:
					self.ghost2.yPos += 2
					self.ghost2.heading = "north"
				elif command == Command.STOP_RIGHT_FORWARD:
					self.ghost2.yPos -= 2
					self.ghost2.heading = "south"
			elif self.ghost2.heading == "west":
				if command == Command.FORWARD:
					#if self.left_distance <= 10 and self.right_distance <= 10:
					#        self.ghost2.xPos -= 1
					#        self.ghost2.xPos -= 1
					#else:
					self.ghost2.xPos -= 2
				elif command == Command.STOP_LEFT_FORWARD:
					self.ghost2.yPos -= 2
					self.ghost2.heading = "south"
				elif command == Command.STOP_RIGHT_FORWARD:
					self.ghost2.yPos += 2
					self.ghost2.heading = "north"

	def pacManCoords(self, command):
		if self.pacman.heading == "north":
			if command == Command.FORWARD:
				return self.pacman.xPos, (self.pacman.yPos + 2), "north"
			elif command == Command.STOP_LEFT_FORWARD:
				return (self.pacman.xPos - 2), self.pacman.yPos, "west"
			elif command == Command.STOP_RIGHT_FORWARD:
				return (self.pacman.xPos + 2), self.pacman.yPos, "east"
		elif self.pacman.heading == "south":
			if command == Command.FORWARD:
				return self.pacman.xPos, (self.pacman.yPos - 2), "south"
			elif command == Command.STOP_LEFT_FORWARD:
				return (self.pacman.xPos + 2), self.pacman.yPos, "east"
			elif command == Command.STOP_RIGHT_FORWARD:
				return self.pacman.xPos - 2, self.pacman.yPos, "west"
		elif self.pacman.heading == "east":
			if command == Command.FORWARD:
				return self.pacman.xPos + 2, self.pacman.yPos, "east"
			elif command == Command.STOP_LEFT_FORWARD:
				return self.pacman.xPos, self.pacman.yPos + 2, "north"
			elif command == Command.STOP_RIGHT_FORWARD:
					return self.pacman.xPos, self.pacman.yPos - 2, "south"
		elif self.pacman.heading == "west":
			if command == Command.FORWARD:
				return self.pacman.xPos - 2, self.pacman.yPos, "west"
			elif command == Command.STOP_LEFT_FORWARD:
				return self.pacman.xPos, (self.pacman.yPos - 2), "south"
			elif command == Command.STOP_RIGHT_FORWARD:
				return self.pacman.xPos, (self.pacman.yPos + 2), "north"
				
	def ghost1Coords(self, command):
		if self.ghost1.heading == "north":
			if command == Command.FORWARD:
				return self.ghost1.xPos, (self.ghost1.yPos + 2), "north"
			elif command == Command.STOP_LEFT_FORWARD:
				return (self.ghost1.xPos - 2), self.ghost1.yPos, "west"
			elif command == Command.STOP_RIGHT_FORWARD:
				return (self.ghost1.xPos + 2), self.ghost1.yPos, "east"
		elif self.ghost1.heading == "south":
			if command == Command.FORWARD:
				return self.ghost1.xPos, (self.ghost1.yPos - 2), "south"
			elif command == Command.STOP_LEFT_FORWARD:
				return (self.ghost1.xPos + 2), self.ghost1.yPos, "east"
			elif command == Command.STOP_RIGHT_FORWARD:
				return self.ghost1.xPos - 2, self.ghost1.yPos, "west"
		elif self.ghost1.heading == "east":
			if command == Command.FORWARD:
				return self.ghost1.xPos + 2, self.ghost1.yPos, "east"
			elif command == Command.STOP_LEFT_FORWARD:
				return self.ghost1.xPos, self.ghost1.yPos + 2, "north"
			elif command == Command.STOP_RIGHT_FORWARD:
					return self.ghost1.xPos, self.ghost1.yPos - 2, "south"
		elif self.ghost1.heading == "west":
			if command == Command.FORWARD:
				return self.ghost1.xPos - 2, self.ghost1.yPos, "west"
			elif command == Command.STOP_LEFT_FORWARD:
				return self.ghost1.xPos, (self.ghost1.yPos - 2), "south"
			elif command == Command.STOP_RIGHT_FORWARD:
				return self.ghost1.xPos, (self.ghost1.yPos + 2), "north"
				
	def ghost2Coords(self, command):
		if self.ghost2.heading == "north":
			if command == Command.FORWARD:
				return self.ghost2.xPos, (self.ghost2.yPos + 2), "north"
			elif command == Command.STOP_LEFT_FORWARD:
				return (self.ghost2.xPos - 2), self.ghost2.yPos, "west"
			elif command == Command.STOP_RIGHT_FORWARD:
				return (self.ghost2.xPos + 2), self.ghost2.yPos, "east"
		elif self.ghost2.heading == "south":
			if command == Command.FORWARD:
				return self.ghost2.xPos, (self.ghost2.yPos - 2), "south"
			elif command == Command.STOP_LEFT_FORWARD:
				return (self.ghost2.xPos + 2), self.ghost2.yPos, "east"
			elif command == Command.STOP_RIGHT_FORWARD:
				return self.ghost2.xPos - 2, self.ghost2.yPos, "west"
		elif self.ghost2.heading == "east":
			if command == Command.FORWARD:
				return self.ghost2.xPos + 2, self.ghost2.yPos, "east"
			elif command == Command.STOP_LEFT_FORWARD:
				return self.ghost2.xPos, self.ghost2.yPos + 2, "north"
			elif command == Command.STOP_RIGHT_FORWARD:
					return self.ghost2.xPos, self.ghost2.yPos - 2, "south"
		elif self.ghost2.heading == "west":
			if command == Command.FORWARD:
				return self.ghost2.xPos - 2, self.ghost2.yPos, "west"
			elif command == Command.STOP_LEFT_FORWARD:
				return self.ghost2.xPos, (self.ghost2.yPos - 2), "south"
			elif command == Command.STOP_RIGHT_FORWARD:
				return self.ghost2.xPos, (self.ghost2.yPos + 2), "north"
				
	def determine_distance_ghost1(self, x, y):
		x_dist = 0
		y_dist = 0
		if x > self.ghost1.xPos:
			x_dist = x - self.ghost1.xPos
		else: 
			x_dist = self.ghost1.xPos - x
		if y > self.ghost1.yPos:
			y_dist = y - self.ghost1.yPos
		else:
			y_dist = self.ghost1.yPos - y
		return x_dist + y_dist
		
	def determine_distance_ghost2(self, x, y):
		x_dist = 0
		y_dist = 0
		if x > self.ghost2.xPos:
			x_dist = x - self.ghost2.xPos
		else: 
			x_dist = self.ghost2.xPos - x
		if y > self.ghost2.yPos:
			y_dist = y - self.ghost2.yPos
		else:
			y_dist = self.ghost2.yPos - y
		return x_dist + y_dist
		
	def determine_distance_pacman(self, x, y):
		x_dist = 0
		y_dist = 0
		if x > self.pacman.xPos:
			x_dist = x - self.pacman.xPos
		else: 
			x_dist = self.pacman.xPos - x
		if y > self.pacman.yPos:
			y_dist = y - self.pacman.yPos
		else:
			y_dist = self.pacman.yPos - y
		return x_dist + y_dist
	
	def determine_closest_ghost(self):
		ghost1 = self.determine_distance_ghost1(self.pacman.xPos, self.pacman.yPos)
		#print("Ghost 1 distance = {}".format(ghost1))
		ghost2 = self.determine_distance_ghost2(self.pacman.xPos, self.pacman.yPos)
		#print("Ghost 2 distance = {}".format(ghost1))
		if ghost1 == ghost2:
			return "random"
		else:
			close = min([ghost1, ghost2])
		if close == ghost1:
			#print("Closest ghost: ghost 1")
			return "ghost1"
		else:
			#print("Closest ghost: ghost 2")
			return "ghost2"
		
	def game_over(self):
		pacIP = "192.168.1.103"
		ghost1IP = "192.168.1.104"
		ghost2IP = "192.168.1.105"
		if self.pacman.xPos == self.ghost1.xPos and self.pacman.yPos == self.ghost1.yPos and self.pacman.heading != self.ghost1.heading:
			self.sendCommand.emit(Command.GAME_OVER, pacIP)
			self.sendCommand.emit(Command.GAME_OVER, ghost1IP)
			self.sendCommand.emit(Command.PAUSE, ghost2IP)
			self.scoreChanged.emit("<font color='maroon'>" + str(self.score) + "</font>")
			self.serverState = "Game Over"
			self.stateChanged.emit(self.serverState)
			#self.ui.scoreValue.setText("<font color='maroon'>" + self.score + "</font>") # Use this to change color on game over
			#self.sendCommand.emit(Command.PAUSE, "all")
		elif self.pacman.xPos == self.ghost2.xPos and self.pacman.yPos == self.ghost2.yPos and self.pacman.heading != self.ghost2.heading:
			self.sendCommand.emit(Command.GAME_OVER, pacIP)
			self.sendCommand.emit(Command.GAME_OVER, ghost2IP)
			self.sendCommand.emit(Command.PAUSE, ghost1IP)
			self.scoreChanged.emit("<font color='maroon'>" + str(self.score) + "</font>")
			self.serverState = "Game Over"
			self.stateChanged.emit(self.serverState)
			#self.ui.scoreValue.setText("<font color='maroon'>" + self.score + "</font>") # Use this to change color on game over
			#self.sendCommand.emit(Command.PAUSE, "all")
		
	def pacman_decision(self, possible_moves):
		if len(possible_moves) == 1:
			return possible_moves[0]
		elif len(possible_moves) == 2:
			move1 = possible_moves[0]
			move2 = possible_moves[1]
			x1, y1, heading1 = self.pacManCoords(move1)
			move1_dist1 = self.determine_distance_ghost1(x1, y1)
			#print("Move1_dist1 =", move1_dist1)
			move1_dist2 = self.determine_distance_ghost2(x1, y1)
			x2, y2, heading2 = self.pacManCoords(move2)
			move2_dist1 = self.determine_distance_ghost1(x2, y2)
			#print("Move2_dist1 =", move2_dist1)
			move2_dist2 = self.determine_distance_ghost2(x2, y2)
			closer_ghost = self.determine_closest_ghost()
			if closer_ghost == "ghost1":
				if move1_dist1 == move2_dist1:
					#print("Moves are Equidistant - Random Move")
					x = randint(0,1)
					return possible_moves[x]
				else:
					best_dist = max([move1_dist1, move2_dist1])
					#print("Distance =", best_dist)
					if best_dist == move1_dist1:
						return move1
					else:
						return move2
			elif closer_ghost == "ghost2":
				if move1_dist2 == move2_dist2:
					#print("Move is Equidistant - Random Move")
					x = randint(0, 1)
					return possible_moves[x]
				else:
					best_dist = max([move1_dist2, move2_dist2])
					#print("Distance =", best_dist)
					if best_dist == move1_dist2:
						return move1
					else:
						return move2
			elif closer_ghost == "random":
				best_dist = max([move1_dist1, move1_dist2, move2_dist1, move2_dist2])
				if best_dist == move1_dist1 or best_dist == move1_dist2:
					return move1
				else:
					return move2
			
		elif len(possible_moves) == 3:
			move1 = possible_moves[0]
			move2 = possible_moves[1]
			move3 = possible_moves[2]
			x1, y1, heading1 = self.pacManCoords(move1)
			move1_dist1 = self.determine_distance_ghost1(x1, y1)
			move1_dist2 = self.determine_distance_ghost2(x1, y1)
			x2, y2, heading2 = self.pacManCoords(move2)
			move2_dist1 = self.determine_distance_ghost1(x2, y2)
			move2_dist2 = self.determine_distance_ghost2(x2, y2)
			x3, y3, heading3 = self.pacManCoords(move3)
			move3_dist1 = self.determine_distance_ghost1(x3, y3)
			move3_dist2 = self.determine_distance_ghost2(x3, y3)
			closer_ghost = self.determine_closest_ghost()
			if closer_ghost == "ghost1":
				if move1_dist1 == move2_dist1 and move1_dist1 == move3_dist1:
					x = randint(0,2)
					return possible_moves[x]
				elif move1_dist1 == move2_dist1 and move3_dist1 < move1_dist1:
					#print("Move1 and Move2 are Equidistance - Random move")
					x = randint(0, 1)
					return possible_moves[x]
				elif move1_dist1 == move3_dist1 and move2_dist1 < move1_dist1:
					#print("Move1 and Move3 are Equidistance - Random move")
					x = randint(0, 1)
					if x == 0:
						return possible_moves[x]
					else:
						return possible_moves[2]
				elif move2_dist1 == move3_dist1 and move1_dist1 < move2_dist1:
					#print("Move2 and Move3 are Equidistance - Random move")
					x = randint(1, 2)
					return possible_moves[x]
				else:	
					#print("best distance =", best_dist)
					best_dist = max([move1_dist1, move2_dist1, move3_dist1])
					if best_dist == move1_dist1:
						return move1
					elif best_dist == move2_dist1:
						return move2
					else:
						return move3
			elif closer_ghost == "ghost2":
				if move1_dist2 == move2_dist2 and move1_dist2 == move3_dist2:
					#print("Moves are Equidistant - Random Move")
					x = randint(0,2)
					return possible_moves[x]
				elif move1_dist2 == move2_dist2 and move3_dist2 < move1_dist2:
					#print("Move1 and Move2 are equidistant - random move")
					x = randint(0, 1)
					return possible_moves[x]
				elif move1_dist2 == move3_dist2 and move2_dist2 < move1_dist2:
					#print("Move1 and Move3 are equidistant - random move")
					x = randint(0, 1)
					if x == 0:
						return possible_moves[x]
					else:
						return possible_moves[2]
				elif move2_dist2 == move3_dist2 and move1_dist2 < move2_dist2:
					#print("Move2 and move3 are equidistant - random move")
					x = randint(1, 2)
					return possible_moves[x]
				else:	
					best_dist = max([move1_dist2, move2_dist2, move3_dist2])
					#print("best distance =", best_dist)
					if best_dist == move1_dist2:
						return move1
					elif best_dist == move2_dist2:
						return move2
					else:
						return move3
			elif closer_ghost == "random":
				best_dist = max([move1_dist1, move1_dist2, move2_dist1, move2_dist2, move3_dist1, move3_dist2])
				if best_dist == move1_dist1 or best_dist == move1_dist2:
					return move1
				elif best_dist == move2_dist1 or best_dist == move2_dist2:
					return move2
				else:
					return move3
				
	def ghost1_decision(self, possible_moves):
		if len(possible_moves) == 1:
			return possible_moves[0]
		elif len(possible_moves) == 2:
			move1 = possible_moves[0]
			move2 = possible_moves[1]
			x1, y1, heading1 = self.ghost1Coords(move1)
			move1_dist = self.determine_distance_pacman(x1, y1)
			x2, y2, heading2 = self.ghost1Coords(move2)
			move2_dist = self.determine_distance_pacman(x2, y2)
			if (x1, y1) == (self.ghost2.xPos, self.ghost2.yPos):
				return move2
			elif (x2, y2) == (self.ghost2.xPos, self.ghost2.yPos):
				return move1
			best_dist = min([move1_dist, move2_dist])
			if best_dist == move1_dist:
				return move1
			elif best_dist == move2_dist:
				return move2
		elif len(possible_moves) == 3:
			move1 = possible_moves[0]
			move2 = possible_moves[1]
			move3 = possible_moves[2]
			x1, y1, heading1 = self.ghost1Coords(move1)
			move1_dist = self.determine_distance_pacman(x1, y1)
			x2, y2, heading2 = self.ghost1Coords(move2)
			move2_dist = self.determine_distance_pacman(x2, y2)
			x3, y3, heading3 = self.ghost1Coords(move3)
			move3_dist = self.determine_distance_pacman(x3, y3)
			if (x1, y1) == (self.ghost2.xPos, self.ghost2.yPos):
				return move2
			elif (x2, y2) == (self.ghost2.xPos, self.ghost2.yPos):
				return move1
			elif (x3, y3) == (self.ghost2.xPos, self.ghost2.yPos):
				x = randint(0,1)
				return possible_moves[x]
			best_dist = min([move1_dist, move2_dist, move3_dist])
			if best_dist == move1_dist:
				return move1
			elif best_dist == move2_dist:
				return move2
			elif best_dist == move3_dist:
				return move3
				
	def ghost2_decision(self, possible_moves):
		if len(possible_moves) == 1:
			return possible_moves[0]
		elif len(possible_moves) == 2:
			move1 = possible_moves[0]
			move2 = possible_moves[1]
			x1, y1, heading1 = self.ghost2Coords(move1)
			move1_dist = self.determine_distance_pacman(x1, y1)
			x2, y2, heading2 = self.ghost2Coords(move2)
			move2_dist = self.determine_distance_pacman(x2, y2)
			if (x1, y1) == (self.ghost1.xPos, self.ghost1.yPos):
				return move2
			elif (x2, y2) == (self.ghost1.xPos, self.ghost1.yPos):
				return move1
			best_dist = min([move1_dist, move2_dist])
			if best_dist == move1_dist:
				return move1
			elif best_dist == move2_dist:
				return move2
		elif len(possible_moves) == 3:
			move1 = possible_moves[0]
			move2 = possible_moves[1]
			move3 = possible_moves[2]
			x1, y1, heading1 = self.ghost2Coords(move1)
			move1_dist = self.determine_distance_pacman(x1, y1)
			x2, y2, heading2 = self.ghost2Coords(move2)
			move2_dist = self.determine_distance_pacman(x2, y2)
			x3, y3, heading3 = self.ghost2Coords(move3)
			move3_dist = self.determine_distance_pacman(x3, y3)
			if (x1, y1) == (self.ghost1.xPos, self.ghost1.yPos):
				return move2
			elif (x2, y2) == (self.ghost1.xPos, self.ghost1.yPos):
				return move1
			elif (x3, y3) == (self.ghost1.xPos, self.ghost1.yPos):
				x = randint(0,1)
				return possible_moves[x]
			best_dist = min([move1_dist, move2_dist, move3_dist])
			if best_dist == move1_dist:
				return move1
			elif best_dist == move2_dist:
				return move2
			elif best_dist == move3_dist:
				return move3
				
	def printCoords(self):
		print("Pacman headed toward ({}, {}) with state {} and previous state {}".format(self.pacman.xPos, self.pacman.yPos, self.pacman.irState, self.pacman.prevState))
		
	def printGhost1Coords(self):
		print("Ghost1 headed toward ({}, {}) with state {} and previous state {}".format(self.ghost1.xPos, self.ghost1.yPos, self.ghost1.irState, self.ghost1.prevState))

	def printGhost2Coords(self):
		print("Ghost2 headed toward ({}, {}) with state {} and previous state {}".format(self.ghost2.xPos, self.ghost2.yPos, self.ghost2.irState, self.ghost2.prevState))

	def newCommand(self):
		pacIP = "192.168.1.103"
		ghost1IP = "192.168.1.104"
		ghost2IP = "192.168.1.105"
		x = 0
		if self.manual:
			return

		if self.rover == "pacman":
			if self.pacman.irState == "01":  # Forward open, left blocked, right blocked
				pass
			elif self.pacman.irState == "02":  # Forward open, left open, right open
				commands = [Command.FORWARD, Command.STOP_LEFT_FORWARD, Command.STOP_RIGHT_FORWARD]
				if self.pacman.prevState == "01":
					choice = self.pacman_decision(commands)
					self.decideCoordinate(choice)
					if choice == Command.FORWARD:
						print("forward")
					elif choice == Command.STOP_LEFT_FORWARD:
						print("left")
					elif choice == Command.STOP_RIGHT_FORWARD:
						print("right")
					self.printCoords()
					self.sendCommand.emit(choice, pacIP)
					self.score += 1
			elif self.pacman.irState == "03":  # Forward blocked, left open, right open
				commands = [Command.STOP_LEFT_FORWARD, Command.STOP_RIGHT_FORWARD]
				if self.pacman.prevState == "01":
					choice = self.pacman_decision(commands)
					self.decideCoordinate(choice)
					if choice == Command.STOP_LEFT_FORWARD:
						print("left")
					elif choice == Command.STOP_RIGHT_FORWARD:
						print("right")
					self.printCoords()
					self.sendCommand.emit(choice, pacIP)
					self.score += 1
			elif self.pacman.irState == "04":  # Forward blocked, left open, right blocked
				if self.pacman.prevState == "01":
					self.decideCoordinate(Command.STOP_LEFT_FORWARD)
					print("left")
					self.printCoords()
					self.sendCommand.emit(Command.STOP_LEFT_FORWARD, pacIP)
					self.score += 1
			elif self.pacman.irState == "05":  # Forward blocked, left blocked, right open
				if self.pacman.prevState == "01":
					self.decideCoordinate(Command.STOP_RIGHT_FORWARD)
					print("right")
					self.printCoords()
					self.sendCommand.emit(Command.STOP_RIGHT_FORWARD, pacIP)
					self.score += 1
			elif self.pacman.irState == "06":  # Forward open, left open, right blocked
				commands = [Command.FORWARD, Command.STOP_LEFT_FORWARD]
				if self.pacman.prevState == "01":
					choice = self.pacman_decision(commands)
					self.decideCoordinate(choice)
					if choice == Command.FORWARD:
						print("forward")
					elif choice == Command.STOP_LEFT_FORWARD:
						print("left")
					self.printCoords()
					self.sendCommand.emit(choice, pacIP)
					self.score += 1
			elif self.pacman.irState == "07":  # Forward open, left blocked, right open
				commands = [Command.FORWARD, Command.STOP_RIGHT_FORWARD]
				if self.pacman.prevState == "01":
					choice = self.pacman_decision(commands)
					self.decideCoordinate(choice)
					if choice == Command.FORWARD:
						print("forward")
					elif choice == Command.STOP_RIGHT_FORWARD:
						print("right")
					self.printCoords()
					self.sendCommand.emit(choice, pacIP)
					self.score += 1
			self.pacman.prevState = self.pacman.irState
			self.scoreChanged.emit(str(self.score))

		if self.rover == "ghost1":
			if self.ghost1.irState == "01":  # Forward open, left blocked, right blocked
				pass
			if self.ghost1.irState == "02":  # Forward open, left open, right open
				commands = [Command.FORWARD, Command.STOP_LEFT_FORWARD, Command.STOP_RIGHT_FORWARD]
				if self.ghost1.prevState == "01":
					choice = self.ghost1_decision(commands)
					self.decideCoordinate(choice)
					self.printGhost1Coords()
					self.sendCommand.emit(choice, ghost1IP)
			if self.ghost1.irState == "03":  # Forward blocked, left open, right open
				commands = [Command.STOP_LEFT_FORWARD, Command.STOP_RIGHT_FORWARD]
				if self.ghost1.prevState == "01":
					choice = self.ghost1_decision(commands)
					self.decideCoordinate(choice)
					self.printGhost1Coords()
					self.sendCommand.emit(choice, ghost1IP)
			if self.ghost1.irState == "04":  # Forward blocked, left open, right blocked
				if self.ghost1.prevState == "01":
					self.decideCoordinate(Command.STOP_LEFT_FORWARD)
					self.printGhost1Coords()
					self.sendCommand.emit(Command.STOP_LEFT_FORWARD, ghost1IP)
			if self.ghost1.irState == "05":  # Forward blocked, left blocked, right open
				if self.ghost1.prevState == "01":
					self.decideCoordinate(Command.STOP_RIGHT_FORWARD)
					self.printGhost1Coords()
					self.sendCommand.emit(Command.STOP_RIGHT_FORWARD, ghost1IP)
			if self.ghost1.irState == "06":  # Forward open, left open, right blocked
				commands = [Command.FORWARD, Command.STOP_LEFT_FORWARD]
				if self.ghost1.prevState == "01":
					choice = self.ghost1_decision(commands)
					self.decideCoordinate(choice)
					self.printGhost1Coords()
					self.sendCommand.emit(choice, ghost1IP)
			if self.ghost1.irState == "07":  # Forward open, left blocked, right open
				commands = [Command.FORWARD, Command.STOP_RIGHT_FORWARD]
				if self.ghost1.prevState == "01":
					choice = self.ghost1_decision(commands)
					self.decideCoordinate(choice)
					self.printGhost1Coords()
					self.sendCommand.emit(choice, ghost1IP)
			self.ghost1.prevState = self.ghost1.irState

		if self.rover == "ghost2":
			if self.ghost2.irState == "01":  # Forward open, left blocked, right blocked
				pass
			if self.ghost2.irState == "02":  # Forward open, left open, right open
				commands = [Command.FORWARD, Command.STOP_LEFT_FORWARD, Command.STOP_RIGHT_FORWARD]
				if self.ghost2.prevState == "01":
					choice = self.ghost2_decision(commands)
					self.decideCoordinate(choice)
					self.printGhost2Coords()
					self.sendCommand.emit(choice, ghost2IP)
			if self.ghost2.irState == "03":  # Forward blocked, left open, right open
				commands = [Command.STOP_LEFT_FORWARD, Command.STOP_RIGHT_FORWARD]
				if self.ghost2.prevState == "01":
					choice = self.ghost2_decision(commands)
					self.decideCoordinate(choice)
					self.printGhost2Coords()
					self.sendCommand.emit(choice, ghost2IP)
			if self.ghost2.irState == "04":  # Forward blocked, left open, right blocked
				if self.ghost2.prevState == "01":
					self.decideCoordinate(Command.STOP_LEFT_FORWARD)
					self.printGhost2Coords()
					self.sendCommand.emit(Command.STOP_LEFT_FORWARD, ghost2IP)
			if self.ghost2.irState == "05":  # Forward blocked, left blocked, right open
				if self.ghost2.prevState == "01":
					self.decideCoordinate(Command.STOP_RIGHT_FORWARD)
					self.printGhost2Coords()
					self.sendCommand.emit(Command.STOP_RIGHT_FORWARD, ghost2IP)
			if self.ghost2.irState == "06":  # Forward open, left open, right blocked
				commands = [Command.FORWARD, Command.STOP_LEFT_FORWARD]
				if self.ghost2.prevState == "01":
					choice = self.ghost2_decision(commands)
					self.decideCoordinate(choice)
					self.printGhost2Coords()
					self.sendCommand.emit(choice, ghost2IP)
			if self.ghost2.irState == "07":  # Forward open, left blocked, right open
				commands = [Command.FORWARD, Command.STOP_RIGHT_FORWARD]
				if self.ghost2.prevState == "01":
					choice = self.ghost2_decision(commands)
					self.decideCoordinate(choice)
					self.printGhost2Coords()
					self.sendCommand.emit(choice, ghost2IP)
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
