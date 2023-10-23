from PySide6.QtWidgets import QMainWindow, QWidget, QPushButton, QApplication, QLineEdit, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout
from PySide6.QtGui import QFont, QGuiApplication
from PySide6.QtCore import Qt
from backend.cores_sqlite3 import User, Event
from datetime import datetime
from backend.cores_ilab import login_iLab, get_user_info
from backend.cores_hash import get_salt_hash
from frontend.emergencyGUI import EmergencyGUI

class iLabGUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.second_window = None # start as none

        layout = QVBoxLayout(self)
        self.setStyleSheet("background-color: #99CCFE;")

        # Create the heading label
        heading_label = QLabel("Flow Cytometry Core Lab @ CHOP")
        heading_font = heading_label.font()
        heading_font.setPointSize(14)
        heading_font.setBold(True)
        heading_label.setFont(heading_font)
        heading_label.setStyleSheet("color: #808285;")
        layout.addWidget(heading_label)

        # Create the "User Registration" label
        registration_label = QLabel("User Registration")
        registration_font = registration_label.font()
        registration_font.setPointSize(18)
        registration_font.setBold(True)
        registration_label.setFont(registration_font)
        registration_label.setStyleSheet("color: #808285;")
        layout.addWidget(registration_label)

        # Create the information confirmation text
        confirmation_text = QLabel("By clicking the button below, I confirm that my information shown below is correct.")
        confirmation_text.setStyleSheet("color: #808285;")
        layout.addWidget(confirmation_text, alignment=Qt.AlignCenter)

        # Create a layout for name and email labels
        # Create a layout for name and email labels
        name_email_layout = QVBoxLayout()

        self.name_label = QLabel("Name: ")
        self.email_label = QLabel("Email: ")

        name_email_layout.addWidget(self.name_label)
        name_email_layout.addWidget(self.email_label)

        # Create a widget to contain the name_email_layout
        name_email_widget = QWidget()
        name_email_widget.setLayout(name_email_layout)

        # Add the name_email_widget to the main layout with center alignment
        layout.addWidget(name_email_widget, alignment=Qt.AlignCenter)

        # Create a layout for password labels and text boxes
        password_layout = QGridLayout()

        password_label1 = QLabel("Password:")
        self.password_edit = QLineEdit(self)
        self.password_edit.setStyleSheet("background-color: white")
        self.password_edit.setPlaceholderText("Enter password...")
        self.password_edit.setEchoMode(QLineEdit.Password)

        password_label2 = QLabel("Re-enter password:")
        self.confirm_password_edit = QLineEdit(self)
        self.confirm_password_edit.setStyleSheet("background-color: white")
        self.confirm_password_edit.setPlaceholderText("Confirm password...")
        self.confirm_password_edit.setEchoMode(QLineEdit.Password)

        password_layout.addWidget(password_label1, 0, 0)
        password_layout.addWidget(self.password_edit, 0, 1)
        password_layout.addWidget(password_label2, 1, 0)
        password_layout.addWidget(self.confirm_password_edit, 1, 1)

        password_layout.setColumnStretch(0, 1)  # Ensure labels are left-aligned

        # Create a widget to contain the password_layout
        password_widget = QWidget()
        password_widget.setLayout(password_layout)

        # Add the password_widget to the main layout with center alignment
        layout.addWidget(password_widget, alignment=Qt.AlignCenter)

        # Save My Profile button with rounded edges
        save_button = QPushButton("Save My Profile", self)
        save_button.setStyleSheet("background-color: lightgray;")
        save_button.clicked.connect(self.save_profile)
        layout.addWidget(save_button, alignment=Qt.AlignCenter)  # Center align the button

        # Create the italicized note
        note_label = QLabel("The login info above will be used on all instruments in the Flow Core Lab.")
        note_font = note_label.font()
        note_font.setItalic(True)
        note_label.setFont(note_font)
        note_label.setStyleSheet("color: #808285;")
        layout.addWidget(note_label, alignment=Qt.AlignCenter)
    
    def set_user_info(self, name, email):
        self.name_label.setText(f"Name: {name}")
        self.email_label.setText(f"Email: {email}")
    
    def save_profile(self):
        # Get the entered information
        name = self.name_label.text().split(": ")[1]
        email = self.email_label.text().split(": ")[1]
        password = self.password_edit.text()
        confirm_password = self.confirm_password_edit.text()

        # Validate password and confirm password match
        if password == confirm_password:
            salt_db_str, hash_db_str = get_salt_hash(email,password)
            # Create a new user in the database with the provided information
            new_user = User()
            new_user.name = name
            new_user.email = email
            new_user.salt = salt_db_str
            new_user.hash = hash_db_str

            # Add the user to the database
            user_id = new_user.add_user()

            if user_id:
                print(f"User added successfully with ID {user_id}")
                login_event = Event()
                login_event.email = email
                login_event.login_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                login_event.login_type = 'local'  # may need to be adjusted
                login_event_id = login_event.record_login()

                # EDIT 
                self.second_window = MiniGUI(email, login_event)  # Store it as an instance variable
                self.second_window.show()
                #txt_box_1.clear()
                #txt_box_2.clear()
                self.hide()

                #second_window = MiniGUI(email, login_event)
                #second_window.show()
                #second_window.raise_()
                #second_window.activateWindow()
                #self.close()
            else:
                print("Error adding user to the database. Handle this case accordingly.")
        else:
            print("Password and confirm password do not match. Handle this case accordingly.")


