#!/usr/bin/env python3

# To run script install next libraries using command:
# pip install <libname>

# wheel
# setuptools
# pyabf
# pyqt5

import abfplot_gui
import abfplot_core
import abfplot_init
import sys
from PyQt5 import QtWidgets


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новий екземпляр QApplication
    window = abfplot_init.AbfPlot_GUI()  # Створення об'єкту классу AbfPlot_GUI
    window.show()  # Виведення головного вікна
    app.exec_()  # Запуск програми


if __name__ == '__main__':
    main()
