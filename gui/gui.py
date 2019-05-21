from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from _thread import *
import socket

# global
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
io_lock = allocate_lock()

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("GST603")
        MainWindow.resize(577, 455)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setReadOnly(True)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.verticalLayout.addWidget(self.plainTextEdit)
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.lineEdit)
        MainWindow.setCentralWidget(self.centralwidget)

        self.lineEdit.returnPressed.connect(self.input)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        start_new_thread(self.serverThread, ())

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle("GST603")

    def input(self):
        self.plainTextEdit.verticalScrollBar().setValue(self.plainTextEdit.verticalScrollBar().maximum())
        self.plainTextEdit.insertPlainText(self.lineEdit.text() + '\n')
        self.lineEdit.clear()

    def printMSG(self, message):
        self.plainTextEdit.verticalScrollBar().setValue(self.plainTextEdit.verticalScrollBar().maximum())
        self.plainTextEdit.insertPlainText(message + '\n')

    def serverThread():
        while True:
            with io_lock:
                message = socks.recv(MSG_BUF_SIZE).decode()
                if message[0] != "\n" and message[0] != "\b" and message[0] != "\0":
                    self.printMSG(message)


class Ui_loginWindow(object):
    def setupRegister(self, registerWindow):
        registerWindow.setObjectName("registerWindow")
        registerWindow.resize(319, 422)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../Desktop/Gui/0577 - Icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        registerWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(registerWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.userFrame = QtWidgets.QFrame(self.centralwidget)
        self.userFrame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.userFrame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.userFrame.setObjectName("userFrame")
        self.gridLayout = QtWidgets.QGridLayout(self.userFrame)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 45, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 45, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 0, 2, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(48, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 1, 0, 1, 1)
        self.userLabel = QtWidgets.QLabel(self.userFrame)
        self.userLabel.setObjectName("userLabel")
        self.gridLayout.addWidget(self.userLabel, 1, 1, 1, 1)
        self.userInput = QtWidgets.QLineEdit(self.userFrame)
        self.userInput.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.userInput.setObjectName("userInput")
        self.gridLayout.addWidget(self.userInput, 1, 2, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(48, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 1, 3, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(20, 6, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem4, 2, 1, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(20, 6, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem5, 2, 2, 1, 1)
        spacerItem6 = QtWidgets.QSpacerItem(48, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem6, 3, 0, 1, 1)
        self.passLabel = QtWidgets.QLabel(self.userFrame)
        self.passLabel.setObjectName("passLabel")
        self.gridLayout.addWidget(self.passLabel, 3, 1, 1, 1)
        self.passInput = QtWidgets.QLineEdit(self.userFrame)
        self.passInput.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passInput.setObjectName("passInput")
        self.gridLayout.addWidget(self.passInput, 3, 2, 1, 1)
        spacerItem7 = QtWidgets.QSpacerItem(48, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem7, 3, 3, 1, 1)
        self.loginMsgLabel = QtWidgets.QLabel(self.userFrame)
        self.loginMsgLabel.setText("")
        self.loginMsgLabel.setObjectName("loginMsgLabel")
        self.gridLayout.addWidget(self.loginMsgLabel, 4, 1, 1, 1)
        spacerItem8 = QtWidgets.QSpacerItem(20, 75, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem8, 5, 1, 1, 1)
        spacerItem9 = QtWidgets.QSpacerItem(20, 75, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem9, 5, 2, 1, 1)
        self.verticalLayout.addWidget(self.userFrame)
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame.setObjectName("frame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.createButton = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.createButton.sizePolicy().hasHeightForWidth())
        self.createButton.setSizePolicy(sizePolicy)
        self.createButton.setMinimumSize(QtCore.QSize(150, 0))
        self.createButton.setMaximumSize(QtCore.QSize(300, 16777215))
        self.createButton.setObjectName("createButton")
        self.gridLayout_2.addWidget(self.createButton, 1, 1, 1, 1)
        spacerItem10 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem10, 0, 1, 1, 1)
        spacerItem11 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem11, 1, 0, 1, 1)
        spacerItem12 = QtWidgets.QSpacerItem(20, 48, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem12, 2, 1, 1, 1)
        spacerItem13 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem13, 1, 2, 1, 1)
        self.verticalLayout.addWidget(self.frame)
        registerWindow.setCentralWidget(self.centralwidget)

        self.createButton.clicked.connect(self.register)
        self.userInput.returnPressed.connect(self.register)
        self.passInput.returnPressed.connect(self.register)

        self.retranslateRegister(registerWindow)
        QtCore.QMetaObject.connectSlotsByName(registerWindow)

    def retranslateRegister(self, registerWindow):
        _translate = QtCore.QCoreApplication.translate
        registerWindow.setWindowTitle(_translate("registerWindow", "GST603"))
        self.userLabel.setText(_translate("registerWindow", "Username:"))
        self.passLabel.setText(_translate("registerWindow", "Password:"))
        self.createButton.setText(_translate("registerWindow", "Create New User!"))

    def setupLogin(self, loginWindow):
        loginWindow.setObjectName("loginWindow")
        loginWindow.resize(311, 422)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../Desktop/Gui/0577 - Icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        loginWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(loginWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.userFrame = QtWidgets.QFrame(self.centralwidget)
        self.userFrame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.userFrame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.userFrame.setObjectName("userFrame")
        self.gridLayout = QtWidgets.QGridLayout(self.userFrame)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(48, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(48, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 3, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(48, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 4, 3, 1, 1)
        self.passLabel = QtWidgets.QLabel(self.userFrame)
        self.passLabel.setObjectName("passLabel")
        self.gridLayout.addWidget(self.passLabel, 4, 1, 1, 1)
        self.passInput = QtWidgets.QLineEdit(self.userFrame)
        self.passInput.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passInput.setObjectName("passInput")
        self.gridLayout.addWidget(self.passInput, 4, 2, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 75, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem3, 6, 1, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(20, 75, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem4, 6, 2, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(20, 6, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem5, 2, 2, 1, 1)
        spacerItem6 = QtWidgets.QSpacerItem(20, 45, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem6, 0, 2, 1, 1)
        self.userInput = QtWidgets.QLineEdit(self.userFrame)
        self.userInput.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.userInput.setObjectName("userInput")
        self.gridLayout.addWidget(self.userInput, 1, 2, 1, 1)
        self.userLabel = QtWidgets.QLabel(self.userFrame)
        self.userLabel.setObjectName("userLabel")
        self.gridLayout.addWidget(self.userLabel, 1, 1, 1, 1)
        spacerItem7 = QtWidgets.QSpacerItem(20, 6, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem7, 2, 1, 1, 1)
        spacerItem8 = QtWidgets.QSpacerItem(20, 45, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem8, 0, 1, 1, 1)
        spacerItem9 = QtWidgets.QSpacerItem(48, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem9, 4, 0, 1, 1)
        self.loginMsgLabel = QtWidgets.QLabel(self.userFrame)
        self.loginMsgLabel.setText("")
        self.loginMsgLabel.setObjectName("loginMsgLabel")
        self.gridLayout.addWidget(self.loginMsgLabel, 5, 1, 1, 2)
        self.verticalLayout.addWidget(self.userFrame)
        self.buttonFrame = QtWidgets.QFrame(self.centralwidget)
        self.buttonFrame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.buttonFrame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.buttonFrame.setObjectName("buttonFrame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.buttonFrame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.registerButton = QtWidgets.QPushButton(self.buttonFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.registerButton.sizePolicy().hasHeightForWidth())
        self.registerButton.setSizePolicy(sizePolicy)
        self.registerButton.setMaximumSize(QtCore.QSize(108, 40))
        self.registerButton.setObjectName("registerButton")
        self.gridLayout_2.addWidget(self.registerButton, 1, 1, 1, 1)
        spacerItem10 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem10, 1, 4, 1, 1)
        self.loginButton = QtWidgets.QPushButton(self.buttonFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.loginButton.sizePolicy().hasHeightForWidth())
        self.loginButton.setSizePolicy(sizePolicy)
        self.loginButton.setMaximumSize(QtCore.QSize(108, 40))
        self.loginButton.setObjectName("loginButton")
        self.gridLayout_2.addWidget(self.loginButton, 1, 3, 1, 1)
        spacerItem11 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem11, 1, 0, 1, 1)
        spacerItem12 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem12, 2, 1, 1, 1)
        spacerItem13 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem13, 0, 1, 1, 1)
        spacerItem14 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem14, 1, 2, 1, 1)
        self.verticalLayout.addWidget(self.buttonFrame)
        loginWindow.setCentralWidget(self.centralwidget)

        self.loginButton.clicked.connect(self.login)
        self.registerButton.clicked.connect(self.showRegister)
        self.userInput.returnPressed.connect(self.login)
        self.passInput.returnPressed.connect(self.login)

        self.retranslateUi(loginWindow)
        QtCore.QMetaObject.connectSlotsByName(loginWindow)

    def showRegister(self):
        self.register = Ui_loginWindow()
        self.register.setupRegister(loginWindow)
        loginWindow.show()

    def register(self):
        return

    def login(self):
        Username = self.userInput.text()
        Password = self.passInput.text()
        self.userInput.clear()
        self.passInput.clear()

        loginWindow.hide()

        self.mainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.mainWindow)
        self.mainWindow.show()



    def retranslateUi(self, loginWindow):
        _translate = QtCore.QCoreApplication.translate
        loginWindow.setWindowTitle(_translate("loginWindow", "GST603"))
        self.passLabel.setText(_translate("loginWindow", "Password:"))
        self.userLabel.setText(_translate("loginWindow", "Username:"))
        self.registerButton.setText(_translate("loginWindow", "Register"))
        self.loginButton.setText(_translate("loginWindow", "Login"))




if __name__ == "__main__":
    IP_address = "192.168.29.168"
    Port = int("7000")
    server.connect((IP_address, Port))
    app = QtWidgets.QApplication(sys.argv)
    loginWindow = QtWidgets.QMainWindow()
    ui = Ui_loginWindow()
    ui.setupLogin(loginWindow)
    loginWindow.show()
    sys.exit(app.exec_())

"""
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Ui_loginWindow()
    window.openWindow()
    sys.exit(app.exec_())
"""
