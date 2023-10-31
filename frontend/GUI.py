from PySide6.QtWidgets import QMainWindow, QWidget, QPushButton, QApplication, QLineEdit, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout
from PySide6.QtGui import QFont, QGuiApplication
from PySide6.QtCore import Qt
from backend.cores_sqlite3 import User, Event
from datetime import datetime
from backend.cores_ilab import login_iLab, get_user_info
from backend.cores_hash import get_salt_hash
from frontend.EmergencyGUI import EmergencyGUI
from frontend.iLabGUI import iLabGUI
from frontend.MiniGUI import MiniGUI
from frontend.ErrorGUI import ErrorGUI

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("background-color: #99CCFE;")

        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        #added this
        #self.central_layout = main_layout

        self.ilab_window = None

        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)

        # Title text
        title_text = "Children's Hospital of Philadelphia<br>Flow Cytometry Core Lab"
        label_title = QLabel(title_text, parent=central_widget)
        label_title.setFont(title_font)
        label_title.setStyleSheet("color: #3865B6;")
        label_title.setAlignment(Qt.AlignTop | Qt.AlignLeft)  # Align text to the top left
        main_layout.addWidget(label_title)

        device_font = QFont()
        device_font.setBold(True)
        device_font.setPointSize(25)

        label_aurora = QLabel("Aurora alpha", parent=central_widget)
        label_aurora.setFont(device_font)
        label_aurora.setStyleSheet("color: #005587;")
        label_aurora.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(label_aurora)

        label_spectral_analyzer = QLabel("Spectral analyzer", parent=central_widget)
        label_spectral_analyzer.setStyleSheet("color: gray;")
        main_layout.addWidget(label_spectral_analyzer)

        input_layout = QHBoxLayout(central_widget)

        label_1 = QLabel('Username:', parent=central_widget)
        input_layout.addWidget(label_1)
        txt_box_1 = QLineEdit(parent=central_widget)
        txt_box_1.setPlaceholderText("Enter email...")
        txt_box_1.setStyleSheet("background-color: white;")
        input_layout.addWidget(txt_box_1)

        main_layout.addLayout(input_layout)

        password_layout = QHBoxLayout(central_widget)

        label_2 = QLabel('Password:', parent=central_widget)
        password_layout.addWidget(label_2)

        txt_box_2 = QLineEdit(parent=central_widget)
        txt_box_2.setPlaceholderText("Enter password...")
        txt_box_2.setStyleSheet("background-color: white;")
        txt_box_2.setEchoMode(QLineEdit.Password)
        password_layout.addWidget(txt_box_2)

        main_layout.addLayout(password_layout)

        login_status_label = QLabel(parent=central_widget)

        def authenticate_user():
            email = txt_box_1.text()
            password = txt_box_2.text()

            if User.authenticate_user(email, password):
                global second_window

                user = User.from_database_by_email(email)

                if user: 
                    # Record login event
                    login_event = Event()
                    login_event.email = email
                    login_event.login_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    login_event.login_type = 'local'  # may need to be adjusted
                    login_event_id = login_event.record_login()

                    if login_event_id:
                        print(f"Login successful. Login event recorded with ID {login_event_id}")
                        # edit 
                        second_window = MiniGUI(user.name, email, login_event, self)
                        second_window.show()
                        txt_box_1.clear()
                        txt_box_2.clear()
                        self.hide()
                    else:
                        print("Error recording login event.")
                        # Handle the error as needed

            else:
                print("Login failed. Invalid password")
                login_status_label.setText('<font color="red">Login failed. Invalid password</font>')


        button_layout = QHBoxLayout(central_widget)

        btn_login = QPushButton("Login", parent=central_widget)
        btn_login.clicked.connect(authenticate_user)
        btn_login.setStyleSheet("background-color: #CAC8C8;")
        button_layout.addWidget(btn_login)

        btnClose = QPushButton("Cancel", parent=central_widget)
        btnClose.clicked.connect(QGuiApplication.instance().quit)
        button_layout.addWidget(btnClose)

        login_layout = QVBoxLayout()
        login_layout.addWidget(login_status_label)
        login_layout.addLayout(button_layout)

        main_layout.addLayout(login_layout)

        label_iLab = QLabel('<a href="none">Login with iLab...</a>', parent=central_widget)
        # label_iLab.setOpenExternalLinks(True)  # Allow opening links in a web browser
        label_iLab.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        label_iLab.linkActivated.connect(self.open_iLab)
        main_layout.addWidget(label_iLab)

    # helper function for opening iLab
    def open_iLab(self):
        browser, logged_in = login_iLab()

        if logged_in:
            # Retrieve user information from iLab
            name, phone, email, lab_list = get_user_info(browser, logged_in)

            # Create a new instance of iLabGUI if it doesn't exist
            if not self.ilab_window:
                self.ilab_window = iLabGUI(self)

            # Set user information in the existing iLabGUI instance
            self.ilab_window.set_user_info(name, email)

            # Show the iLabGUI window
            self.ilab_window.show()

            # Hide the main window
            self.hide()

        else:
            # Create and show the emergencyGUI window
            self.error_window = ErrorGUI(self)
            self.error_window.show_on_top()
            self.hide()
            
            

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()