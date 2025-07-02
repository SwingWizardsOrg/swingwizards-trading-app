from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QFormLayout, QHBoxLayout
)
import sys

class LoginForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("API Login")
        self.setFixedSize(300, 180)  # Slightly taller to fit the extra field
        self.init_ui()

    def init_ui(self):
        # Labels and input fields
        secret_label = QLabel("Secret key")
        self.secret_input = QLineEdit()

        api_label = QLabel("API key")
        self.api_input = QLineEdit()

        username_label = QLabel("Username")
        self.username_input = QLineEdit()

        # Button
        self.connect_btn = QPushButton("CONNECT")
        self.connect_btn.setFixedWidth(80)

        # Form layout
        form_layout = QFormLayout()
        form_layout.addRow(secret_label, self.secret_input)
        form_layout.addRow(api_label, self.api_input)
        form_layout.addRow(username_label, self.username_input)

        # Center button horizontally
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.connect_btn)
        btn_layout.addStretch()

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addSpacing(10)
        main_layout.addLayout(btn_layout)

        self.setLayout(main_layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginForm()
    window.show()
    sys.exit(app.exec_())
