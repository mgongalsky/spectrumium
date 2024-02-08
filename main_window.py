import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class SpectralEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Спектральный редактор')
        self.setGeometry(100, 100, 800, 600)

        container = QWidget()  # Контейнер для компоновки
        layout = QVBoxLayout()  # Вертикальная компоновка

        self.canvas = PlotCanvas(self, width=8, height=6)
        layout.addWidget(self.canvas)  # Добавление холста в компоновку

        self.btn_select_file = QPushButton('Выбрать CSV файл', self)
        self.btn_select_file.clicked.connect(self.openFileDialog)
        self.btn_select_file.adjustSize()  # Автоматическая подгонка размера кнопки
        layout.addWidget(self.btn_select_file)  # Добавление кнопки в компоновку

        container.setLayout(layout)  # Установка компоновки в контейнер
        self.setCentralWidget(container)  # Установка контейнера как центрального виджета

        self.show()

    def openFileDialog(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите CSV файл", "", "CSV files (*.csv)")
        if file_path:
            print("Выбранный файл:", file_path)
            self.canvas.plot_csv(file_path)

class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)
        self.setParent(parent)

    def plot_csv(self, file_path):
        self.axes.clear()  # Очистка предыдущих графиков
        data = pd.read_csv(file_path)
        self.axes.plot(data.iloc[:,0], data.iloc[:,1], label='Спектр')
        self.axes.set_xlabel('Длина волны')
        self.axes.set_ylabel('Интенсивность')
        self.axes.legend()
        self.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SpectralEditor()
    sys.exit(app.exec_())
