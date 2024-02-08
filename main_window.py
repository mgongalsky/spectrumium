import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton, QVBoxLayout, QWidget, QSlider, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class GraphData:
    def __init__(self, file_path=None):
        self.file_path = file_path
        self.data = None
        self.load_data()

    def load_data(self):
        if self.file_path:
            self.data = pd.read_csv(self.file_path)

    def get_data(self):
        return self.data


class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super().__init__(self.fig)
        self.setParent(parent)
        self.current_file_path = None  # Для хранения пути к текущему файлу данных
        self.graph_data = None  # Инициализация атрибута для хранения данных графика

    def plot(self, font_size=10, line_width=2, axis_width=1):
        if self.graph_data and self.graph_data.get_data() is not None:
            self.axes.clear()
            self.axes.xaxis.label.set_size(font_size)
            self.axes.yaxis.label.set_size(font_size)
            self.axes.tick_params(labelsize=font_size, width=axis_width)
            data = self.graph_data.get_data()
            self.axes.plot(data.iloc[:,0], data.iloc[:,1], linewidth=line_width, label='Спектр')
            self.axes.set_xlabel('Длина волны', fontsize=font_size)
            self.axes.set_ylabel('Интенсивность', fontsize=font_size)
            self.axes.legend()
            self.draw()

class SpectralEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Спектральный редактор')
        self.setGeometry(100, 100, 1000, 600)

        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)

        h_layout = QHBoxLayout(self.main_widget)
        v_layout = QVBoxLayout()
        h_layout.addLayout(v_layout, 75)

        self.canvas = PlotCanvas(self, width=8, height=6)
        v_layout.addWidget(self.canvas)

        self.btn_select_file = QPushButton('Выбрать CSV файл', self)
        self.btn_select_file.clicked.connect(self.openFileDialog)
        v_layout.addWidget(self.btn_select_file)

        control_layout = QVBoxLayout()
        h_layout.addLayout(control_layout, 25)

        # Создание ползунков как горизонтальных
        self.font_size_slider = self.create_slider("Размер шрифта", control_layout, 8, 20, 10)
        self.line_width_slider = self.create_slider("Толщина линий графика", control_layout, 1, 10, 2)
        self.axis_width_slider = self.create_slider("Толщина осей", control_layout, 1, 10, 1)

        self.show()

    def create_slider(self, label, layout, min_val, max_val, initial_val):
        layout.addWidget(QLabel(label))
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(min_val)
        slider.setMaximum(max_val)
        slider.setValue(initial_val)
        slider.valueChanged.connect(self.update_plot)
        layout.addWidget(slider)
        return slider

    def openFileDialog(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите CSV файл", "", "CSV files (*.csv)")
        if file_path:
            self.canvas.graph_data = GraphData(file_path)
            self.update_plot()

    def update_plot(self):
        self.canvas.plot(self.font_size_slider.value(), self.line_width_slider.value(), self.axis_width_slider.value())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SpectralEditor()
    sys.exit(app.exec_())
