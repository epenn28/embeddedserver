import sys
import socket
import threading
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtNetwork import QTcpServer, QTcpSocket, QAbstractSocket, QHostAddress
from PyQt5.QtCore import QThread, QReadWriteLock, QDataStream, pyqtSignal
from ui_mainwindow import Ui_MainWindow
		
		
class Thread(QThread):
	
	trigger = pyqtSignal(bytes)
	sendAddr = pyqtSignal(str)
	
	def __init__(self, socketId, parent = None):
		super().__init__(parent)
		self.socketId = socketId
		
	def run(self):
		socket = QTcpSocket()
		if not socket.setSocketDescriptor(self.socketId):
			self.emit(SIGNAL("error(int)"), socket.error())
			return
		while socket.state() == QAbstractSocket.ConnectedState:
			address = QHostAddress(socket.peerAddress()).toString()
			self.sendAddr.emit(address)
			data = bytes(5)
			stream = QDataStream(socket)
			stream.setVersion(QDataStream.Qt_5_8)
			while True:
				socket.waitForReadyRead(-1)
				if socket.bytesAvailable() >= 5:
					data = stream.readRawData(5)
					self.trigger.emit(data)
					break
		
		
class ThreadedServer(QTcpServer):
	
	headerOut = pyqtSignal(str)
	packetCountOut = pyqtSignal(str)
	sourceOut = pyqtSignal(str)
	valueOut = pyqtSignal(str)
	footerOut = pyqtSignal(str)
	ipOut = pyqtSignal(str)
	
	def __init__(self, parent = None):
		super().__init__(parent)
		
	def incomingConnection(self, socketId):
		thread = Thread(socketId, self)
		thread.finished.connect(thread.deleteLater)
		thread.trigger.connect(self.newData)
		thread.sendAddr.connect(self.ipAddress)
		thread.start()
		
	def newData(self, data):
		output = data.hex()
		header, packetCount, source, value, footer = output[:2], str(int(output[2:4], 16)), output[4:6], output[6:8], output[8:]
		self.headerOut.emit(header)
		self.packetCountOut.emit(packetCount)
		self.sourceOut.emit(source)
		self.valueOut.emit(value)
		self.footerOut.emit(footer)
		
	def ipAddress(self, ip):
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
		
		self.server.ipOut.connect(self.ui.ipValue.setText)
		self.server.packetCountOut.connect(self.ui.forwardValue.setText)
		self.server.sourceOut.connect(self.ui.leftValue.setText)
		self.server.valueOut.connect(self.ui.rightValue.setText)
		self.server.footerOut.connect(self.ui.lineValue.setText)
		
	def startServer(self):
		if not self.server.listen(QHostAddress("0.0.0.0"), port_num):
			# TODO: fix this message box
			QMessageBox.critical(self, "Raspberry Pi server", QString("Failed to start server: %1").arg(self.server.errorString()))
			self.close()
			return

		
port_num = 2000
app = QApplication(sys.argv)
window = MyWindow()

window.show()
sys.exit(app.exec_())