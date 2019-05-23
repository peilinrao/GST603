from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QMutex, QMutexLocker
import socket
import select
import os
from os import listdir

# constants
FILE_NO_EXIST = "\b\b"
FILE_UPLOADING = "\0\0"
FILE_REQUEST = "\n\n"
EOF = "\0\0\0"
DONE = "\n\n\n"
FAIL = "\b\b\b"
NO_EXIST = "\b\0"
NEW_USR = "\0\b"
PASS_ERR = "\b"
FILE_REMOVE = "\b\0\b"
MSG_BUF_SIZE = 2048
PKG_SIZE = 4*2048
SIG_LENGTH = 128
STRFORMATSIZE = 37
BINFORMATSIZE = 33
FILEMODE = True
SERVER_MODE = False

# global
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
io_lock = QMutex()

class serverThread(QThread):
    change_value = pyqtSignal(str)

    def run(self):
        while True:
            with QMutexLocker(io_lock):
                sockets_list = [server]
                read_sockets, write_socket, error_socket = select.select(sockets_list, [], [], 0)
                for sock in read_sockets:
                    message = server.recv(MSG_BUF_SIZE).decode()
                    if message[0] != "\n" and message[0] != "\b" and message[0] != "\0":
                        self.change_value.emit(message)

class Ui_fileWindow(object):
    def setupfileWindow(self, fileWindow):
        fileWindow.setObjectName("fileWindow")
        fileWindow.resize(458, 390)
        self.centralwidget = QtWidgets.QWidget(fileWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.listWidget = QtWidgets.QListWidget(self.frame)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.listWidget)
        self.MSGlabel = QtWidgets.QLabel(self.frame)
        self.MSGlabel.setText("")
        self.MSGlabel.setObjectName("MSGlabel")
        self.verticalLayout.addWidget(self.MSGlabel)
        self.horizontalLayout.addWidget(self.frame)
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.okButton = QtWidgets.QPushButton(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.okButton.sizePolicy().hasHeightForWidth())
        self.okButton.setSizePolicy(sizePolicy)
        self.okButton.setMaximumSize(QtCore.QSize(120, 16777215))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(59, 176, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(59, 176, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(59, 176, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        self.okButton.setPalette(palette)
        self.okButton.setObjectName("okButton")
        self.gridLayout_2.addWidget(self.okButton, 0, 0, 1, 1)
        self.cancelButton = QtWidgets.QPushButton(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cancelButton.sizePolicy().hasHeightForWidth())
        self.cancelButton.setSizePolicy(sizePolicy)
        self.cancelButton.setMaximumSize(QtCore.QSize(120, 16777215))
        self.cancelButton.setObjectName("cancelButton")
        self.gridLayout_2.addWidget(self.cancelButton, 1, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 2, 0, 1, 1)
        self.horizontalLayout.addWidget(self.frame_2)
        fileWindow.setCentralWidget(self.centralwidget)

        self.cancelButton.clicked.connect(self.close())

        self.retranslateUi(fileWindow)
        QtCore.QMetaObject.connectSlotsByName(fileWindow)


    def fileHandle(self, instr):
        if instr == FILE_UPLOADING:
            self.setupSend()
        elif instr == FILE_REQUEST:
            self.receiveFile()
        else:
            self.removeFile()

    def setupSend(self):
        temp = listdir("Upfile")
        self.fileList.addItems(temp[1:])
        self.okButton.clicked.connect(self.sendFile)

    def sendFile(self):
        fileName = self.fileList.currentItem().text()
        temp = os.stat("Upfile/"+fileName)
        fileSize = temp.st_size
        try:
            f = open(fileName, "rb")
        except:
            self.MSGlabel.setText("File broken.")
            return

        with QMutexLocker(io_lock):
            server.send(FILE_UPLOADING.encode())
            server.recv(SIG_LENGTH)
            server.send(fileName.encode())
            server.recv(SIG_LENGTH)
            server.send(str(fileSize).encode())

            message = server.recv(SIG_LENGTH).decode()

            if message == FAIL:
                self.MSGlabel.setText("File name exists.")
                return
            elif message == FILE_REMOVE:
                server.send(DONE.encode())

            try:
                package = f.read(PKG_SIZE)
                while package:
                    server.send(package)
                    package = f.read(PKG_SIZE)
                self.close()
            except:
                self.MSGlabel.setText("Upload failed.")
                return

    def retranslatefileWindow(self, fileWindow):
        _translate = QtCore.QCoreApplication.translate
        fileWindow.setWindowTitle(_translate("fileWindow", "fileWindow"))
        self.okButton.setText(_translate("fileWindow", "Ok"))
        self.cancelButton.setText(_translate("fileWindow", "Cancel"))

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(577, 465)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.verticalLayout.addWidget(self.plainTextEdit)
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.lineEdit)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 577, 22))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.actionUpload = QtWidgets.QAction(MainWindow)
        self.actionUpload.setObjectName("actionUpload")
        self.actionDownload = QtWidgets.QAction(MainWindow)
        self.actionDownload.setObjectName("actionDownload")
        self.actionRemove = QtWidgets.QAction(MainWindow)
        self.actionRemove.setObjectName("actionRemove")
        self.menu.addAction(self.actionUpload)
        self.menu.addAction(self.actionDownload)
        self.menu.addAction(self.actionRemove)
        self.menubar.addAction(self.menu.menuAction())

        # events
        self.lineEdit.returnPressed.connect(self.input)
        self.actionUpload.triggered.connect(self.sendFile)
        self.actionDownload.triggered.connect(self.receiveFile)
        self.actionRemove.triggered.connect(self.removeFile)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.startInput()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle("GST603")

    def sendFile(self):
        self.fileWindow = QtWidgets.QMainWindow()
        self.fileW = Ui_fileWindow()
        self.fileW.setupfileWindow(self.fileWindow)
        self.fileWindow.show()

        self.fileInstr = pyqtSignal(str)
        self.fileInstr.connect(self.fileW.fileHandle)
        self.fileW.close.connect(self.closeFileWindow)
        self.fileInstr.emit(FILE_UPLOADING)

    def startInput(self):
        self.inthread = serverThread()
        self.inthread.change_value.connect(self.printMSG)
        self.inthread.start()

    def input(self):
        message = self.lineEdit.text()
        self.lineEdit.clear()
        self.plainTextEdit.verticalScrollBar().setValue(self.plainTextEdit.verticalScrollBar().maximum())
        self.plainTextEdit.insertPlainText("<You> " + message + '\n')

        with QMutexLocker(io_lock):
            server.send(message.encode())

    def printMSG(self, message):
        self.plainTextEdit.verticalScrollBar().setValue(self.plainTextEdit.verticalScrollBar().maximum())
        self.plainTextEdit.insertPlainText(message + '\n')



