import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5 import uic
import datetime
import re
import sqlite3


class Registration(QtWidgets.QWidget):

    switch_menu = QtCore.pyqtSignal()

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        uic.loadUi('./ui/registration.ui', self)
        self.register_2.clicked.connect(self.reg)

    def __validation(self, data):
        pattern_password = re.compile(
            r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-]).{8,}$')

        if len(data["first_name"]) == 0 or len(data["first_name"]) >= 50:
            return 'Некорректно заполнено поле: "Имя"'

        if len(data["last_name"]) == 0 or len(data["last_name"]) >= 50:
            return 'Некорректно заполнено поле: "Фамилия"'

        if len(data["patronymic"]) == 0 or len(data["patronymic"]) >= 50:
            return 'Некорректно заполнено поле: "Отчество"'

        if len(data["login"]) == 0 or len(data["login"]) >= 30:
            return 'Некорректно заполнено поле: "Логин"'

        if len(data["password"]) == 0 or len(data["password"]) >= 30:
            return 'Некорректно заполнено поле: "Пароль"'

        if data["birth_date"] > datetime.date.today():
            return 'Некорректно заполнено поле: "Дата рождения"'

        if data["password"] != data["password2"]:
            return "Пароли не совпадают"

        if not pattern_password.match(data["password"]):
            return "Пароль должен содержать как минимум 8 символов, \nвключая 1 спецсимвол, 1 цифру,\n 1 латинскую букву в верхнем и нижнем регистре"

        con = sqlite3.connect("cash_machine.db")
        cur = con.cursor()
        result = cur.execute(
            f"SELECT * FROM users WHERE login == \"{data['login']}\"").fetchall()
        if result:
            return "Пользователь с таким логином уже зарегистрирован"
        con.close()
        return ""

    def reg(self):
        data = {
            "first_name": self.first_name.text(),
            "last_name": self.last_name.text(),
            "patronymic": self.patronymic_value.text(),
            "login": self.login_value.text(),
            "password": self.password_value.text(),
            "password2": self.password2.text(),
            "birth_date": datetime.datetime.strptime(self.birthDate.text(), "%d.%m.%Y").date()
        }
        error = self.__validation(data)
        if not error:
            con = sqlite3.connect("cash_machine.db")
            cur = con.cursor()
            sql = ("""INSERT INTO users(first_name, last_name, patronymic, login, password,
                    birth_date, date_joined) VALUES(?,?,?,?,?,?,?)""")
            result = cur.execute(sql, [data["first_name"], data["last_name"], data["patronymic"], data["login"],
                                       data["password"], data["birth_date"].strftime('%d.%m.%Y'), datetime.date.today().strftime('%d.%m.%Y')])
            con.commit()
            con.close()
            if result:
                self.close()
                self.switch_menu.emit()
        else:
            self.error.setText(error)
