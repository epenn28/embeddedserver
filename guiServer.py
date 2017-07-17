import sys
import socket
import threading
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtNetwork import QTcpServer, QTcpSocket, QAbstractSocket, QHostAddress
from PyQt5.QtCore import QThread, QReadWriteLock, QDataStream, pyqtSignal
from ui_mainwindow import Ui_MainWindow
		
		
class Thread(QThread):
	
	sendData = pyqtSignal(bytes, str)
	#sendAddr = pyqtSignal(str)
	
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
		#self.sendAddr.emit(address)
		while socket.state() == QAbstractSocket.ConnectedState:
			data = bytes(5)
			stream = QDataStream(socket)
			stream.setVersion(QDataStream.Qt_5_8)
			while True:
				socket.waitForReadyRead(-1)
				if socket.bytesAvailable() >= 5:
					data = stream.readRawData(5)
					self.sendData.emit(data, address)
					break
		
		
class ThreadedServer(QTcpServer):
	"""
	headerOut = pyqtSignal(str)
	packetCountOut = pyqtSignal(str)
	sourceOut = pyqtSignal(str)
	valueOut = pyqtSignal(str)
	footerOut = pyqtSignal(str)
	"""
	dataOut = pyqtSignal(bytes, str)
	#ipOut = pyqtSignal(str)
	
	def __init__(self, parent = None):
		super().__init__(parent)
		self.client_list = []
		
	def incomingConnection(self, socketId):
		thread = Thread(socketId, self)
		thread.finished.connect(thread.deleteLater)
		self.client_list.append(thread)
		thread.sendData.connect(self.newData)
		#thread.sendAddr.connect(self.newClient)
		thread.start()
		
	def newData(self, data, ip):
		"""
		output = data.hex()
		header, packetCount, source, value, footer = output[:2], str(int(output[2:4], 16)), output[4:6], output[6:8], output[8:]
		self.headerOut.emit(header)
		self.packetCountOut.emit(packetCount)
		self.sourceOut.emit(source)
		self.valueOut.emit(value)
		self.footerOut.emit(footer)
		"""
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
		
		# Connect server signals to output line edit boxes
		#self.server.ipOut.connect(self.addClient)
		#self.server.dataOut.connect(
		"""
		self.server.packetCountOut.connect(self.ui.forwardValue.setText)
		self.server.sourceOut.connect(self.ui.leftValue.setText)
		self.server.valueOut.connect(self.ui.rightValue.setText)
		self.server.footerOut.connect(self.ui.lineValue.setText)
		"""
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
				# connect thread's data to proper display
				self.server.dataOut.connect(self.convertData)
				thread.guiDisplay = True
			else:  # if already running, do nothing
				pass 
	
	# TODO: add ip as a method of this slot and use it to check where to connect data	
	def convertData(self, data, ip):
		output = data.hex()
		header, packetCount, source, value, footer = output[:2], str(int(output[2:4], 16)), output[4:6], output[6:8], output[8:]
		
		self.ui.ipValue.setText(ip)
		self.ui.forwardValue.setText(packetCount)

		
port_num = 2000
app = QApplication(sys.argv)
window = MyWindow()

window.show()
sys.exit(app.exec_())