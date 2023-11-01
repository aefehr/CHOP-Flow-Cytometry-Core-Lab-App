from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton
from PySide6.QtGui import QFont, Qt
from PySide6.QtCore import Qt
from datetime import datetime
from PySide6.QtGui import QGuiApplication
from PySide6.QtCore import Qt, QTimer, QPoint
from PySide6.QtGui import QGuiApplication, QCursor

class MiniGUI(QWidget):
    def __init__(self, name, email,login_event, window, parent=None):
        super().__init__(parent)
        self.window = window
        self.expanded = True
        self.initial_size = None
        self.login_event = login_event
        
        # Mouse Idle Detection setup
        self.last_mouse_position = QPoint()
        self.idle_timer = QTimer(self)
        self.idle_timer.timeout.connect(self.check_mouse_idle)
        # 5 seconds for testing
        self.idle_timer.start(5000)
        
        self.setStyleSheet("background-color: #FFFFFF;")
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        
        main_layout = QHBoxLayout(self)

        # Left side layout for user info
        left_layout = QVBoxLayout()
        
        # Displaying the provided name
        name_label = QLabel(name)
        name_label.setFont(QFont("Arial", 16, QFont.Bold))
        left_layout.addWidget(name_label)

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
    
    def check_mouse_idle(self):
        current_mouse_position = QCursor.pos()

        if current_mouse_position == self.last_mouse_position:
            print("Mouse is idle.")
            # Logout after inactivity
            self.logout()
        else:
            print(f"Mouse moved to ({current_mouse_position.x()}, {current_mouse_position.y()})")
            self.last_mouse_position = current_mouse_position
    
    def mouseMoveEvent(self, event):
        # If the mouse moves, reset the timer
        self.last_mouse_position = QCursor.pos()
        super().mouseMoveEvent(event)

    def logout(self):
        if self.login_event:
            # Record logout event before closing the MiniGUI
            self.login_event.logout_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            logout_event_id = self.login_event.record_logout()

            if logout_event_id:
                print(f"Logout successful. Logout event recorded with ID {logout_event_id}")
            else:
                print("Error recording logout event.")

            # Stop the idle timer and close the MiniGUI
            self.idle_timer.stop()
            self.close()
            self.window.show()

    def toggle_size(self):
        # Minimize the window
        self.showMinimized()
    
