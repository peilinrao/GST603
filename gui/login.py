from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_loginWindow(object):
    def setupUi(self, loginWindow):
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
        self.userInput.returnPressed.connect(self.login)
        self.passInput.returnPressed.connect(self.login)

        self.retranslateUi(loginWindow)
        QtCore.QMetaObject.connectSlotsByName(loginWindow)

    def login(self):
        self.loginMsgLabel.setText("No user database")
        Username = self.userInput.text()
        Password = self.passInput.text()
        self.userInput.clear()
        self.passInput.clear()

        mainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(mainWindow)
        mainWindow.show()



    def retranslateUi(self, loginWindow):
        _translate = QtCore.QCoreApplication.translate
        loginWindow.setWindowTitle(_translate("loginWindow", "GST603"))
        self.passLabel.setText(_translate("loginWindow", "Password:"))
        self.userLabel.setText(_translate("loginWindow", "Username:"))
        self.registerButton.setText(_translate("loginWindow", "Register"))
        self.loginButton.setText(_translate("loginWindow", "Login"))



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    loginWindow = QtWidgets.QMainWindow()
    ui = Ui_loginWindow()
    ui.setupUi(loginWindow)
    loginWindow.show()
    sys.exit(app.exec_())
    
