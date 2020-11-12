import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5 import uic
import sqlite3
import re
DB_NAME = "cash_machine.db"


class TakeSum(QtWidgets.QWidget):

    switch_menu = QtCore.pyqtSignal(dict)

    def __init__(self, user):
        QtWidgets.QWidget.__init__(self)
        uic.loadUi('./ui/takeSum.ui', self)
        self.takeCash.clicked.connect(self.takeSum)
        self.user = user

    def validation(self, money):
        pattern_money = re.compile(r'^[0-9]{1,10}[.]{0,1}[0-9]{0,2}$')
        if not pattern_money.match(money):
            return "Некорректно заполнено поле"
        return ""

    def takeSum(self):
        error = self.validation(self.takeCash.text())
        if not error:
            if self.user["money"] > float(self.cash.text()):
                self.user["money"] -= float(self.cash.text())
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
                    print("error")
            else:
                print("Not enough money!")
        else:
            print(error)
