from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout
from frontend.EmergencyGUI import EmergencyGUI
from PySide6.QtCore import Qt
from frontend.iLabGUI import iLabGUI
from backend.cores_ilab import login_iLab, get_user_info

class ErrorGUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)

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
        if self.parent() is not None:
            # Get the parent (main window) instance
            parent = self.parent()

            # Implement the code here to open the iLab login window similar to your MainWindow
            # Replace this with your actual implementation

            browser, logged_in = login_iLab()  # Implement this according to your requirements

            if logged_in:
                # Retrieve user information from iLab
                name, phone, email, lab_list = get_user_info(browser, logged_in)

                # Create a new instance of iLabGUI if it doesn't exist
                if parent.ilab_window is None:
                    parent.ilab_window = iLabGUI(parent)

                # Set user information in the existing iLabGUI instance
                parent.ilab_window.set_user_info(name, email)

                # Show the iLabGUI window
                parent.ilab_window.show()

                # Hide the error window
                self.close()

            # for else, it should open emergency GUI
            else: 
                self.emergency_window = EmergencyGUI()
                self.emergency_window.show_on_top()
                self.close()

    def open_emergency(self):
        self.emergency_window = EmergencyGUI()
        self.emergency_window.show_on_top()
        self.close()
    
    def show_on_top(self):
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.show()
        self.raise_()