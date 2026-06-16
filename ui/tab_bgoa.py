from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QComboBox,
    QLineEdit,
    QGroupBox,
    QFormLayout,
    QSpinBox,
    QMessageBox
)

from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from algorithms.babc import BABC

class BGOA_Tab(QWidget):
    def __init__(self):
        super().__init__()

        # Главный layout
        main_layout = QVBoxLayout()

        # =====================================================
        # БЛОК ПАРАМЕТРОВ
        # =====================================================

        parameters_group = QGroupBox("Параметры")
        parameters_layout = QFormLayout()

        # -----------------------------------------------------
        # 1. Целевая функция
        # -----------------------------------------------------

        self.function_combo = QComboBox()

        self.function_combo.addItems([
            "Тестовая функция 1",
            "Тестовая функция 2",
            "Тестовая функция 3"
        ])

        parameters_layout.addRow(
            "Целевая функция:",
            self.function_combo
        )

        # Поле размерности

        self.dimension_spin = QSpinBox()

        self.dimension_spin.setMinimum(1)
        self.dimension_spin.setMaximum(1000)
        self.dimension_spin.setValue(5)

        parameters_layout.addRow(
            "Размерность:",
            self.dimension_spin
        )

        # Поле изображения функции
        self.function_image = QLabel()
        self.function_image.setFixedHeight(200)
        self.function_image.setAlignment(Qt.AlignmentFlag.AlignCenter)

        parameters_layout.addRow(
            "Формула:",
            self.function_image
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
        # КНОПКА ЗАПУСКА
        # =====================================================

        self.run_button = QPushButton("Запустить расчет")

        main_layout.addWidget(self.run_button)

        # =====================================================
        # БЛОК РЕЗУЛЬТАТОВ
        # =====================================================

        results_group = QGroupBox("Результаты")
        results_layout = QFormLayout()

        # Поле минимума функции
        self.minimum_field = QLineEdit()
        self.minimum_field.setReadOnly(True)

        results_layout.addRow(
            "Минимум функции:",
            self.minimum_field
        )

        # Поле значения в точке минимума
        self.point_field = QLineEdit()
        self.point_field.setReadOnly(True)

        results_layout.addRow(
            "Значение в точке минимума:",
            self.point_field
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

        self.function_combo.currentTextChanged.connect(
            self.update_function_image
        )

        self.transfer_combo.currentTextChanged.connect(
            self.update_transfer_image
        )

        self.run_button.clicked.connect(self.run_algorithm)

        # Загрузка стартовых изображений
        self.update_function_image()
        self.update_transfer_image()

    # =========================================================
    # ОБНОВЛЕНИЕ КАРТИНКИ ФУНКЦИИ
    # =========================================================

    def update_function_image(self):
        current_function = self.function_combo.currentText()

        image_paths = {
            "Тестовая функция 1": "resources/images/functions/function1.png",
            "Тестовая функция 2": "resources/images/functions/function2.png",
            "Тестовая функция 3": "resources/images/functions/function3.png"
        }

        pixmap = QPixmap(image_paths[current_function])

        self.function_image.setPixmap(
            pixmap.scaled(
                600,
                180,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
        )

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
        # =========================
        # 1. Получаем параметры из GUI
        # =========================

        function_name = self.function_combo.currentText()
        transfer_name = self.transfer_combo.currentText()

        # =========================
        # 2. Создаём алгоритм
        # =========================

        algorithm = BABC(function_name, transfer_name)

        # =========================
        # 3. Параметры (пока фиксированные)
        # =========================

        n = self.dimension_spin.value()
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

        # =========================
        # 5. Вывод результата в GUI
        # =========================

        self.minimum_field.setText(str(result["best_value"]))

        self.point_field.setText(str(result["best_point"]))

        QMessageBox.information(
            self,
            "Готово",
            "Вычисления успешно выполнены"
        )