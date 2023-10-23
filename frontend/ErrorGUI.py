from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout
from frontend.EmergencyGUI import EmergencyGUI
from PySide6.QtCore import Qt

class ErrorGUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.emergency_window = None

        # Create a QVBoxLayout to stack widgets vertically
        layout = QVBoxLayout()

        # Text label
        text_label = QLabel("Would you like to try logging in through iLab again or request emergency access?", self)

        # "Log in through iLab" button
        ilab_button = QPushButton("Log in through iLab", self)
        ilab_button.clicked.connect(self.open_iLab)

        # "Request Emergency Access" button
        emergency_button = QPushButton("Request Emergency Access", self)
        emergency_button.clicked.connect(self.open_emergency)

        # Add widgets to the layout in the desired order
        layout.addWidget(text_label)
        layout.addWidget(ilab_button)
        layout.addWidget(emergency_button)

        # Set the layout for the ErrorGUI
        self.setLayout(layout)

    def open_iLab(self):
        pass

    def open_emergency(self):
        self.emergency_window = EmergencyGUI()
        self.emergency_window.show_on_top()
        self.close()
    
    def show_on_top(self):
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.show()
        self.raise_()