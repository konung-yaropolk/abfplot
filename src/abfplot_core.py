import sys
import numpy as np
import matplotlib.pyplot as plt
import pyabf
import pyabf.filter
import pyabf.tools.memtest
from itertools import zip_longest


# Задання глобального масиву вертикальних зміщень
OFFSETS = [0.0, 0.0, 0.0, 0.0]

# Функція виведеня окремо взятого треку


def makeline(ABF_FILE, SINCE, STIM, EXCLUDE_SWEEPS, BASELINE, SIGMA,
             OFFSET_Y, LINE_WIDTH, ALPHA, MIN_X, MAX_X, channel=0, plotonly=''):

    global OFFSETS

    # Перехоплення помилки відсутнього файлу
    try:
        # Відкривання abf файлу
        abf = pyabf.ABF(ABF_FILE + '.abf')
    except ValueError:
        print(ABF_FILE + '.abf not found!')
        raise FileNotFoundError
    else:
        print(ABF_FILE + '.abf processing...')

        # Визначення загальної кількості треків
        sweep_count = abf.sweepCount
        pyabf.filter.gaussian(abf, 0)
        # Задання інтенсивності фільтрування даних
        pyabf.filter.gaussian(abf, SIGMA)

        if SINCE == 0:
            SINCE = sweep_count + 1

        # Створення груп треків, всі, що за номером після значення SINCE - йдуть у групу B
        sweep_a = list(range(0, SINCE-1))
        sweep_b = list(range(SINCE-1, sweep_count))

        # Об'явлення масивів значень x та y для групи треків
        sweep_a_x_list = np.array([], float)
        sweep_a_y_list = np.array([], float)
        sweep_b_x_list = np.array([], float)
        sweep_b_y_list = np.array([], float)

        # Створення масивів для рендерингу треків
        for sweep_n_a, sweep_n_b in zip_longest(sweep_a, sweep_b, fillvalue=None):

            # Створення масиву виключно з треків виключно групи B
            if plotonly != 2 and sweep_n_a != None:

                # Обрання конкретного треку з файлу
                abf.setSweep(sweep_n_a, channel, baseline=BASELINE)

                # Перенесення треку в масив тільки якщо він не позначений як виключений
                if sweep_n_a + 1 not in EXCLUDE_SWEEPS:

                    # Якщо список з даними треків пустий - додати першим елементом ділянку треку
                    if list(sweep_a_x_list) == []:
                        sweep_a_x_list = [abf.sweepX[MIN_X:MAX_X]]
                        sweep_a_y_list = [abf.sweepY[MIN_X:MAX_X]]
                    # Інакше - додати наступним елементом ділянку треку
                    else:
                        sweep_a_x_list = np.vstack(
                            (sweep_a_x_list, abf.sweepX[MIN_X:MAX_X]))
                        sweep_a_y_list = np.vstack(
                            (sweep_a_y_list, abf.sweepY[MIN_X:MAX_X]))

            # Створення масиву виключно з треків виключно групи A
            if plotonly != 1 and sweep_n_b != None:

                # Обрання конкретного треку з файлу
                abf.setSweep(sweep_n_b, channel, baseline=BASELINE)

                # Перенесення треку в масив тільки якщо він не позначений як виключений
                if sweep_n_b + 1 not in EXCLUDE_SWEEPS:
                    # Якщо список з даними треків пустий - додати першим елементом ділянку треку
                    if list(sweep_b_x_list) == []:
                        sweep_b_x_list = [abf.sweepX[MIN_X:MAX_X]]
                        sweep_b_y_list = [abf.sweepY[MIN_X:MAX_X]]
                    # Інакше - додати наступним елементом ділянку треку
                    else:
                        sweep_b_x_list = np.vstack(
                            (sweep_b_x_list, abf.sweepX[MIN_X:MAX_X]))
                        sweep_b_y_list = np.vstack(
                            (sweep_b_y_list, abf.sweepY[MIN_X:MAX_X]))

        # Додання до кожного значення Y вертикальне зміщення OFFSET_Y
        def makeoffset(sweep_y_list):
            for i in range(0, len(sweep_y_list)):
                OFFSETS[1] = i * OFFSET_Y
                sweep_y_list[i] += OFFSETS[1]

        makeoffset(sweep_a_y_list)
        makeoffset(sweep_b_y_list)

        # Створення кінцевого списку для рендерингу
        data_to_plot = zip_longest(
            sweep_a_x_list, sweep_a_y_list, sweep_b_x_list, sweep_b_y_list, fillvalue=[])

        # Рендеринг треків по черзі по одному з кожної групи
        for sweep_a_x_data, sweep_a_y_data, sweep_b_x_data, sweep_b_y_data in data_to_plot:

            if plotonly != 2:
                plt.plot(sweep_a_x_data, sweep_a_y_data, lw=LINE_WIDTH,
                        alpha=ALPHA, color='black' if STIM == 1 else 'red')
            if plotonly != 1:
                plt.plot(sweep_b_x_data, sweep_b_y_data, lw=LINE_WIDTH,
                        alpha=ALPHA, color='black' if STIM == -1 else 'red')


