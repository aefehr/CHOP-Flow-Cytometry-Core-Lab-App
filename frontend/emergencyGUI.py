from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QGridLayout
from PySide6.QtCore import Qt
from backend.cores_sqlite3 import User, Event
from datetime import datetime
from frontend.MiniGUI import MiniGUI

class EmergencyGUI(QWidget):
    def __init__(self, main_window):
        super().__init__()

        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)

        self.mini_gui = None # start as none
        self.main_window = main_window

        self.setWindowTitle("Emergency Access")
        self.setGeometry(100, 100, 400, 200)
        self.setStyleSheet("background-color: #99CCFE;")

        layout = QVBoxLayout(self)

        # Heading label
        heading_label = QLabel("EMERGENCY ACCESS", self)
        heading_label.setAlignment(Qt.AlignCenter)
        heading_label.setStyleSheet("color: darkred; font-size: 18px; font-weight: bold;")
        layout.addWidget(heading_label)

        # Create a layout for password labels and text boxes
        input_layout = QGridLayout()

        labels = ["First name:", "Last name:", "Your email address:", "Your phone number:", "Principal Investigator:"]
        fields = [
            QLineEdit(self),  # First name
            QLineEdit(self),  # Last name
            QLineEdit(self),  # Email
            QLineEdit(self),  # Phone
            QLineEdit(self),  # PI name
        ]

        # Set label alignment to right and black color
        for i, label_text in enumerate(labels):
            label = QLabel(label_text)
            label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            label.setStyleSheet("color:  #808285; font-weight: bold;")
            input_layout.addWidget(label, i, 0)
            input_layout.addWidget(fields[i], i, 1)

        # Set placeholders for fields and adjust field lengths
        for field in fields:
            field.setStyleSheet("background-color: white")
            field.setPlaceholderText("Enter " + field.placeholderText())
            field.setMinimumWidth(200)  # Adjust field length

        # Assign the email line edit to self.email_line_edit
        self.first_name_line_edit = fields[0]
        self.last_name_line_edit = fields[1]
        self.email_line_edit = fields[2]
        self.phone_line_edit = fields[3]
        self.pi_name_line_edit = fields[4]
        
        # Create a widget to contain the input_layout
        input_widget = QWidget()
        input_widget.setLayout(input_layout)

        # Add the input_widget to the main layout with center alignment
        layout.addWidget(input_widget, alignment=Qt.AlignCenter)



        # Create the italicized note with word wrap
        note_label = QLabel(
            "The staff of the Flow Core Lab will be promptly notified that you have requested emergency access to this device.",
            self
        )
        note_label.setStyleSheet("color: darkred; font-style: italic;")  # Note label in red and italic
        note_label.setWordWrap(True)  # Enable word wrap
        note_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        layout.addWidget(note_label, alignment=Qt.AlignCenter)

        # Request button
        request_button = QPushButton("Request Emergency Access", self)
        request_button.setStyleSheet("background-color: lightgray;")
        request_button.clicked.connect(self.request_emergency_access)
        layout.addWidget(request_button)

        # Create the "Cancel" button
        cancel_button = QPushButton("Cancel", self)
        cancel_button.setStyleSheet("background-color: lightgray;")
        layout.addWidget(cancel_button)

        # Connect the "Cancel" button to the cancel method
        cancel_button.clicked.connect(self.cancel)

        self.setLayout(layout)

    def show_on_top(self):
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.show()
        self.raise_()

    def cancel(self):
        self.main_window.show()
        # Close the EmergencyGUI window
        self.close()
     
     # create function for logging in user through emergency access
    def request_emergency_access(self):
        # Collect the user information from the input fields
        email = self.email_line_edit.text()
        first_name = self.first_name_line_edit.text()
        last_name = self.last_name_line_edit.text()
        phone = self.phone_line_edit.text()
        pi_name = self.pi_name_line_edit.text()

        # Create an instance of Event and fill in the event details
        login_event = Event()
        login_event.email = email
        login_event.device = "Aurora alpha"
        login_event.login_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        login_event.login_type = "EMERGENCY"

         # Record the login event in the database
        event_id = login_event.record_login()

        if event_id:
            # TODO: add code to manage emergency access request
            print(f"Emergency login recorded with ID {event_id}")
            
            #mini_gui = MiniGUI(email, login_event, self.main_window)
            #mini_gui.show()
            #self.close()
        else:
            print("Error recording emergency login event.")
            
        
    

