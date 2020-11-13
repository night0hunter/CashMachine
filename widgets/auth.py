import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5 import uic
import sqlite3
from PyQt5.QtWidgets import QLineEdit
import cfg
from service.service import create_log
import hashlib


class Authorization(QtWidgets.QWidget):

    switch_menu = QtCore.pyqtSignal(dict)

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        uic.loadUi('./ui/authorization.ui', self)
        self.auth_btn_2.clicked.connect(self.auth)
        # self.hide_password.clicked.connect(self.hidePassword)
        # self.password_value.setEchoMode(QLineEdit.Password)

    def auth(self):
        con = sqlite3.connect(cfg.DB_NAME)
        cur = con.cursor()
        hash_password = hashlib.sha512(self.password_value.text().encode("utf-8")).hexdigest()
        data = {
            "login": self.login_value.text(),
            "password": hash_password
        }
        if data["login"] and data["password"]:
            result = cur.execute(
                f"""SELECT * FROM users WHERE login == \"{data['login']}\" AND password == \"{data['password']}\"""").fetchall()
            if result:
                curUser = {
                    "account": result[0][0],
                    "first_name": result[0][1],
                    "last_name": result[0][2],
                    "patronymic": result[0][3],
                    "login": result[0][4],
                    "birth_date": result[0][6],
                    "date_joined": result[0][7],
                    "money": result[0][8]
                }
                create_log(f"auth: user_id - {curUser['account']}")
                self.close()
                self.switch_menu.emit(curUser)
            else:
                self.error2.setText("Неверно введен логин или пароль!")
        else:
            self.error2.setText(
                "Для успешной авторизации\nнеобходимо заполнить все поля!")

    # def hidePassword(self):
    #     print(self.password_value.EchoMode())
    #     if self.password_value.EchoMode() == 2:
    #         self.password_value.setEchoMode(QLineEdit.Normal)
    #     elif self.password_value.EchoMode() == 0:
    #         self.password_value.setEchoMode(QLineEdit.Password)
