import math
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTextEdit, QSlider, QTableWidget, QTableWidgetItem
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import pandas as pd
from PyQt5.QtCore import Qt

# чтобы запустить надо сначала скачать библиотеку
# на mac перед командами приписывать  python3 -m
# pip install PyQt5
# pip install matplotlib
# pip install numpy
# python3 -m pip install pandas

l = 40
D = 0.5
T = 450
NN = 300
x = 5

# считаем A_n член ряда 
def A(n: int, x: float, t: float, l) -> float:
    if n == 1: 
        A_n = 0
    else:
        A_n = -(4*math.cos(math.pi * n) + 4)/(math.pi * n**2 - math.pi)
    return math.cos((math.pi * n * x)/l) * A_n * math.exp((-D)*  (((math.pi * n) / l)**2)   * t) 

# считаем сумму ряда
def Sum_r(x: float, t: float, N: int, l) -> float:
    result = 4/math.pi
    for i in range(0,N):
        result+=A(i+1, x, t, l)
    return result

def create1(N: int, x: float, l):
    linx = np.linspace(0, int (T/2), N)
    u = np.zeros(N)
    for i in range(0, N):
        u[i] = Sum_r(x=x, t=linx[i], N=N, l=l)
    return u

def create2(N: int, t: float, l):
    linx = np.linspace(0, int(l), int(N))
    u = np.zeros(N)
    for i in range(0, N):
        u[i] = Sum_r(x=linx[i], t=t, N=N, l=l)
    return u

# Calculate R_N
def R_N(x, t, N, l):
    summation = 0
    for n in range(N + 1, 200):  
        summation += 4 / (n * (n + 2) * (n + 1) * ((D * (math.pi**3) * t * (np.exp(D*((math.pi * n) /l) ** 2 * t))) / (l ** 2)))
    print(summation)
    return summation 


def find_N_epsilon(epsilon, x, t, l):
    N = 1
    while True:
        if abs(R_N(x, t, N, l)) < epsilon:
            return N
        N += 1

# Calculate N_ex
def find_N_ex(epsilon, x, t, l):
    N = find_N_epsilon(epsilon, x, t, l)
    NE = N
    while abs(Sum_r(x, t, N, l) - Sum_r(x, t, NE - 1, l)) <= epsilon and NE > 0:
        NE -= 1
    return NE + 1


# Main function to generate the table
def generate_table(epsilons, x, t):
    data = {'ε': epsilons, 'N_ε': [], 'N_экс': []}
    for epsilon in epsilons:
        N_epsilon = find_N_epsilon(epsilon, x, t, l)
        N_ex = find_N_ex(epsilon, x, t, l)
        data['N_ε'].append(N_epsilon)
        data['N_экс'].append(N_ex)
    return data

