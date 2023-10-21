from PySide6.QtWidgets import QMainWindow, QLabel, QApplication, QWidget
from PySide6.QtCore import Qt

class EmergencyGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Emergency Access")
        self.setGeometry(100, 100, 400, 200)  # Adjust the window dimensions

        label = QLabel("Emergency Access", self)
        label.setAlignment(Qt.AlignCenter)

    def show_on_top(self):
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.show()
        self.raise_()