class MiniGUI(QWidget):
    def __init__(self, email,login_event, parent=None):
        super().__init__(parent)

        self.expanded = True  # Start with the window expanded
        self.initial_size = None

        self.login_event = login_event

        self.setStyleSheet("background-color: #FFFFFF;")

        # Set window flags to hide the title bar
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)

        main_layout = QHBoxLayout(self)

        # Left side layout for user info
        left_layout = QVBoxLayout()

        # Get user information from the database using email
        user = User.from_database_by_email(email)

        if user:
            # User name
            name_label = QLabel(user.name)
            name_label.setFont(QFont("Arial", 16, QFont.Bold))
            left_layout.addWidget(name_label)

            # User email
            email_label = QLabel(user.email)
            left_layout.addWidget(email_label)

            # Login time (formatted)
            login_time_label = QLabel(f"Login time: {datetime.now().strftime('%I:%M %p')}")
            left_layout.addWidget(login_time_label)

        main_layout.addLayout(left_layout)

        # Right side layout for buttons
        right_layout = QVBoxLayout()

        self.logout_button = QPushButton("Logout", self)
        self.logout_button.clicked.connect(self.logout)
        right_layout.addWidget(self.logout_button)

        self.collapse_button = QPushButton("Minimize", self)
        self.collapse_button.clicked.connect(self.toggle_size)
        right_layout.addWidget(self.collapse_button)

        main_layout.addLayout(right_layout)

        # Move the window to the left side of the screen
        primary_screen = QGuiApplication.primaryScreen()
        screen_geometry = primary_screen.geometry()
        self.move(screen_geometry.left(), screen_geometry.bottom() - self.height())

    def logout(self):
        if self.login_event:
            # Record logout event before closing the MiniGUI
            self.login_event.logout_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            logout_event_id = self.login_event.record_logout()

            if logout_event_id:
                print(f"Logout successful. Logout event recorded with ID {logout_event_id}")
            else:
                print("Error recording logout event.")

        # Close the MiniGUI and show the main window
        self.close()
        window.show()

    def toggle_size(self):
        # Minimize the window
        self.showMinimized()

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

                # Record login event
                login_event = Event()
                login_event.email = email
                login_event.login_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                login_event.login_type = 'local'  # may need to be adjusted
                login_event_id = login_event.record_login()

                if login_event_id:
                    print(f"Login successful. Login event recorded with ID {login_event_id}")
                    second_window = MiniGUI(email, login_event)
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
                self.ilab_window = iLabGUI()

            # Set user information in the existing iLabGUI instance
            self.ilab_window.set_user_info(name, email)

            # Show the iLabGUI window
            self.ilab_window.show()

            # Hide the main window
            self.hide()

        else:
            # Create and show the emergencyGUI window
            self.emergency_window = EmergencyGUI()
            self.emergency_window.show_on_top()
            
            

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()