class Ui_loginWindow(object):
    def setupRegister(self, registerWindow):
        registerWindow.setObjectName("registerWindow")
        registerWindow.resize(311, 422)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../Desktop/Gui/0577 - Icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        registerWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(registerWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.userFrame = QtWidgets.QFrame(self.centralwidget)
        self.userFrame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.userFrame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.userFrame.setObjectName("userFrame")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.userFrame)
        self.gridLayout_3.setObjectName("gridLayout_3")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem1, 0, 2, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem2, 0, 0, 1, 1)
        self.loginMsgLabel = QtWidgets.QLabel(self.userFrame)
        self.loginMsgLabel.setText("")
        self.loginMsgLabel.setObjectName("loginMsgLabel")
        self.gridLayout_3.addWidget(self.loginMsgLabel, 1, 1, 1, 1)
        self.frame_2 = QtWidgets.QFrame(self.userFrame)
        self.frame_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout = QtWidgets.QGridLayout(self.frame_2)
        self.gridLayout.setObjectName("gridLayout")
        self.passInput = QtWidgets.QLineEdit(self.frame_2)
        self.passInput.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passInput.setObjectName("passInput")
        self.gridLayout.addWidget(self.passInput, 1, 1, 1, 1)
        self.userLabel = QtWidgets.QLabel(self.frame_2)
        self.userLabel.setObjectName("userLabel")
        self.gridLayout.addWidget(self.userLabel, 0, 0, 1, 1)
        self.passLabel = QtWidgets.QLabel(self.frame_2)
        self.passLabel.setObjectName("passLabel")
        self.gridLayout.addWidget(self.passLabel, 1, 0, 1, 1)
        self.userInput = QtWidgets.QLineEdit(self.frame_2)
        self.userInput.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.userInput.setObjectName("userInput")
        self.gridLayout.addWidget(self.userInput, 0, 1, 1, 1)
        self.gridLayout_3.addWidget(self.frame_2, 0, 1, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem3, 2, 1, 1, 1)
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
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem4, 0, 1, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem5, 1, 0, 1, 1)
        spacerItem6 = QtWidgets.QSpacerItem(20, 48, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem6, 2, 1, 1, 1)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem7, 1, 2, 1, 1)
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
        self.gridLayout_3 = QtWidgets.QGridLayout(self.userFrame)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.loginMsgLabel = QtWidgets.QLabel(self.userFrame)
        self.loginMsgLabel.setText("")
        self.loginMsgLabel.setObjectName("loginMsgLabel")
        self.gridLayout_3.addWidget(self.loginMsgLabel, 2, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem, 3, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem1, 1, 2, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem2, 1, 0, 1, 1)
        self.frame = QtWidgets.QFrame(self.userFrame)
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setObjectName("gridLayout")
        self.userLabel = QtWidgets.QLabel(self.frame)
        self.userLabel.setObjectName("userLabel")
        self.gridLayout.addWidget(self.userLabel, 0, 0, 1, 1)
        self.userInput = QtWidgets.QLineEdit(self.frame)
        self.userInput.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.userInput.setObjectName("userInput")
        self.gridLayout.addWidget(self.userInput, 0, 1, 1, 1)
        self.passLabel = QtWidgets.QLabel(self.frame)
        self.passLabel.setObjectName("passLabel")
        self.gridLayout.addWidget(self.passLabel, 1, 0, 1, 1)
        self.passInput = QtWidgets.QLineEdit(self.frame)
        self.passInput.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passInput.setObjectName("passInput")
        self.gridLayout.addWidget(self.passInput, 1, 1, 1, 1)
        self.gridLayout_3.addWidget(self.frame, 1, 1, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem3, 0, 1, 1, 1)
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
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem4, 1, 4, 1, 1)
        self.loginButton = QtWidgets.QPushButton(self.buttonFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.loginButton.sizePolicy().hasHeightForWidth())
        self.loginButton.setSizePolicy(sizePolicy)
        self.loginButton.setMaximumSize(QtCore.QSize(108, 40))
        self.loginButton.setObjectName("loginButton")
        self.gridLayout_2.addWidget(self.loginButton, 1, 3, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem5, 1, 0, 1, 1)
        spacerItem6 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem6, 2, 1, 1, 1)
        spacerItem7 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem7, 0, 1, 1, 1)
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem8, 1, 2, 1, 1)
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

        server.send((NEW_USR).encode())

    def register(self):
        usrName = self.userInput.text()
        password = self.passInput.text()
        self.userInput.clear()
        self.passInput.clear()

        if usrName == "" or password == "":
            self.loginMsgLabel.setText("Invalid Username or password!")
            return

        if usrName == ":S":
            self.loginMsgLabel.setText("This is an invalid Username!")
            return

        server.send((usrName + " " + password + "\n").encode())
        message = server.recv(200).decode()

        if message == FAIL:
            self.loginMsgLabel.setText("Username taken.")
            return

        loginWindow.hide()

        self.mainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.mainWindow)
        self.mainWindow.show()


    def login(self):
        usrName = self.userInput.text()
        password = self.passInput.text()
        self.userInput.clear()
        self.passInput.clear()

        if usrName == "" or password == "":
            self.loginMsgLabel.setText("Invalid Username or password!")
            return

        server.send((usrName + " " + password + "\n").encode())
        message = server.recv(200).decode()

        if message == PASS_ERR:
            self.loginMsgLabel.setText("Password incorrect")
            return
        elif message == NO_EXIST:
            self.loginMsgLabel.setText("User does not exist")
            return
        else:
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
