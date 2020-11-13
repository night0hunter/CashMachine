import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5 import uic

class MainWindow(QtWidgets.QWidget):

    switch_auth = QtCore.pyqtSignal()
    switch_reg = QtCore.pyqtSignal()

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        uic.loadUi('./ui/mainWindow.ui', self)
        self.auth_btn.clicked.connect(self.swAuth)
        self.reg_2.clicked.connect(self.swReg)

    def swAuth(self):
        """Закрытие нынешнего окна и открытие окна авторизации"""

        self.close()
        self.switch_auth.emit()

    def swReg(self):
        """Закрытие нынешнего окна и открытие окна регистрации"""

        self.close()
        self.switch_reg.emit()


