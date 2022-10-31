import settings
import abfplot_gui
import abfplot_core
from PyQt5 import QtWidgets


# Ініціалізація графічного інтерфейсу
class AbfPlot_GUI(QtWidgets.QMainWindow, abfplot_gui.Ui_MainWindow):

    def __init__(self):

        super().__init__()
        self.setupUi(self)

        # Зміна параметрів при перемиканні режимів
        self.radioButton_6.toggled.connect(lambda: self.setMode('VC'))
        self.radioButton_7.toggled.connect(lambda: self.setMode('IC'))
        self.radioButton_8.toggled.connect(lambda: self.setMode('CA'))
        self.radioButton_9.toggled.connect(lambda: self.setMode('CAP'))
        self.pushButton_1.clicked.connect(lambda: self.plot())
        self.pushButton_2.clicked.connect(lambda: self.membrane_test())

    # Зміна параметрів при перемиканні режимів
    def setMode(self, mode):

        if mode == 'VC':
            self.spinBox_4.setValue(20000)
            self.lineEdit_5.setValue(300)
            self.lineEdit_6.setValue(400)
            self.lineEdit_7.setValue(-400)
            self.lineEdit_8.setValue(100)
        if mode == 'IC':
            self.spinBox_4.setValue(20000)
            self.lineEdit_5.setValue(300)
            self.lineEdit_6.setValue(400)
            self.lineEdit_7.setValue(-100)
            self.lineEdit_8.setValue(50)
        if mode == 'CA':
            self.spinBox_4.setValue(20000)
            self.lineEdit_5.setValue(300)
            self.lineEdit_6.setValue(400)
            self.lineEdit_7.setValue(-75)
            self.lineEdit_8.setValue(75)
        if mode == 'CAP':
            self.spinBox_4.setValue(125000)
            self.lineEdit_5.setValue(70)
            self.lineEdit_6.setValue(120)
            self.lineEdit_7.setValue(-1)
            self.lineEdit_8.setValue(1)

    def initParam(self):

        global ABF_FILE, DIR, SINCE, STIM, EXCLUDE_SWEEPS, CHANNEL, BASELINE, SIGMA, DESCR, OFFSET_Y, TWO_WIN, LINE_WIDTH, ALPHA, FIGURE_W, FIGURE_H, DPI, FREQ, SHOW, SAVE, SAVE_FORMAT, MIN_X, MAX_X, MIN_Y, MAX_Y

        # [self.lineEdit_1.text()]
        ABF_FILE = list(map(str, self.lineEdit_1.text().split(' ')))
        DIR = ''
        SINCE = list(map(int, self.lineEdit_2.text().split(' ')))
        # if self.radioButton_1.isChecked():
        #    STIM = ['+']
        # else:
        #    STIM = ['-']
        STIM = list(map(str, self.lineEdit_10.text().split(' ')))
        EXCLUDE_SWEEPS = [
            list(map(int, self.lineEdit_9.text().split(',')))]
        CHANNEL = self.comboBox_1.currentIndex()
        BASELINE = [self.doubleSpinBox_4.value(), self.doubleSpinBox_5.value()] if self.checkBox_2.isChecked() else [None, None]
        SIGMA = self.doubleSpinBox_3.value()
        DESCR = self.lineEdit_3.text()
        OFFSET_Y = self.lineEdit_4.value()
        TWO_WIN = self.checkBox_1.isChecked()
        LINE_WIDTH = self.doubleSpinBox_1.value()
        ALPHA = self.doubleSpinBox_2.value()
        FIGURE_W = self.spinBox_1.value()
        FIGURE_H = self.spinBox_2.value()
        DPI = self.spinBox_3.value()
        FREQ = self.spinBox_4.value()
        SHOW = self.checkBox_3.isChecked()
        SAVE = self.checkBox_4.isChecked()
        if self.radioButton_3.isChecked():
            SAVE_FORMAT = 'png'
        if self.radioButton_4.isChecked():
            SAVE_FORMAT = 'svg'
        if self.radioButton_5.isChecked():
            SAVE_FORMAT = 'eps'
        MIN_X = int(self.lineEdit_5.text()) * FREQ//1000
        MAX_X = int(self.lineEdit_6.text()) * FREQ//1000
        MIN_Y = self.lineEdit_7.value()
        MAX_Y = self.lineEdit_8.value()

        for i in range(len(STIM)):
            if STIM[i] == '-':
                STIM[i] = -1
            else:
                STIM[i] = 1
        
        # load params from settings.py if input is empty
        if ABF_FILE[0] == '' and len(ABF_FILE) == 1:
            ABF_FILE = settings.ABF_FILE
            DIR = settings.DIR

    def plot(self):
             
        try:
            self.initParam()
            abfplot_core.plot(ABF_FILE, SINCE, STIM, EXCLUDE_SWEEPS, CHANNEL, BASELINE, SIGMA,
                              DESCR, OFFSET_Y, TWO_WIN, LINE_WIDTH, ALPHA, FIGURE_W, FIGURE_H,
                              DPI, FREQ, SHOW, SAVE, SAVE_FORMAT, MIN_X, MAX_X, MIN_Y, MAX_Y)

        # Перехоплення можливих помилок та виведення повідомлення про помилку
        except ValueError as e:
            print(e)
            self.label_8.setText('Invalid input. Please, retry.')
        except ZeroDivisionError as e:
            print(e)
            self.label_8.setText('Invalid input. Please, retry.')
        except FileNotFoundError as e:
            print(e)
            self.label_8.setText('File not found')
        except Exception as e:
            print(e)
            self.label_8.setText('Unknown error. Check input.')
        else:
            self.label_8.setText('')

    def membrane_test(self):
        
        try:
            self.initParam()
            abfplot_core.membrane_test(ABF_FILE, DIR, FIGURE_W, FIGURE_H, SAVE, SHOW, SAVE_FORMAT)

        # Перехоплення можливих помилок та виведення повідомлення про помилку
        except FileNotFoundError as e:
            print(e)
            self.label_8.setText('File not found')
        except Exception as e:
            print(e)
            self.label_8.setText('Must be in VC configuration')
        except:
            print('Unknown error. Check input.')
            self.label_8.setText('Unknown error. Check input.')
        else:
            self.label_8.setText('')
