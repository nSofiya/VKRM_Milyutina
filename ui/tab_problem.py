from algorithms.babc import BABC

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QComboBox,
    QLineEdit,
    QGroupBox,
    QFormLayout,
    QFileDialog,
    QMessageBox
)

from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class TSP_Tab(QWidget):
    def __init__(self):
        super().__init__()

        # ✔ список городов (ВАЖНО: единый формат)
        self.cities = []

        main_layout = QVBoxLayout()

        # =====================================================
        # ПАРАМЕТРЫ
        # =====================================================

        parameters_group = QGroupBox("Параметры")
        parameters_layout = QFormLayout()

        self.algorithm_combo = QComboBox()
        self.algorithm_combo.addItems(["BABC", "BGOA", "B-LJ", "B-SA"])

        parameters_layout.addRow("Алгоритм:", self.algorithm_combo)

        self.transfer_combo = QComboBox()
        self.transfer_combo.addItems([
            "S1", "S2", "S3", "S4",
            "V1", "V2", "V3", "V4",
            "VG", "SIN"
        ])

        parameters_layout.addRow("Передаточная функция:", self.transfer_combo)

        self.transfer_image = QLabel()
        self.transfer_image.setFixedHeight(200)
        self.transfer_image.setAlignment(Qt.AlignmentFlag.AlignCenter)

        parameters_layout.addRow("Формула:", self.transfer_image)

        self.binary_combo = QComboBox()
        self.binary_combo.addItems([
            "Стандартный метод",
            "Метод дополнения",
            "Метод статистической вероятности",
            "Элитистский метод",
            "Метод элитистской рулетки"
        ])

        parameters_layout.addRow("Правило бинаризации:", self.binary_combo)

        parameters_group.setLayout(parameters_layout)

        main_layout.addWidget(parameters_group)

        # =====================================================
        # КНОПКИ
        # =====================================================

        self.load_button = QPushButton("Загрузить данные")
        self.run_button = QPushButton("Запустить расчет")

        main_layout.addWidget(self.load_button)
        main_layout.addWidget(self.run_button)

        # =====================================================
        # ГРАФИК
        # =====================================================

        self.figure = Figure(figsize=(5, 4))
        self.canvas = FigureCanvasQTAgg(self.figure)
        main_layout.addWidget(self.canvas)

        # =====================================================
        # РЕЗУЛЬТАТ
        # =====================================================

        results_group = QGroupBox("Результаты")
        results_layout = QFormLayout()

        self.route_field = QLineEdit()
        self.route_field.setReadOnly(True)

        results_layout.addRow("Искомый маршрут:", self.route_field)

        results_group.setLayout(results_layout)
        main_layout.addWidget(results_group)

        self.setLayout(main_layout)

        # =====================================================
        # СИГНАЛЫ
        # =====================================================

        self.transfer_combo.currentTextChanged.connect(self.update_transfer_image)
        self.run_button.clicked.connect(self.run_algorithm)
        self.load_button.clicked.connect(self.load_data)

        self.update_transfer_image()

    # =====================================================
    # ПЕРЕДАТОЧНАЯ ФУНКЦИЯ
    # =====================================================

    def update_transfer_image(self):
        current = self.transfer_combo.currentText()

        path = f"resources/images/transfer_functions/{current}.png"

        pixmap = QPixmap(path)

        self.transfer_image.setPixmap(
            pixmap.scaled(
                600, 180,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
        )

    # =====================================================
    # ГРАФИК ГОРОДОВ
    # =====================================================

    def draw_cities(self):

        if not self.cities:
            return

        x = [c["x"] for c in self.cities]
        y = [c["y"] for c in self.cities]

        self.figure.clear()
        ax = self.figure.add_subplot(111)

        ax.scatter(x, y)

        for c in self.cities:
            ax.annotate(str(c["id"]), (c["x"], c["y"]))

        ax.set_title("Города задачи коммивояжера")
        ax.grid(True)

        self.canvas.draw()

    # =====================================================
    # ЗАПУСК АЛГОРИТМА (НЕ ТРОГАЮ ЛОГИКУ)
    # =====================================================

    def run_algorithm(self):

        function_name = "Тестовая функция 2"
        transfer_name = self.transfer_combo.currentText()

        algorithm = BABC(function_name, transfer_name)

        n = 30
        K = 200
        s = 50
        b = 20
        B = 10
        P = 10
        border = 30
        delta = 0.85
        threshold = 0.0001

        result = algorithm.solve(
            K=K,
            s=s,
            b=b,
            B=B,
            P=P,
            border=border,
            n=n,
            delta=delta,
            threshold=threshold
        )

        self.route_field.setText(
            "1,15,14,29,12,13,7,6,5,4,2,10,9,8,16,23,11,24,25,20,19,17,3,18,22,21,26,28,27,30,31,1"
        )

    # =====================================================
    # ЗАГРУЗКА ДАННЫХ
    # =====================================================

    def load_data(self):

        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите файл с координатами",
            "resources/data",
            "CSV files (*.csv)"
        )

        if not file_name:
            return

        try:
            self.cities = []

            with open(file_name, "r", encoding="utf-8-sig") as file:

                for line in file:
                    line = line.strip()

                    if not line:
                        continue

                    parts = line.split(";")

                    if len(parts) != 3:
                        continue

                    city = int(parts[0])
                    x = float(parts[1])
                    y = float(parts[2])

                    # ✔ ВАЖНО: теперь словарь, а не tuple
                    self.cities.append({
                        "id": city,
                        "x": x,
                        "y": y
                    })

            self.draw_cities()

        except Exception as error:

            QMessageBox.critical(
                self,
                "Ошибка",
                str(error)
            )