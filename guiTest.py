import sys
import unittest
import PyQt5
from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt
import guiServer

app = QApplication(sys.argv)

class ServerTest(unittest.TestCase):
    def setUp(self):
        self.form = guiServer.MyWindow()

    def testWindow(self):
        self.assertIsInstance(self.form.ui.centralWidget, PyQt5.QtWidgets.QWidget)

    def testButtons(self):
        self.assertEqual(self.form.ui.startButton.text(), "Start", "no start button")
        self.assertEqual(self.form.ui.stopButton.text(), "Stop", "no stop button")

    def testRoverDisplay(self):
        self.assertIsInstance(self.form.ui.tabWidget, PyQt5.QtWidgets.QTabWidget, "no tab widget")
        self.assertEqual(self.form.ui.tabWidget.count(), 3, "incorrect number of tabs")
        for index in range(self.form.ui.tabWidget.count()):
            self.assertIsInstance(self.form.ui.tabWidget.widget(index), PyQt5.QtWidgets.QWidget, "no tab")


if __name__ == "__main__":
    unittest.main()
