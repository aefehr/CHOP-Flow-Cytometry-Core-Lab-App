from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton
from PySide6.QtGui import QFont, Qt
from PySide6.QtCore import Qt
from backend.cores_sqlite3 import User, Event
from datetime import datetime
from PySide6.QtGui import QGuiApplication

class MiniGUI(QWidget):
    def __init__(self, name, email,login_event, window, parent=None):
        super().__init__(parent)
        self.window = window

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
        #user = User.from_database_by_email(email)

        #if user:
            # User name
            #name_label = QLabel(user.name)
            #name_label.setFont(QFont("Arial", 16, QFont.Bold))
            #left_layout.addWidget(name_label)
        
        # Displaying the provided name
        name_label = QLabel(name)
        name_label.setFont(QFont("Arial", 16, QFont.Bold))
        left_layout.addWidget(name_label)

        # User email
        #email_label = QLabel(user.email)
        #left_layout.addWidget(email_label)

        # Remaining user info
        email_label = QLabel(email)
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
            self.window.show()

    def toggle_size(self):
        # Minimize the window
        self.showMinimized()