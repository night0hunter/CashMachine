import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5 import uic
import sqlite3
import re
import cfg
from service.service import create_log

class TakeSum(QtWidgets.QWidget):

    switch_menu = QtCore.pyqtSignal(dict)

    def __init__(self, user):
        QtWidgets.QWidget.__init__(self)
        uic.loadUi('./ui/takeSum.ui', self)
        self.takeCash.clicked.connect(self.takeSum)
        self.sum_100.clicked.connect(self.change_line_edit)
        self.sum_500.clicked.connect(self.change_line_edit)
        self.sum_1000.clicked.connect(self.change_line_edit)
        self.sum_5000.clicked.connect(self.change_line_edit)
        self.takeCashLineEdit.setText("10")
        self.user = user

    def validation(self, money):
        pattern_money = re.compile(r'^[0-9]{1,10}[.]{0,1}[0-9]{0,2}$')
        if not pattern_money.match(money):
            self.error.setText("Некорректно заполнено поле")
        return ""

    def takeSum(self):
        error = self.validation(self.takeCashLineEdit.text())
        if not error:
            takeMoney = float(self.takeCashLineEdit.text())
            if self.user["money"] > takeMoney:
                self.user["money"] -= takeMoney
                con = sqlite3.connect(cfg.DB_NAME)
                cur = con.cursor()
                result = cur.execute("""UPDATE users
                            SET money = ?
                            WHERE id = ?""", [takeMoney, self.user["account"]])
                con.commit()
                if result:
                    create_log(f"takeSum: user_id - {self.user['account']} money - {takeMoney}")
                    self.close()
                    self.switch_menu.emit(self.user)
                else:
                    self.error.setText("Ошибка пополнения счёта")
            else:
                self.error.setText("Недостаточно средств")
        else:
            self.error.setText("Некорректно заполнено поле")

    def change_line_edit(self):
        self.takeCashLineEdit.setText(self.sender().text())