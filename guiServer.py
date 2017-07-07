import sys
import socket
import select
import threading
import codecs
import binascii
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtNetwork import QTcpServer, QTcpSocket, QAbstractSocket, QHostAddress
from PyQt5.QtCore import QThread, QReadWriteLock, QDataStream, pyqtSignal
from ui_mainwindow import Ui_MainWindow
		
		
class Thread(QThread):
	
	trigger = pyqtSignal(bytes)
	
	def __init__(self, socketId, parent = None):
		super().__init__(parent)
		self.socketId = socketId
		
	def run(self):
		socket = QTcpSocket()
		if not socket.setSocketDescriptor(self.socketId):
			self.emit(SIGNAL("error(int)"), socket.error())
			return
		while socket.state() == QAbstractSocket.ConnectedState:
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
	
	dataOut = pyqtSignal(str)
	
	def __init__(self, parent = None):
		super().__init__(parent)
		
	def incomingConnection(self, socketId):
		thread = Thread(socketId, self)
		#self.connect(thread, SIGNAL("finished()"), thread, SLOT("deleteLater()"))
		thread.finished.connect(thread.deleteLater)
		thread.trigger.connect(self.newData)
		thread.start()
		
	def newData(self, data):
		output = data.hex()
		self.dataOut.emit(output)

        
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
		
		self.server.dataOut.connect(self.ui.ipValue.setText)
		
	def startServer(self):
		if not self.server.listen(QHostAddress("0.0.0.0"), port_num):
			QMessageBox.critical(self, "Raspberry Pi server", QString("Failed to start server: %1").arg(self.server.errorString()))
			self.close()
			return

		
port_num = 2000
app = QApplication(sys.argv)
window = MyWindow()

window.show()
sys.exit(app.exec_())