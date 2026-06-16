from PyQt6.QtWidgets import QMainWindow, QTabWidget

from ui.tab_babc import BABC_Tab
from ui.tab_bgoa import BGOA_Tab
from ui.tab_blj import BLJ_Tab
from ui.tab_bsa import BSA_Tab
from ui.tab_problem import TSP_Tab


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Заголовок окна
        self.setWindowTitle(
            "Метаэвристические алгоритмы бинарной оптимизации"
        )

        # Размер окна
        self.resize(900, 650)

        # Создание панели вкладок
        tabs = QTabWidget()

        # Добавление вкладок
        tabs.addTab(BABC_Tab(), "BABC")
        tabs.addTab(BGOA_Tab(), "BGOA-TVG")
        tabs.addTab(BLJ_Tab(), "B-LJ")
        tabs.addTab(BSA_Tab(), "B-SA")
        tabs.addTab(TSP_Tab(), "Задача комивояжера")

        # Центральный элемент
        self.setCentralWidget(tabs)