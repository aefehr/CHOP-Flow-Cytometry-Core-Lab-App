from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QGridLayout
from PySide6.QtCore import Qt

class EmergencyGUI(QWidget):
    def __init__(self):
        super().__init__()

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

        layout.addWidget(request_button)

        self.setLayout(layout)

    def show_on_top(self):
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.show()
        self.raise_()
    

