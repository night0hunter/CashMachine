import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5 import uic


class Menu(QtWidgets.QWidget):

    switch_mainWindow = QtCore.pyqtSignal()
    switch_addSum = QtCore.pyqtSignal(dict)
    switch_takeSum = QtCore.pyqtSignal()

    def __init__(self, user):
        QtWidgets.QWidget.__init__(self)
        uic.loadUi('./ui/menu.ui', self)
        self.addS.clicked.connect(self.add)
        self.takeS.clicked.connect(self.take)
        self.exit.clicked.connect(self.menu)

        self.name.setText(f"Имя: {user['first_name']}")
        self.surname.setText(f"Фамилия: {user['last_name']}")
        self.patronymic.setText(f"Отчество: {user['patronymic']}")
        self.login.setText(f"Логин: {user['login']}")
        self.bir_date.setText(f"Дата рождения: {user['birth_date']}")
        self.date_join.setText(f"Дата регистрации: {user['date_joined']}")
        self.account.setText(f"Счёт: {user['money']}")

        self.user = user
        
    def menu(self):
        self.close()
        self.switch_mainWindow.emit()

    def add(self):
        self.close()
        self.switch_addSum.emit(self.user)

    def take(self):
        self.close()
        self.switch_takeSum.emit()