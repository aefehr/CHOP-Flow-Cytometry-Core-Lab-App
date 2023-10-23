from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QGridLayout, QLineEdit, QPushButton
from PySide6.QtGui import QFont, Qt
from PySide6.QtCore import Qt
from backend.cores_sqlite3 import User, Event
from datetime import datetime
from backend.cores_hash import get_salt_hash
from frontend.MiniGUI import MiniGUI

class iLabGUI(QWidget):
    def __init__(self, main_window, parent=None):
        super().__init__(parent)

        self.second_window = None # start as none
        self.main_window = main_window

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
                self.second_window = MiniGUI(email, login_event, self.main_window)  # Store it as an instance variable
                self.second_window.show()
                self.hide()

            else:
                print("Error adding user to the database. Handle this case accordingly.")
        else:
            print("Password and confirm password do not match. Handle this case accordingly.")
