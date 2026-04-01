import sys

from PySide6.QtWidgets import QApplication

from .embedded_assets import get_logo_icon
from .ui.main_window import MainWindow


class Termnal:

    def __init__(self) -> None:
        self.app: QApplication | None = None
        self.window: MainWindow | None = None

    def run(self) -> int:
        self.app = QApplication(sys.argv)
        self.app.setWindowIcon(get_logo_icon())
        self.window = MainWindow()
        self.window.show()
        return self.app.exec()
