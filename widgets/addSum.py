import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5 import uic
import sqlite3
import re
DB_NAME = "cash_machine.db"

class AddSum(QtWidgets.QWidget):

    switch_menu = QtCore.pyqtSignal(dict)

    def __init__(self, user):
        QtWidgets.QWidget.__init__(self)
        uic.loadUi('./ui/addSum.ui', self)
        self.getCash.clicked.connect(self.addSum)
        self.sum_100.clicked.connect(self.change_line_edit)
        self.sum_500.clicked.connect(self.change_line_edit)
        self.sum_1000.clicked.connect(self.change_line_edit)
        self.sum_5000.clicked.connect(self.change_line_edit)
        self.cash.setText("10")
        self.user = user

    def validation(self, money):
        pattern_money = re.compile(r'^[0-9]{1,10}[.]{0,1}[0-9]{0,2}$')
        if not pattern_money.match(money):
            return "Некорректно заполнено поле"
        return ""

    def addSum(self):
        error = self.validation(self.cash.text())
        if not error:
            self.user["money"] += float(self.cash.text())
            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            result = cur.execute("""UPDATE users
                        SET money = ?
                        WHERE id = ?""", [self.user["money"], self.user["account"]])
            con.commit()
            if result:
                self.close()
                self.switch_menu.emit(self.user)
            else:
                self.error.setText("Ошибка пополнения счёта")
        else:
            self.error.setText("Некорректно заполнено поле")
    
    def change_line_edit(self):
        self.cash.setText(self.sender().text())
