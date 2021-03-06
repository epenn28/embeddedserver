# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(482, 455)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralWidget)
        self.tabWidget.setGeometry(QtCore.QRect(140, 10, 311, 421))
        self.tabWidget.setObjectName("tabWidget")
        self.pacmanTab = QtWidgets.QWidget()
        self.pacmanTab.setObjectName("pacmanTab")
        self.layoutWidget = QtWidgets.QWidget(self.pacmanTab)
        self.layoutWidget.setGeometry(QtCore.QRect(50, 10, 213, 275))
        self.layoutWidget.setObjectName("layoutWidget")
        self.pacmanLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.pacmanLayout.setContentsMargins(11, 11, 11, 11)
        self.pacmanLayout.setSpacing(6)
        self.pacmanLayout.setObjectName("pacmanLayout")
        self.xValue = QtWidgets.QLineEdit(self.layoutWidget)
        self.xValue.setReadOnly(True)
        self.xValue.setObjectName("xValue")
        self.pacmanLayout.addWidget(self.xValue, 4, 1, 1, 1)
        self.ipLabel = QtWidgets.QLabel(self.layoutWidget)
        self.ipLabel.setObjectName("ipLabel")
        self.pacmanLayout.addWidget(self.ipLabel, 0, 0, 1, 1)
        self.ipValue = QtWidgets.QLineEdit(self.layoutWidget)
        self.ipValue.setReadOnly(True)
        self.ipValue.setObjectName("ipValue")
        self.pacmanLayout.addWidget(self.ipValue, 0, 1, 1, 1)
        self.forwardLabel = QtWidgets.QLabel(self.layoutWidget)
        self.forwardLabel.setObjectName("forwardLabel")
        self.pacmanLayout.addWidget(self.forwardLabel, 1, 0, 1, 1)
        self.forwardValue = QtWidgets.QLineEdit(self.layoutWidget)
        self.forwardValue.setReadOnly(True)
        self.forwardValue.setObjectName("forwardValue")
        self.pacmanLayout.addWidget(self.forwardValue, 1, 1, 1, 1)
        self.leftLabel = QtWidgets.QLabel(self.layoutWidget)
        self.leftLabel.setObjectName("leftLabel")
        self.pacmanLayout.addWidget(self.leftLabel, 2, 0, 1, 1)
        self.leftValue = QtWidgets.QLineEdit(self.layoutWidget)
        self.leftValue.setReadOnly(True)
        self.leftValue.setObjectName("leftValue")
        self.pacmanLayout.addWidget(self.leftValue, 2, 1, 1, 1)
        self.rightLabel = QtWidgets.QLabel(self.layoutWidget)
        self.rightLabel.setObjectName("rightLabel")
        self.pacmanLayout.addWidget(self.rightLabel, 3, 0, 1, 1)
        self.rightValue = QtWidgets.QLineEdit(self.layoutWidget)
        self.rightValue.setReadOnly(True)
        self.rightValue.setObjectName("rightValue")
        self.pacmanLayout.addWidget(self.rightValue, 3, 1, 1, 1)
        self.xLabel = QtWidgets.QLabel(self.layoutWidget)
        self.xLabel.setObjectName("xLabel")
        self.pacmanLayout.addWidget(self.xLabel, 4, 0, 1, 1)
        self.yLabel = QtWidgets.QLabel(self.layoutWidget)
        self.yLabel.setObjectName("yLabel")
        self.pacmanLayout.addWidget(self.yLabel, 5, 0, 1, 1)
        self.yValue = QtWidgets.QLineEdit(self.layoutWidget)
        self.yValue.setReadOnly(True)
        self.yValue.setObjectName("yValue")
        self.pacmanLayout.addWidget(self.yValue, 5, 1, 1, 1)
        self.headingLabel = QtWidgets.QLabel(self.layoutWidget)
        self.headingLabel.setObjectName("headingLabel")
        self.pacmanLayout.addWidget(self.headingLabel, 6, 0, 1, 1)
        self.headingValue = QtWidgets.QLineEdit(self.layoutWidget)
        self.headingValue.setReadOnly(True)
        self.headingValue.setObjectName("headingValue")
        self.pacmanLayout.addWidget(self.headingValue, 6, 1, 1, 1)
        self.commandLabel = QtWidgets.QLabel(self.layoutWidget)
        self.commandLabel.setObjectName("commandLabel")
        self.pacmanLayout.addWidget(self.commandLabel, 7, 0, 1, 1)
        self.commandValue = QtWidgets.QLineEdit(self.layoutWidget)
        self.commandValue.setReadOnly(True)
        self.commandValue.setObjectName("commandValue")
        self.pacmanLayout.addWidget(self.commandValue, 7, 1, 1, 1)
        self.irStatusLabel = QtWidgets.QLabel(self.pacmanTab)
        self.irStatusLabel.setGeometry(QtCore.QRect(10, 330, 51, 16))
        self.irStatusLabel.setObjectName("irStatusLabel")
        self.irStatusImage = QtWidgets.QLabel(self.pacmanTab)
        self.irStatusImage.setGeometry(QtCore.QRect(60, 300, 81, 81))
        self.irStatusImage.setFrameShape(QtWidgets.QFrame.Box)
        self.irStatusImage.setText("")
        self.irStatusImage.setObjectName("irStatusImage")
        self.lfStatusLabel = QtWidgets.QLabel(self.pacmanTab)
        self.lfStatusLabel.setGeometry(QtCore.QRect(160, 330, 51, 16))
        self.lfStatusLabel.setObjectName("lfStatusLabel")
        self.lfStatusImage = QtWidgets.QLabel(self.pacmanTab)
        self.lfStatusImage.setGeometry(QtCore.QRect(210, 300, 81, 81))
        self.lfStatusImage.setFrameShape(QtWidgets.QFrame.Box)
        self.lfStatusImage.setText("")
        self.lfStatusImage.setObjectName("lfStatusImage")
        self.tabWidget.addTab(self.pacmanTab, "")
        self.ghost1Tab = QtWidgets.QWidget()
        self.ghost1Tab.setObjectName("ghost1Tab")
        self.layoutWidget1 = QtWidgets.QWidget(self.ghost1Tab)
        self.layoutWidget1.setGeometry(QtCore.QRect(50, 10, 213, 275))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.ghost1Layout = QtWidgets.QGridLayout(self.layoutWidget1)
        self.ghost1Layout.setContentsMargins(11, 11, 11, 11)
        self.ghost1Layout.setSpacing(6)
        self.ghost1Layout.setObjectName("ghost1Layout")
        self.ipLabel_2 = QtWidgets.QLabel(self.layoutWidget1)
        self.ipLabel_2.setObjectName("ipLabel_2")
        self.ghost1Layout.addWidget(self.ipLabel_2, 0, 0, 1, 1)
        self.ipValue_2 = QtWidgets.QLineEdit(self.layoutWidget1)
        self.ipValue_2.setReadOnly(True)
        self.ipValue_2.setObjectName("ipValue_2")
        self.ghost1Layout.addWidget(self.ipValue_2, 0, 1, 1, 1)
        self.forwardLabel_2 = QtWidgets.QLabel(self.layoutWidget1)
        self.forwardLabel_2.setObjectName("forwardLabel_2")
        self.ghost1Layout.addWidget(self.forwardLabel_2, 1, 0, 1, 1)
        self.forwardValue_2 = QtWidgets.QLineEdit(self.layoutWidget1)
        self.forwardValue_2.setReadOnly(True)
        self.forwardValue_2.setObjectName("forwardValue_2")
        self.ghost1Layout.addWidget(self.forwardValue_2, 1, 1, 1, 1)
        self.leftLabel_2 = QtWidgets.QLabel(self.layoutWidget1)
        self.leftLabel_2.setObjectName("leftLabel_2")
        self.ghost1Layout.addWidget(self.leftLabel_2, 2, 0, 1, 1)
        self.leftValue_2 = QtWidgets.QLineEdit(self.layoutWidget1)
        self.leftValue_2.setReadOnly(True)
        self.leftValue_2.setObjectName("leftValue_2")
        self.ghost1Layout.addWidget(self.leftValue_2, 2, 1, 1, 1)
        self.rightLabel_2 = QtWidgets.QLabel(self.layoutWidget1)
        self.rightLabel_2.setObjectName("rightLabel_2")
        self.ghost1Layout.addWidget(self.rightLabel_2, 3, 0, 1, 1)
        self.rightValue_2 = QtWidgets.QLineEdit(self.layoutWidget1)
        self.rightValue_2.setReadOnly(True)
        self.rightValue_2.setObjectName("rightValue_2")
        self.ghost1Layout.addWidget(self.rightValue_2, 3, 1, 1, 1)
        self.xLabel_2 = QtWidgets.QLabel(self.layoutWidget1)
        self.xLabel_2.setObjectName("xLabel_2")
        self.ghost1Layout.addWidget(self.xLabel_2, 4, 0, 1, 1)
        self.xValue_2 = QtWidgets.QLineEdit(self.layoutWidget1)
        self.xValue_2.setReadOnly(True)
        self.xValue_2.setObjectName("xValue_2")
        self.ghost1Layout.addWidget(self.xValue_2, 4, 1, 1, 1)
        self.yLabel_2 = QtWidgets.QLabel(self.layoutWidget1)
        self.yLabel_2.setObjectName("yLabel_2")
        self.ghost1Layout.addWidget(self.yLabel_2, 5, 0, 1, 1)
        self.yValue_2 = QtWidgets.QLineEdit(self.layoutWidget1)
        self.yValue_2.setReadOnly(True)
        self.yValue_2.setObjectName("yValue_2")
        self.ghost1Layout.addWidget(self.yValue_2, 5, 1, 1, 1)
        self.headingLabel_2 = QtWidgets.QLabel(self.layoutWidget1)
        self.headingLabel_2.setObjectName("headingLabel_2")
        self.ghost1Layout.addWidget(self.headingLabel_2, 6, 0, 1, 1)
        self.headingValue_2 = QtWidgets.QLineEdit(self.layoutWidget1)
        self.headingValue_2.setReadOnly(True)
        self.headingValue_2.setObjectName("headingValue_2")
        self.ghost1Layout.addWidget(self.headingValue_2, 6, 1, 1, 1)
        self.commandLabel_2 = QtWidgets.QLabel(self.layoutWidget1)
        self.commandLabel_2.setObjectName("commandLabel_2")
        self.ghost1Layout.addWidget(self.commandLabel_2, 7, 0, 1, 1)
        self.commandValue_2 = QtWidgets.QLineEdit(self.layoutWidget1)
        self.commandValue_2.setReadOnly(True)
        self.commandValue_2.setObjectName("commandValue_2")
        self.ghost1Layout.addWidget(self.commandValue_2, 7, 1, 1, 1)
        self.irStatusLabel_2 = QtWidgets.QLabel(self.ghost1Tab)
        self.irStatusLabel_2.setGeometry(QtCore.QRect(10, 330, 51, 16))
        self.irStatusLabel_2.setObjectName("irStatusLabel_2")
        self.irStatusImage_2 = QtWidgets.QLabel(self.ghost1Tab)
        self.irStatusImage_2.setGeometry(QtCore.QRect(60, 300, 81, 81))
        self.irStatusImage_2.setFrameShape(QtWidgets.QFrame.Box)
        self.irStatusImage_2.setText("")
        self.irStatusImage_2.setObjectName("irStatusImage_2")
        self.lfStatusLabel_2 = QtWidgets.QLabel(self.ghost1Tab)
        self.lfStatusLabel_2.setGeometry(QtCore.QRect(160, 330, 51, 16))
        self.lfStatusLabel_2.setObjectName("lfStatusLabel_2")
        self.lfStatusImage_2 = QtWidgets.QLabel(self.ghost1Tab)
        self.lfStatusImage_2.setGeometry(QtCore.QRect(210, 300, 81, 81))
        self.lfStatusImage_2.setFrameShape(QtWidgets.QFrame.Box)
        self.lfStatusImage_2.setText("")
        self.lfStatusImage_2.setObjectName("lfStatusImage_2")
        self.tabWidget.addTab(self.ghost1Tab, "")
        self.ghost2Tab = QtWidgets.QWidget()
        self.ghost2Tab.setObjectName("ghost2Tab")
        self.layoutWidget2 = QtWidgets.QWidget(self.ghost2Tab)
        self.layoutWidget2.setGeometry(QtCore.QRect(50, 10, 213, 275))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.ghost2Layout = QtWidgets.QGridLayout(self.layoutWidget2)
        self.ghost2Layout.setContentsMargins(11, 11, 11, 11)
        self.ghost2Layout.setSpacing(6)
        self.ghost2Layout.setObjectName("ghost2Layout")
        self.ipLabel_3 = QtWidgets.QLabel(self.layoutWidget2)
        self.ipLabel_3.setObjectName("ipLabel_3")
        self.ghost2Layout.addWidget(self.ipLabel_3, 0, 0, 1, 1)
        self.ipValue_3 = QtWidgets.QLineEdit(self.layoutWidget2)
        self.ipValue_3.setReadOnly(True)
        self.ipValue_3.setObjectName("ipValue_3")
        self.ghost2Layout.addWidget(self.ipValue_3, 0, 1, 1, 1)
        self.forwardLabel_3 = QtWidgets.QLabel(self.layoutWidget2)
        self.forwardLabel_3.setObjectName("forwardLabel_3")
        self.ghost2Layout.addWidget(self.forwardLabel_3, 1, 0, 1, 1)
        self.forwardValue_3 = QtWidgets.QLineEdit(self.layoutWidget2)
        self.forwardValue_3.setReadOnly(True)
        self.forwardValue_3.setObjectName("forwardValue_3")
        self.ghost2Layout.addWidget(self.forwardValue_3, 1, 1, 1, 1)
        self.leftLabel_3 = QtWidgets.QLabel(self.layoutWidget2)
        self.leftLabel_3.setObjectName("leftLabel_3")
        self.ghost2Layout.addWidget(self.leftLabel_3, 2, 0, 1, 1)
        self.leftValue_3 = QtWidgets.QLineEdit(self.layoutWidget2)
        self.leftValue_3.setReadOnly(True)
        self.leftValue_3.setObjectName("leftValue_3")
        self.ghost2Layout.addWidget(self.leftValue_3, 2, 1, 1, 1)
        self.rightLabel_3 = QtWidgets.QLabel(self.layoutWidget2)
        self.rightLabel_3.setObjectName("rightLabel_3")
        self.ghost2Layout.addWidget(self.rightLabel_3, 3, 0, 1, 1)
        self.rightValue_3 = QtWidgets.QLineEdit(self.layoutWidget2)
        self.rightValue_3.setReadOnly(True)
        self.rightValue_3.setObjectName("rightValue_3")
        self.ghost2Layout.addWidget(self.rightValue_3, 3, 1, 1, 1)
        self.xLabel_3 = QtWidgets.QLabel(self.layoutWidget2)
        self.xLabel_3.setObjectName("xLabel_3")
        self.ghost2Layout.addWidget(self.xLabel_3, 4, 0, 1, 1)
        self.xValue_3 = QtWidgets.QLineEdit(self.layoutWidget2)
        self.xValue_3.setReadOnly(True)
        self.xValue_3.setObjectName("xValue_3")
        self.ghost2Layout.addWidget(self.xValue_3, 4, 1, 1, 1)
        self.yLabel_3 = QtWidgets.QLabel(self.layoutWidget2)
        self.yLabel_3.setObjectName("yLabel_3")
        self.ghost2Layout.addWidget(self.yLabel_3, 5, 0, 1, 1)
        self.yValue_3 = QtWidgets.QLineEdit(self.layoutWidget2)
        self.yValue_3.setReadOnly(True)
        self.yValue_3.setObjectName("yValue_3")
        self.ghost2Layout.addWidget(self.yValue_3, 5, 1, 1, 1)
        self.headingLabel_3 = QtWidgets.QLabel(self.layoutWidget2)
        self.headingLabel_3.setObjectName("headingLabel_3")
        self.ghost2Layout.addWidget(self.headingLabel_3, 6, 0, 1, 1)
        self.headingValue_3 = QtWidgets.QLineEdit(self.layoutWidget2)
        self.headingValue_3.setReadOnly(True)
        self.headingValue_3.setObjectName("headingValue_3")
        self.ghost2Layout.addWidget(self.headingValue_3, 6, 1, 1, 1)
        self.commandLabel_3 = QtWidgets.QLabel(self.layoutWidget2)
        self.commandLabel_3.setObjectName("commandLabel_3")
        self.ghost2Layout.addWidget(self.commandLabel_3, 7, 0, 1, 1)
        self.commandValue_3 = QtWidgets.QLineEdit(self.layoutWidget2)
        self.commandValue_3.setReadOnly(True)
        self.commandValue_3.setObjectName("commandValue_3")
        self.ghost2Layout.addWidget(self.commandValue_3, 7, 1, 1, 1)
        self.irStatusLabel_3 = QtWidgets.QLabel(self.ghost2Tab)
        self.irStatusLabel_3.setGeometry(QtCore.QRect(10, 330, 51, 16))
        self.irStatusLabel_3.setObjectName("irStatusLabel_3")
        self.irStatusImage_3 = QtWidgets.QLabel(self.ghost2Tab)
        self.irStatusImage_3.setGeometry(QtCore.QRect(60, 300, 81, 81))
        self.irStatusImage_3.setFrameShape(QtWidgets.QFrame.Box)
        self.irStatusImage_3.setText("")
        self.irStatusImage_3.setObjectName("irStatusImage_3")
        self.lfStatusLabel_3 = QtWidgets.QLabel(self.ghost2Tab)
        self.lfStatusLabel_3.setGeometry(QtCore.QRect(160, 330, 51, 16))
        self.lfStatusLabel_3.setObjectName("lfStatusLabel_3")
        self.lfStatusImage_3 = QtWidgets.QLabel(self.ghost2Tab)
        self.lfStatusImage_3.setGeometry(QtCore.QRect(210, 300, 81, 81))
        self.lfStatusImage_3.setFrameShape(QtWidgets.QFrame.Box)
        self.lfStatusImage_3.setText("")
        self.lfStatusImage_3.setObjectName("lfStatusImage_3")
        self.tabWidget.addTab(self.ghost2Tab, "")
        self.manualTab = QtWidgets.QWidget()
        self.manualTab.setObjectName("manualTab")
        self.layoutWidget3 = QtWidgets.QWidget(self.manualTab)
        self.layoutWidget3.setGeometry(QtCore.QRect(40, 30, 231, 341))
        self.layoutWidget3.setObjectName("layoutWidget3")
        self.manualLayout = QtWidgets.QGridLayout(self.layoutWidget3)
        self.manualLayout.setContentsMargins(11, 11, 11, 11)
        self.manualLayout.setSpacing(6)
        self.manualLayout.setObjectName("manualLayout")
        self.ghost1AdjustLeftButton = QtWidgets.QPushButton(self.layoutWidget3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ghost1AdjustLeftButton.sizePolicy().hasHeightForWidth())
        self.ghost1AdjustLeftButton.setSizePolicy(sizePolicy)
        self.ghost1AdjustLeftButton.setMaximumSize(QtCore.QSize(31, 21))
        self.ghost1AdjustLeftButton.setObjectName("ghost1AdjustLeftButton")
        self.manualLayout.addWidget(self.ghost1AdjustLeftButton, 3, 1, 1, 1)
        self.pacAdjustLeftButton = QtWidgets.QPushButton(self.layoutWidget3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pacAdjustLeftButton.sizePolicy().hasHeightForWidth())
        self.pacAdjustLeftButton.setSizePolicy(sizePolicy)
        self.pacAdjustLeftButton.setMaximumSize(QtCore.QSize(31, 21))
        self.pacAdjustLeftButton.setObjectName("pacAdjustLeftButton")
        self.manualLayout.addWidget(self.pacAdjustLeftButton, 0, 1, 1, 1)
        self.pacUpButton = QtWidgets.QPushButton(self.layoutWidget3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pacUpButton.sizePolicy().hasHeightForWidth())
        self.pacUpButton.setSizePolicy(sizePolicy)
        self.pacUpButton.setMaximumSize(QtCore.QSize(31, 21))
        self.pacUpButton.setObjectName("pacUpButton")
        self.manualLayout.addWidget(self.pacUpButton, 0, 2, 1, 1)
        self.ghost1LeftButton = QtWidgets.QPushButton(self.layoutWidget3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ghost1LeftButton.sizePolicy().hasHeightForWidth())
        self.ghost1LeftButton.setSizePolicy(sizePolicy)
        self.ghost1LeftButton.setMaximumSize(QtCore.QSize(31, 21))
        self.ghost1LeftButton.setObjectName("ghost1LeftButton")
        self.manualLayout.addWidget(self.ghost1LeftButton, 4, 1, 1, 1)
        self.ghost1RightButton = QtWidgets.QPushButton(self.layoutWidget3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ghost1RightButton.sizePolicy().hasHeightForWidth())
        self.ghost1RightButton.setSizePolicy(sizePolicy)
        self.ghost1RightButton.setMaximumSize(QtCore.QSize(31, 21))
        self.ghost1RightButton.setObjectName("ghost1RightButton")
        self.manualLayout.addWidget(self.ghost1RightButton, 4, 3, 1, 1)
        self.ghost2AdjustLeftButton = QtWidgets.QPushButton(self.layoutWidget3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ghost2AdjustLeftButton.sizePolicy().hasHeightForWidth())
        self.ghost2AdjustLeftButton.setSizePolicy(sizePolicy)
        self.ghost2AdjustLeftButton.setMaximumSize(QtCore.QSize(31, 21))
        self.ghost2AdjustLeftButton.setObjectName("ghost2AdjustLeftButton")
        self.manualLayout.addWidget(self.ghost2AdjustLeftButton, 6, 1, 1, 1)
        self.ghost2UpButton = QtWidgets.QPushButton(self.layoutWidget3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ghost2UpButton.sizePolicy().hasHeightForWidth())
        self.ghost2UpButton.setSizePolicy(sizePolicy)
        self.ghost2UpButton.setMaximumSize(QtCore.QSize(31, 21))
        self.ghost2UpButton.setObjectName("ghost2UpButton")
        self.manualLayout.addWidget(self.ghost2UpButton, 6, 2, 1, 1)
        self.ghost2AdjustRightButton = QtWidgets.QPushButton(self.layoutWidget3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ghost2AdjustRightButton.sizePolicy().hasHeightForWidth())
        self.ghost2AdjustRightButton.setSizePolicy(sizePolicy)
        self.ghost2AdjustRightButton.setMaximumSize(QtCore.QSize(31, 21))
        self.ghost2AdjustRightButton.setObjectName("ghost2AdjustRightButton")
        self.manualLayout.addWidget(self.ghost2AdjustRightButton, 6, 3, 1, 1)
        self.ghost2LeftButton = QtWidgets.QPushButton(self.layoutWidget3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ghost2LeftButton.sizePolicy().hasHeightForWidth())
        self.ghost2LeftButton.setSizePolicy(sizePolicy)
        self.ghost2LeftButton.setMaximumSize(QtCore.QSize(31, 21))
        self.ghost2LeftButton.setObjectName("ghost2LeftButton")
        self.manualLayout.addWidget(self.ghost2LeftButton, 7, 1, 1, 1)
        self.ghost2RightButton = QtWidgets.QPushButton(self.layoutWidget3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ghost2RightButton.sizePolicy().hasHeightForWidth())
        self.ghost2RightButton.setSizePolicy(sizePolicy)
        self.ghost2RightButton.setMaximumSize(QtCore.QSize(31, 21))
        self.ghost2RightButton.setObjectName("ghost2RightButton")
        self.manualLayout.addWidget(self.ghost2RightButton, 7, 3, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.manualLayout.addItem(spacerItem, 2, 0, 1, 1)
        self.ghost1UpButton = QtWidgets.QPushButton(self.layoutWidget3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ghost1UpButton.sizePolicy().hasHeightForWidth())
        self.ghost1UpButton.setSizePolicy(sizePolicy)
        self.ghost1UpButton.setMaximumSize(QtCore.QSize(31, 21))
        self.ghost1UpButton.setObjectName("ghost1UpButton")
        self.manualLayout.addWidget(self.ghost1UpButton, 3, 2, 1, 1)
        self.ghost1ControlLabel = QtWidgets.QLabel(self.layoutWidget3)
        self.ghost1ControlLabel.setObjectName("ghost1ControlLabel")
        self.manualLayout.addWidget(self.ghost1ControlLabel, 3, 0, 2, 1)
        self.pacAdjustRightButton = QtWidgets.QPushButton(self.layoutWidget3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pacAdjustRightButton.sizePolicy().hasHeightForWidth())
        self.pacAdjustRightButton.setSizePolicy(sizePolicy)
        self.pacAdjustRightButton.setMaximumSize(QtCore.QSize(31, 21))
        self.pacAdjustRightButton.setObjectName("pacAdjustRightButton")
        self.manualLayout.addWidget(self.pacAdjustRightButton, 0, 3, 1, 1)
        self.pacLeftButton = QtWidgets.QPushButton(self.layoutWidget3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pacLeftButton.sizePolicy().hasHeightForWidth())
        self.pacLeftButton.setSizePolicy(sizePolicy)
        self.pacLeftButton.setMaximumSize(QtCore.QSize(31, 21))
        self.pacLeftButton.setObjectName("pacLeftButton")
        self.manualLayout.addWidget(self.pacLeftButton, 1, 1, 1, 1)
        self.pacControlLabel = QtWidgets.QLabel(self.layoutWidget3)
        self.pacControlLabel.setObjectName("pacControlLabel")
        self.manualLayout.addWidget(self.pacControlLabel, 0, 0, 2, 1)
        self.pacRightButton = QtWidgets.QPushButton(self.layoutWidget3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pacRightButton.sizePolicy().hasHeightForWidth())
        self.pacRightButton.setSizePolicy(sizePolicy)
        self.pacRightButton.setMaximumSize(QtCore.QSize(31, 21))
        self.pacRightButton.setObjectName("pacRightButton")
        self.manualLayout.addWidget(self.pacRightButton, 1, 3, 1, 1)
        self.ghost1AdjustRightButton = QtWidgets.QPushButton(self.layoutWidget3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ghost1AdjustRightButton.sizePolicy().hasHeightForWidth())
        self.ghost1AdjustRightButton.setSizePolicy(sizePolicy)
        self.ghost1AdjustRightButton.setMaximumSize(QtCore.QSize(31, 21))
        self.ghost1AdjustRightButton.setObjectName("ghost1AdjustRightButton")
        self.manualLayout.addWidget(self.ghost1AdjustRightButton, 3, 3, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.manualLayout.addItem(spacerItem1, 5, 0, 1, 1)
        self.ghost2ControlLabel = QtWidgets.QLabel(self.layoutWidget3)
        self.ghost2ControlLabel.setObjectName("ghost2ControlLabel")
        self.manualLayout.addWidget(self.ghost2ControlLabel, 6, 0, 2, 1)
        self.pacDownButton = QtWidgets.QPushButton(self.layoutWidget3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pacDownButton.sizePolicy().hasHeightForWidth())
        self.pacDownButton.setSizePolicy(sizePolicy)
        self.pacDownButton.setMaximumSize(QtCore.QSize(31, 21))
        self.pacDownButton.setObjectName("pacDownButton")
        self.manualLayout.addWidget(self.pacDownButton, 1, 2, 1, 1)
        self.ghost1DownButton = QtWidgets.QPushButton(self.layoutWidget3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ghost1DownButton.sizePolicy().hasHeightForWidth())
        self.ghost1DownButton.setSizePolicy(sizePolicy)
        self.ghost1DownButton.setMaximumSize(QtCore.QSize(31, 21))
        self.ghost1DownButton.setObjectName("ghost1DownButton")
        self.manualLayout.addWidget(self.ghost1DownButton, 4, 2, 1, 1)
        self.ghost2DownButton = QtWidgets.QPushButton(self.layoutWidget3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ghost2DownButton.sizePolicy().hasHeightForWidth())
        self.ghost2DownButton.setSizePolicy(sizePolicy)
        self.ghost2DownButton.setMaximumSize(QtCore.QSize(31, 21))
        self.ghost2DownButton.setObjectName("ghost2DownButton")
        self.manualLayout.addWidget(self.ghost2DownButton, 7, 2, 1, 1)
        self.tabWidget.addTab(self.manualTab, "")
        self.startButton = QtWidgets.QPushButton(self.centralWidget)
        self.startButton.setGeometry(QtCore.QRect(30, 130, 80, 25))
        self.startButton.setObjectName("startButton")
        self.stopButton = QtWidgets.QPushButton(self.centralWidget)
        self.stopButton.setGeometry(QtCore.QRect(30, 190, 80, 25))
        self.stopButton.setObjectName("stopButton")
        self.statusLabel = QtWidgets.QLabel(self.centralWidget)
        self.statusLabel.setGeometry(QtCore.QRect(30, 250, 71, 16))
        self.statusLabel.setObjectName("statusLabel")
        self.statusValue = QtWidgets.QLabel(self.centralWidget)
        self.statusValue.setGeometry(QtCore.QRect(16, 270, 111, 20))
        self.statusValue.setAlignment(QtCore.Qt.AlignCenter)
        self.statusValue.setObjectName("statusValue")
        self.overrideButton = QtWidgets.QPushButton(self.centralWidget)
        self.overrideButton.setGeometry(QtCore.QRect(20, 330, 101, 21))
        self.overrideButton.setObjectName("overrideButton")
        self.automaticButton = QtWidgets.QPushButton(self.centralWidget)
        self.automaticButton.setGeometry(QtCore.QRect(20, 370, 101, 21))
        self.automaticButton.setObjectName("automaticButton")
        self.scoreLabel = QtWidgets.QLabel(self.centralWidget)
        self.scoreLabel.setGeometry(QtCore.QRect(30, 30, 71, 16))
        self.scoreLabel.setObjectName("scoreLabel")
        self.scoreValue = QtWidgets.QLabel(self.centralWidget)
        self.scoreValue.setGeometry(QtCore.QRect(10, 50, 111, 51))
        self.scoreValue.setAlignment(QtCore.Qt.AlignCenter)
        self.scoreValue.setObjectName("scoreValue")
        MainWindow.setCentralWidget(self.centralWidget)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.tabWidget, self.ipValue)
        MainWindow.setTabOrder(self.ipValue, self.startButton)
        MainWindow.setTabOrder(self.startButton, self.stopButton)
        MainWindow.setTabOrder(self.stopButton, self.forwardValue)
        MainWindow.setTabOrder(self.forwardValue, self.leftValue)
        MainWindow.setTabOrder(self.leftValue, self.rightValue)
        MainWindow.setTabOrder(self.rightValue, self.yValue)
        MainWindow.setTabOrder(self.yValue, self.headingValue)
        MainWindow.setTabOrder(self.headingValue, self.xValue)
        MainWindow.setTabOrder(self.xValue, self.commandValue)
        MainWindow.setTabOrder(self.commandValue, self.rightValue_2)
        MainWindow.setTabOrder(self.rightValue_2, self.ipValue_2)
        MainWindow.setTabOrder(self.ipValue_2, self.headingValue_2)
        MainWindow.setTabOrder(self.headingValue_2, self.yValue_2)
        MainWindow.setTabOrder(self.yValue_2, self.xValue_2)
        MainWindow.setTabOrder(self.xValue_2, self.commandValue_2)
        MainWindow.setTabOrder(self.commandValue_2, self.leftValue_2)
        MainWindow.setTabOrder(self.leftValue_2, self.forwardValue_2)
        MainWindow.setTabOrder(self.forwardValue_2, self.rightValue_3)
        MainWindow.setTabOrder(self.rightValue_3, self.ipValue_3)
        MainWindow.setTabOrder(self.ipValue_3, self.headingValue_3)
        MainWindow.setTabOrder(self.headingValue_3, self.yValue_3)
        MainWindow.setTabOrder(self.yValue_3, self.xValue_3)
        MainWindow.setTabOrder(self.xValue_3, self.commandValue_3)
        MainWindow.setTabOrder(self.commandValue_3, self.leftValue_3)
        MainWindow.setTabOrder(self.leftValue_3, self.forwardValue_3)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Pac-Man"))
        self.ipLabel.setText(_translate("MainWindow", "<html><head/><body><p>IP address:</p></body></html>"))
        self.forwardLabel.setText(_translate("MainWindow", "<html><head/><body><p>Forward IR:</p></body></html>"))
        self.leftLabel.setText(_translate("MainWindow", "<html><head/><body><p>Left IR:</p></body></html>"))
        self.rightLabel.setText(_translate("MainWindow", "<html><head/><body><p>Right IR:</p></body></html>"))
        self.xLabel.setText(_translate("MainWindow", "<html><head/><body><p>X-coordinate:</p></body></html>"))
        self.yLabel.setText(_translate("MainWindow", "<html><head/><body><p>Y-coordinate:</p></body></html>"))
        self.headingLabel.setText(_translate("MainWindow", "<html><head/><body><p>Heading:</p></body></html>"))
        self.commandLabel.setText(_translate("MainWindow", "<html><head/><body><p>Current command:</p></body></html>"))
        self.irStatusLabel.setText(_translate("MainWindow", "IR status:"))
        self.lfStatusLabel.setText(_translate("MainWindow", "LF status:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.pacmanTab), _translate("MainWindow", "Pac-Man"))
        self.ipLabel_2.setText(_translate("MainWindow", "<html><head/><body><p>IP address:</p></body></html>"))
        self.forwardLabel_2.setText(_translate("MainWindow", "<html><head/><body><p>Forward IR:</p></body></html>"))
        self.leftLabel_2.setText(_translate("MainWindow", "<html><head/><body><p>Left IR:</p></body></html>"))
        self.rightLabel_2.setText(_translate("MainWindow", "<html><head/><body><p>Right IR:</p></body></html>"))
        self.xLabel_2.setText(_translate("MainWindow", "<html><head/><body><p>X-coordinate:</p></body></html>"))
        self.yLabel_2.setText(_translate("MainWindow", "<html><head/><body><p>Y-coordinate:</p></body></html>"))
        self.headingLabel_2.setText(_translate("MainWindow", "<html><head/><body><p>Heading:</p></body></html>"))
        self.commandLabel_2.setText(_translate("MainWindow", "<html><head/><body><p>Current command:</p></body></html>"))
        self.irStatusLabel_2.setText(_translate("MainWindow", "IR status:"))
        self.lfStatusLabel_2.setText(_translate("MainWindow", "LF status:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.ghost1Tab), _translate("MainWindow", "Ghost 1"))
        self.ipLabel_3.setText(_translate("MainWindow", "<html><head/><body><p>IP address:</p></body></html>"))
        self.forwardLabel_3.setText(_translate("MainWindow", "<html><head/><body><p>Forward IR:</p></body></html>"))
        self.leftLabel_3.setText(_translate("MainWindow", "<html><head/><body><p>Left IR:</p></body></html>"))
        self.rightLabel_3.setText(_translate("MainWindow", "<html><head/><body><p>Right IR:</p></body></html>"))
        self.xLabel_3.setText(_translate("MainWindow", "<html><head/><body><p>X-coordinate:</p></body></html>"))
        self.yLabel_3.setText(_translate("MainWindow", "<html><head/><body><p>Y-coordinate:</p></body></html>"))
        self.headingLabel_3.setText(_translate("MainWindow", "<html><head/><body><p>Heading:</p></body></html>"))
        self.commandLabel_3.setText(_translate("MainWindow", "<html><head/><body><p>Current command:</p></body></html>"))
        self.irStatusLabel_3.setText(_translate("MainWindow", "IR status:"))
        self.lfStatusLabel_3.setText(_translate("MainWindow", "LF status:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.ghost2Tab), _translate("MainWindow", "Ghost 2"))
        self.ghost1AdjustLeftButton.setText(_translate("MainWindow", "↖"))
        self.pacAdjustLeftButton.setText(_translate("MainWindow", "↖"))
        self.pacUpButton.setText(_translate("MainWindow", "^"))
        self.ghost1LeftButton.setText(_translate("MainWindow", "<"))
        self.ghost1RightButton.setText(_translate("MainWindow", ">"))
        self.ghost2AdjustLeftButton.setText(_translate("MainWindow", "↖"))
        self.ghost2UpButton.setText(_translate("MainWindow", "^"))
        self.ghost2AdjustRightButton.setText(_translate("MainWindow", "↗"))
        self.ghost2LeftButton.setText(_translate("MainWindow", "<"))
        self.ghost2RightButton.setText(_translate("MainWindow", ">"))
        self.ghost1UpButton.setText(_translate("MainWindow", "^"))
        self.ghost1ControlLabel.setText(_translate("MainWindow", "Ghost 1"))
        self.pacAdjustRightButton.setText(_translate("MainWindow", "↗"))
        self.pacLeftButton.setText(_translate("MainWindow", "<"))
        self.pacControlLabel.setText(_translate("MainWindow", "Pac-Man"))
        self.pacRightButton.setText(_translate("MainWindow", ">"))
        self.ghost1AdjustRightButton.setText(_translate("MainWindow", "↗"))
        self.ghost2ControlLabel.setText(_translate("MainWindow", "Ghost 2"))
        self.pacDownButton.setText(_translate("MainWindow", "V"))
        self.ghost1DownButton.setText(_translate("MainWindow", "V"))
        self.ghost2DownButton.setText(_translate("MainWindow", "V"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.manualTab), _translate("MainWindow", "Manual Control"))
        self.startButton.setText(_translate("MainWindow", "Start"))
        self.stopButton.setText(_translate("MainWindow", "Stop"))
        self.statusLabel.setText(_translate("MainWindow", "Server status:"))
        self.statusValue.setText(_translate("MainWindow", "Inititalizing"))
        self.overrideButton.setText(_translate("MainWindow", "Manual Override"))
        self.automaticButton.setText(_translate("MainWindow", "Automatic Mode"))
        self.scoreLabel.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">Score:</p></body></html>"))
        self.scoreValue.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt;\">0</span></p></body></html>"))

