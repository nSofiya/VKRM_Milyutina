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


class TSP_Tab(QWidget):
    def __init__(self):
        super().__init__()
        self.cities_data = []

        # Главный layout
        main_layout = QVBoxLayout()

        # =====================================================
        # БЛОК ПАРАМЕТРОВ
        # =====================================================

        parameters_group = QGroupBox("Параметры")
        parameters_layout = QFormLayout()

        # -----------------------------------------------------
        # 1. Алгоритм
        # -----------------------------------------------------

        self.algorithm_combo = QComboBox()

        self.algorithm_combo.addItems([
            "BABC",
            "BGOA",
            "B-LJ",
            "B-SA"
        ])

        parameters_layout.addRow(
            "Алгоритм:",
            self.algorithm_combo
        )

        # -----------------------------------------------------
        # 2. Передаточная функция
        # -----------------------------------------------------

        self.transfer_combo = QComboBox()

        self.transfer_combo.addItems([
            "S1",
            "S2",
            "S3",
            "S4",
            "V1",
            "V2",
            "V3",
            "V4",
            "VG",
            "SIN"
        ])

        parameters_layout.addRow(
            "Передаточная функция:",
            self.transfer_combo
        )

        # Поле изображения передаточной функции
        self.transfer_image = QLabel()
        self.transfer_image.setFixedHeight(200)
        self.transfer_image.setAlignment(Qt.AlignmentFlag.AlignCenter)

        parameters_layout.addRow(
            "Формула:",
            self.transfer_image
        )

        # -----------------------------------------------------
        # 3. Правило бинаризации
        # -----------------------------------------------------

        self.binary_combo = QComboBox()

        self.binary_combo.addItems([
            "Стандартный метод",
            "Метод дополнения",
            "Метод статистической вероятности",
            "Элитистский метод",
            "Метод элитистской рулетки"
        ])

        parameters_layout.addRow(
            "Правило бинаризации:",
            self.binary_combo
        )

        parameters_group.setLayout(parameters_layout)

        main_layout.addWidget(parameters_group)

        # =====================================================
        # КНОПКА ЗАГРУЗКИ ДАННЫХ
        # =====================================================

        self.load_button = QPushButton("Загрузить данные")

        main_layout.addWidget(self.load_button)

        # =====================================================
        # КНОПКА ЗАПУСКА
        # =====================================================

        self.run_button = QPushButton("Запустить расчет")

        main_layout.addWidget(self.run_button)

        # =====================================================
        # БЛОК РЕЗУЛЬТАТОВ
        # =====================================================

        results_group = QGroupBox("Результаты")
        results_layout = QFormLayout()

        # Поле искомого маршрута

        self.route_field = QLineEdit()
        self.route_field.setReadOnly(True)

        results_layout.addRow(
            "Искомый маршрут:",
            self.route_field
        )

        results_group.setLayout(results_layout)

        main_layout.addWidget(results_group)

        # =====================================================
        # УСТАНОВКА LAYOUT
        # =====================================================

        self.setLayout(main_layout)

        # =====================================================
        # ПОДКЛЮЧЕНИЕ СОБЫТИЙ
        # =====================================================

        self.transfer_combo.currentTextChanged.connect(
            self.update_transfer_image
        )

        self.run_button.clicked.connect(self.run_algorithm)

        self.load_button.clicked.connect(self.load_data)

        # Загрузка стартовых изображений
        self.update_transfer_image()

    # =========================================================
    # ОБНОВЛЕНИЕ КАРТИНКИ ПЕРЕДАТОЧНОЙ ФУНКЦИИ
    # =========================================================

    def update_transfer_image(self):
        current_transfer = self.transfer_combo.currentText()

        image_path = (
            f"resources/images/transfer_functions/"
            f"{current_transfer}.png"
        )

        pixmap = QPixmap(image_path)

        self.transfer_image.setPixmap(
            pixmap.scaled(
                600,
                180,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
        )

    # =========================================================
    # ЗАПУСК АЛГОРИТМА
    # =========================================================

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

        # =========================
        # 4. Запуск алгоритма
        # =========================

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
            self.cities_data = []

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

                    self.cities_data.append(
                        (city, x, y)
                    )

            QMessageBox.information(
                self,
                "Успех",
                f"Загружено городов: {len(self.cities_data)}"
            )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Ошибка",
                str(error)
            )