class MyApp(QWidget):
    def __init__(self):
        super().__init__()# Наследуемся от QWidget
        self.initUI() # Инициализируем интерфейс окна приложения

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)# Установка размеров и позиции окна. Обратите внимание на то, что координаты окна заданы в метрах.
        self.setWindowTitle('Графическое приложение с Matplotlib')# Установка заголовка окна.

        self.fig = Figure()# Создаем объект Figure для отображения графика.
        self.canvas = FigureCanvas(self.fig)# Создаем FigureCanvas для отображения графика.
        self.ax1 = self.fig.add_subplot(121)# Создаем объект Axes для отображения графика.
        self.ax2 = self.fig.add_subplot(122)# Создаем объект Axes для отображения графика. 
        self.table = QTableWidget(self)
        
        self.layout = QVBoxLayout()# Создаем новый QVBoxLayout для отображения графика.
        self.layout.addWidget(self.canvas)# Добавляем FigureCanvas в основной QVBoxLayout.
        self.layout.addWidget(self.table)

        self.button_layout = QHBoxLayout()# Создаем новый QHBoxLayout для кнопок

        self.draw_button1 = QPushButton('Нарисовать графики', self)# Создаем кнопку для отрисовки графика.
        self.draw_button1.clicked.connect(self.draw_plot1)# При нажатии на кнопку отрисовываем график.
        self.button_layout.addWidget(self.draw_button1)# Добавляем кнопку в основной QHBoxLayout.

        self.draw_button2 = QPushButton('Очистить графики', self)
        self.draw_button2.clicked.connect(self.draw_plot2)
        self.button_layout.addWidget(self.draw_button2)

        self.draw_button3 = QPushButton('расчитать оценку остатка ряда', self)
        self.draw_button3.clicked.connect(self.update_table)
        self.button_layout.addWidget(self.draw_button3)

        self.layout.addLayout(self.button_layout)# Добавляем кнопки в основной QVBoxLayout.


        # Создание строки с элементами управления
        self.control_layout_l = QHBoxLayout()

         # Метка для переменной l
        self.label_l = QLabel('l: ', self)
        self.control_layout_l.addWidget(self.label_l)

        # Редактор текста для переменной l
        self.textedit_l = QTextEdit('40', self)
        self.textedit_l.setMaximumHeight(30)
        self.textedit_l.setMaximumWidth(50)
        self.control_layout_l.addWidget(self.textedit_l)

        # Слайдер для управления переменной l
        self.slider_l = QSlider(Qt.Horizontal, self)
        self.slider_l.setMinimum(1)
        self.slider_l.setMaximum(100)
        self.slider_l.setValue(40)
        self.slider_l.setTickInterval(5)
        self.slider_l.setSingleStep(1)
        self.slider_l.valueChanged.connect(self.update_l_from_slider)
        self.control_layout_l.addWidget(self.slider_l)

        self.layout.addLayout(self.control_layout_l)


        # Создание строки с элементами управления
        self.control_layout_T = QHBoxLayout()

         # Метка для переменной T
        self.label_T = QLabel('T:', self)
        self.control_layout_T.addWidget(self.label_T)

        # Редактор текста для переменной T
        self.textedit_T = QTextEdit('450', self)
        self.textedit_T.setMaximumHeight(30)
        self.textedit_T.setMaximumWidth(50)
        self.control_layout_T.addWidget(self.textedit_T)

        # Слайдер для управления переменной T
        self.slider_T = QSlider(Qt.Horizontal, self)
        self.slider_T.setMinimum(1)
        self.slider_T.setMaximum(800)
        self.slider_T.setValue(450)
        self.slider_T.setTickInterval(5)
        self.slider_T.setSingleStep(1)
        self.slider_T.valueChanged.connect(self.update_T_from_slider)
        self.control_layout_T.addWidget(self.slider_T)

        self.layout.addLayout(self.control_layout_T)


        # Создание строки с элементами управления
        self.control_layout_N = QHBoxLayout()

         # Метка для переменной N
        self.label_N = QLabel('N: ', self)
        self.control_layout_N.addWidget(self.label_N)

        # Редактор текста для переменной N
        self.textedit_N = QTextEdit('50', self)
        self.textedit_N.setMaximumHeight(30)
        self.textedit_N.setMaximumWidth(50)
        self.control_layout_N.addWidget(self.textedit_N)

        # Слайдер для управления переменной N
        self.slider_N = QSlider(Qt.Horizontal, self)
        self.slider_N.setMinimum(1)
        self.slider_N.setMaximum(100)
        self.slider_N.setValue(50)
        self.slider_N.setTickInterval(5)
        self.slider_N.setSingleStep(1)
        self.slider_N.valueChanged.connect(self.update_N_from_slider)
        self.control_layout_N.addWidget(self.slider_N)

        self.layout.addLayout(self.control_layout_N)


        # Создание строки с элементами управления
        self.control_layout_t = QHBoxLayout()

        # Метка для переменной t
        self.label_t = QLabel('t: ', self)
        self.control_layout_t.addWidget(self.label_t)

        # Редактор текста для переменной t
        self.textedit_t = QTextEdit('5', self)
        self.textedit_t.setMaximumHeight(30)
        self.textedit_t.setMaximumWidth(50)
        self.control_layout_t.addWidget(self.textedit_t)

        # Слайдер для управления переменной t
        self.slider_t = QSlider(Qt.Horizontal, self)
        self.slider_t.setMinimum(1)
        self.slider_t.setMaximum(200)
        self.slider_t.setValue(1)
        self.slider_t.setTickInterval(5)
        self.slider_t.setSingleStep(1)
        self.slider_t.valueChanged.connect(self.update_t_from_slider)
        self.control_layout_t.addWidget(self.slider_t)

        self.layout.addLayout(self.control_layout_t)

        self.setLayout(self.layout)


        
    def draw_plot1(self):
        # Здесь можно добавить код для отрисовки графиков
        self.ax1.clear()
        self.ax2.clear()

        l = float(self.textedit_l.toPlainText())  # Получаем значение l из редактора текста
        T = float(self.textedit_T.toPlainText())  # Получаем значение T из редактора текста
        NN = float(self.textedit_N.toPlainText())  # Получаем значение N из редактора текста

        t = np.linspace(0, int (T), int(NN))
        for i in range(0,int(l),5):
            self.ax1.plot(t, create1(int(NN), i, int(l)), label=f'x = {i}')

        self.ax1.set_xlabel('t, c')
        self.ax1.set_ylabel('концентрация u, °мг/м^3')
        self.ax1.legend()
        self.ax1.grid()

        t2 = np.linspace(0, int(l), int(NN))
        self.ax2.plot(t2, create2(int(NN), 0, int(l)), label='t = 0')
        self.ax2.plot(t2, create2(int(NN), 2, int(l)), label='t = 2')
        self.ax2.plot(t2, create2(int(NN), 5, int(l)), label='t = 5')
        self.ax2.plot(t2, create2(int(NN), 20, int(l)), label='t = 20')
        self.ax2.plot(t2, create2(int(NN), 40, int(l)), label='t = 40')
        self.ax2.plot(t2, create2(int(NN), 75, int(l)), label='t = 75')
        self.ax2.plot(t2, create2(int(NN), 450, int(l)), label='t = 450')

        self.ax2.set_xlabel('x, см')
        self.ax2.set_ylabel('концентрация u, °мг/м^3')
        self.ax2.legend()
        self.ax2.grid()

        self.canvas.draw()

        pass
        
    def draw_plot2(self):
        # Здесь можно добавить код для очистки графиков
        self.ax1.clear()
        self.ax2.clear()
        self.canvas.draw()

        pass

    def update_l_from_slider(self):
        # Обновление значения переменной l при изменении слайдера
        l = self.slider_l.value()
        self.textedit_l.setText(str(l))

    def update_T_from_slider(self):
        # Обновление значения переменной T при изменении слайдера
        T = self.slider_T.value()
        self.textedit_T.setText(str(T))

    def update_N_from_slider(self):
        # Обновление значения переменной N при изменении слайдера
        NN = self.slider_N.value()
        self.textedit_N.setText(str(NN))

    def update_t_from_slider(self):
        # Обновление значения переменной N при изменении слайдера
        self.textedit_t.setText(str(self.slider_t.value()))


    def update_table(self):
    
            t = float(self.textedit_t.toPlainText()) # Получаем значение t из редактора текста

            epsilons = [10**-i for i in range(2, 9)]
            
            table_data = generate_table(epsilons, x, t)

            self.table.setRowCount(3)
            self.table.setColumnCount(len(epsilons) + 1)
            self.table.setHorizontalHeaderLabels([''] + [f'10^(-{i})' for i in range(2, 9)])

            self.table.setItem(0, 0, QTableWidgetItem('ε'))
            self.table.setItem(1, 0, QTableWidgetItem('N_ε'))
            self.table.setItem(2, 0, QTableWidgetItem('N_экс'))

            for col, epsilon in enumerate(epsilons):
                self.table.setItem(0, col + 1, QTableWidgetItem(str(epsilon)))
                self.table.setItem(1, col + 1, QTableWidgetItem(str(table_data['N_ε'][col])))
                self.table.setItem(2, col + 1, QTableWidgetItem(str(table_data['N_экс'][col])))
            
            
if __name__ == '__main__':
    app = QApplication(sys.argv)# Создаем объект приложения и передаем аргументы командной строки.
    ex = MyApp() # Создаем объект класса MyApp.
    ex.show()# Показ окна.
    sys.exit(app.exec_())# Запуск цикла обработки событий.