# Створення підписів до осі абсис
def labels_x(MIN_X, MAX_X, FREQ):

    labels = []
    for i in range(MIN_X, MAX_X + 500, 100):
        if (i*2 / FREQ * 1000) % 25 == 0:
            labels.append(int(i*2 / FREQ * 1000))
        else:
            labels.append('')
    return labels


# Масштабування по осям абсис та ординат

def makefigure(rows_n, cols_n, plot_n, FREQ, MIN_X, MAX_X, MIN_Y=0, MAX_Y=0, yaxis=True):
    axis = [MIN_X/FREQ, MAX_X/FREQ] + [MIN_Y, MAX_Y]
    plt.subplot(rows_n, cols_n, plot_n)

    if not yaxis:
        plt.yticks([])
    if yaxis:
        plt.axis(axis)


# Функція, що компонує готові рисунки

def makeplot(ABF_FILE, SINCE, STIM, EXCLUDE_SWEEPS, CHANNEL, BASELINE, SIGMA,
             DESCR, OFFSET_Y, TWO_WIN, LINE_WIDTH, ALPHA, FREQ, MIN_X, MAX_X,
             MIN_Y, MAX_Y):


    # Виведення для одного з каналів
    if CHANNEL == 0 or CHANNEL == 1:

        if TWO_WIN == True:

            for j in range(1, 3):

                makefigure(1, 2, j, FREQ, MIN_X, MAX_X, yaxis=False)

                for i in range(len(ABF_FILE)):
                    makeline(ABF_FILE[i], SINCE[i], STIM[i], EXCLUDE_SWEEPS[i], BASELINE, SIGMA,
                             OFFSET_Y, LINE_WIDTH, ALPHA, MIN_X, MAX_X, channel=CHANNEL, plotonly=j)

        else:

            if OFFSET_Y == 0:
                makefigure(1, 1, 1, FREQ, MIN_X, MAX_X, MIN_Y, MAX_Y)
            else:
                makefigure(1, 1, 1, FREQ, MIN_X, MAX_X, yaxis=False)

            for i in range(len(ABF_FILE)):
                makeline(ABF_FILE[i], SINCE[i], STIM[i], EXCLUDE_SWEEPS[i], BASELINE, SIGMA,
                         OFFSET_Y, LINE_WIDTH, ALPHA, MIN_X, MAX_X, channel=CHANNEL)

    # Виведення для двох каналів одночасно
    if CHANNEL == 2:

        if OFFSET_Y == 0:

            for j in range(2):

                makefigure(2, 1, j+1, FREQ, MIN_X, MAX_X, MIN_Y, MAX_Y)

                for i in range(len(ABF_FILE)):
                    makeline(ABF_FILE[i], SINCE[i], STIM[i], EXCLUDE_SWEEPS[i], BASELINE,
                             SIGMA, OFFSET_Y, LINE_WIDTH, ALPHA, MIN_X, MAX_X, channel=j)

        else:

            for j in range(2):

                makefigure(2, 1, j+1, FREQ, MIN_X, MAX_X, yaxis=False)

                for i in range(len(ABF_FILE)):
                    makeline(ABF_FILE[i], SINCE[i], STIM[i], EXCLUDE_SWEEPS[i], BASELINE,
                             SIGMA, OFFSET_Y, LINE_WIDTH, ALPHA, MIN_X, MAX_X, channel=j)



