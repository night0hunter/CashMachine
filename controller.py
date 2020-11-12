import sys
from PyQt5 import QtWidgets
from widgets.mainWindow import MainWindow
from widgets.auth import Authorization
from widgets.reg import Registration
from widgets.menu import Menu
from widgets.addSum import AddSum
from widgets.takeSum import TakeSum

class Controller:
    def __init__(self):
        pass

    def show_auth(self):
        self.auth = Authorization()
        self.auth.switch_menu.connect(self.show_menu)
        self.auth.show()

    def show_reg(self):
        self.reg = Registration()
        self.reg.switch_menu.connect(self.show_main)
        self.reg.show()

    def show_menu(self, user):
        self.menu = Menu(user)
        self.menu.switch_mainWindow.connect(self.show_main)
        self.menu.switch_addSum.connect(self.show_addSum)
        self.menu.switch_takeSum.connect(self.show_takeSum)
        self.menu.show()

    def show_addSum(self, user):
        self.addSum = AddSum(user)
        self.addSum.switch_menu.connect(self.show_menu)
        self.addSum.show()

    def show_takeSum(self, user):
        self.takeSum = TakeSum(user)
        self.takeSum.switch_menu.connect(self.show_menu)
        self.takeSum.show()

    def show_main(self):
        self.window = MainWindow()
        self.window.switch_auth.connect(self.show_auth)
        self.window.switch_reg.connect(self.show_reg)
        self.window.show()


def main():
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    controller.show_main()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
