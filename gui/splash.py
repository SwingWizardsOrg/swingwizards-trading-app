from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QProgressBar
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QTimer, QPoint
import os

class SplashScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.drag_pos = None
        self.counter = 0
        
        # Setup UI
        self.setup_ui()
        
        # Start loading animation
        self.start_loading()

    def setup_ui(self):
        # Main container
        self.container = QWidget(self)
        self.container.setStyleSheet("""
            background-color: #151515;
            border-radius: 20px;
        """)
        self.container.setFixedSize(400, 300)

        # Layout
        layout = QVBoxLayout(self.container)
        layout.setContentsMargins(30, 30, 30, 20)
        layout.setSpacing(10)

        # Logo
        self.logo = QLabel()
        self.load_logo()
        self.logo.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.logo)

        # Title
        self.title = QLabel("SwingWizards")
        self.title.setFont(QFont("Arial", 18, QFont.Bold))
        self.title.setStyleSheet("color: #88aaff;")
        self.title.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title)

        # Progress bar
        self.progress = QProgressBar()
        self.progress.setFixedHeight(15)
        self.progress.setTextVisible(False)
        self.progress.setStyleSheet("""
            QProgressBar {
                background-color: #333;
                border-radius: 8px;
            }
            QProgressBar::chunk {
                background-color: #88aaff;
                border-radius: 8px;
            }
        """)
        layout.addWidget(self.progress)

        # Status labels
        self.loading_label = QLabel("Loading...")
        self.loading_label.setAlignment(Qt.AlignCenter)
        self.loading_label.setStyleSheet("color: white; font-size: 11px;")
        layout.addWidget(self.loading_label)

        self.step_label = QLabel("Initializing application...")
        self.step_label.setAlignment(Qt.AlignCenter)
        self.step_label.setStyleSheet("color: #555; font-size: 10px;")
        layout.addWidget(self.step_label)

        self.setFixedSize(400, 300)

    def load_logo(self):
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            image_path = os.path.join(base_dir, "assets", "images", "wizard_logo.png")
            if os.path.exists(image_path):
                pixmap = QPixmap(image_path)
                if not pixmap.isNull():
                    self.logo.setPixmap(pixmap.scaled(100, 100, 
                                      Qt.KeepAspectRatio, 
                                      Qt.SmoothTransformation))
        except Exception as e:
            print(f"Error loading logo: {str(e)}")

    def start_loading(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(40)  # Update every 40ms

    def update_progress(self):
        self.counter += 1
        self.progress.setValue(self.counter)
        
        # Update loading text based on progress
        if self.counter < 30:
            self.step_label.setText("Loading core modules...")
        elif self.counter < 60:
            self.step_label.setText("Initializing UI components...")
        elif self.counter < 90:
            self.step_label.setText("Connecting to services...")
        else:
            self.step_label.setText("Finalizing setup...")
            
        if self.counter >= 100:
            self.timer.stop()
            self.close()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.drag_pos:
            self.move(event.globalPos() - self.drag_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.drag_pos = None