def plot(ABF_FILE, SINCE, STIM, EXCLUDE_SWEEPS, CHANNEL, BASELINE, SIGMA,
         DESCR, OFFSET_Y, TWO_WIN, LINE_WIDTH, ALPHA, FIGURE_W, FIGURE_H,
         DPI, FREQ, SHOW, SAVE, SAVE_FORMAT, MIN_X, MAX_X, MIN_Y, MAX_Y):

    # Створення нового рисунку
    plt.figure(num=None, figsize=(FIGURE_W, FIGURE_H),
               dpi=DPI if SAVE else None)
        
    try:
        makeplot(ABF_FILE, SINCE, STIM, EXCLUDE_SWEEPS, CHANNEL, BASELINE, SIGMA,
                 DESCR, OFFSET_Y, TWO_WIN, LINE_WIDTH, ALPHA, FREQ, MIN_X, MAX_X,
                 MIN_Y, MAX_Y)
    except FileNotFoundError:
        plt.close()
        raise FileNotFoundError
    else:
        # Створення  рисунку
        plt.suptitle('\n' + ABF_FILE[0] + ' ' + DESCR, size=10)
        plt.tight_layout()

        # Збереження рисунку у форматі, вказаному в SAVE_FORMAT

        if SAVE:
            plt.savefig(ABF_FILE[0] + '.' + SAVE_FORMAT)       
        if SHOW:
            plt.show()
        else:
            plt.close()
            
        print('Script finished.')

def membrane_test(ABF_FILE, FIGURE_W, FIGURE_H, SAVE, SHOW, SAVE_FORMAT):
    
    for i in ABF_FILE:
    
        try:
            abf = pyabf.ABF(i + '.abf')
        except ValueError:
            print(i + '.abf not found!')
            raise FileNotFoundError
        else:            
            print(i + '.abf processing...')
            
            memtest = pyabf.tools.memtest.Memtest(abf)

            fig = plt.figure(figsize=(FIGURE_W, FIGURE_H))

            ax1 = fig.add_subplot(221)
            ax1.grid(alpha=.2)
            ax1.plot(abf.sweepTimesMin, memtest.Ih.values,
                    ".", color='C0', alpha=.7, mew=0)
            ax1.set_title(memtest.Ih.name)
            ax1.set_ylabel(memtest.Ih.units)

            ax2 = fig.add_subplot(222)
            ax2.grid(alpha=.2)
            ax2.plot(abf.sweepTimesMin, memtest.Rm.values,
                    ".", color='C3', alpha=.7, mew=0)
            ax2.set_title(memtest.Rm.name)
            ax2.set_ylabel(memtest.Rm.units)

            ax3 = fig.add_subplot(223)
            ax3.grid(alpha=.2)
            ax3.plot(abf.sweepTimesMin, memtest.Ra.values,
                    ".", color='C1', alpha=.7, mew=0)
            ax3.set_title(memtest.Ra.name)
            ax3.set_ylabel(memtest.Ra.units)

            ax4 = fig.add_subplot(224)
            ax4.grid(alpha=.2)
            ax4.plot(abf.sweepTimesMin, memtest.CmStep.values,
                    ".", color='C2', alpha=.7, mew=0)
            ax4.set_title(memtest.CmStep.name)
            ax4.set_ylabel(memtest.CmStep.units)

            for ax in [ax1, ax2, ax3, ax4]:
                ax.margins(0.1, 0.9)
                ax.set_xlabel("Recording Time (minutes)")
                for tagTime in abf.tagTimesMin:
                    ax.axvline(tagTime, color='k', ls='--')

            plt.suptitle(i[-15:])   # Вывести только имя файла (последние 15 символов пути для типичного abf файла)
            plt.tight_layout()
            
            if SAVE:
                plt.savefig(i + '_memtest.' + SAVE_FORMAT)       
            if SHOW:
                plt.show()
            else:
                plt.close()
                            
    print('Script finished.')

