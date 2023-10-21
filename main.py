from PySide6.QtWidgets import QApplication
from frontend.GUI import MainWindow
from backend.cores_sqlite3 import initialize_database
import os
# Import other necessary modules

def main():
    # Initialize the database
    initialize_database()

    # Create the Qt Application
    app = QApplication([])

    # Create the GUI window
    window = MainWindow()
    window.show()

    # Start the application event loop
    app.exec()

if __name__ == "__main__":
    main()