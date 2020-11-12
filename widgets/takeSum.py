import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5 import uic


class TakeSum(QtWidgets.QWidget):

    switch_menu = QtCore.pyqtSignal()

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        uic.loadUi('./ui/takeSum.ui', self)
        self.takeCash.clicked.connect(self.takeSum)

    def takeSum(self):
        self.close()
        self.switch_menu.emit()