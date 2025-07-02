from PyQt5.QtWidgets import (
    QApplication, QDockWidget, QWidget,
    QVBoxLayout, QLabel, QHBoxLayout, QPushButton
)
from PyQt5.QtCore import Qt, QSize


class NumberDock(QDockWidget):
    _instance_counter = 0

    def __init__(self, parent=None):
        super().__init__("Number", parent)
        # Auto-increment instance count to ensure unique name
        NumberDock._instance_counter += 1
        self.setObjectName(f"number_dock_{NumberDock._instance_counter}")

        self.setAllowedAreas(Qt.AllDockWidgetAreas)
        self.setFloating(True)
        self.move(200, 150)

        self.setFeatures(
            QDockWidget.DockWidgetClosable |
            QDockWidget.DockWidgetMovable |
            QDockWidget.DockWidgetFloatable
        )

        self.is_maximized = False
        self.normal_geometry = self.geometry()

        self.setTitleBarWidget(self.create_custom_title_bar())

        label = QLabel(str(NumberDock._instance_counter))
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 48px; color: #333; padding: 20px;")

        content = QWidget()
        content.setStyleSheet("background-color: lightblue;")

        layout = QVBoxLayout(content)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.addWidget(label)
        self.setWidget(content)

    def create_custom_title_bar(self):
        bar = QWidget()
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(5, 2, 5, 2)

        title = QLabel("Number")
        title.setStyleSheet("font-weight: bold;")
        layout.addWidget(title)
        layout.addStretch()

        # Dock/Undock button
        self.dock_btn = QPushButton("⧉")
        self.dock_btn.setFixedSize(QSize(24, 24))
        self.dock_btn.setStyleSheet("background: transparent; border: none;")
        self.dock_btn.clicked.connect(self.toggle_dock)
        layout.addWidget(self.dock_btn)

        # Maximize/Restore button
        self.max_btn = QPushButton("🗖")
        self.max_btn.setFixedSize(QSize(24, 24))
        self.max_btn.setStyleSheet("background: transparent; border: none;")
        self.max_btn.clicked.connect(self.toggle_maximize_restore)
        layout.addWidget(self.max_btn)

        # Close button
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(QSize(24, 24))
        close_btn.setStyleSheet("background: transparent; border: none;")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)

        return bar

    def toggle_maximize_restore(self):
        screen = QApplication.screenAt(self.frameGeometry().center()) or QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()

        if not self.is_maximized:
            # Save geometry before maximizing
            if self.isFloating():
                self.normal_geometry = self.geometry()
            else:
                self.normal_geometry = self.frameGeometry()
                self.setFloating(True)

            self.setGeometry(screen_geometry)
            self.max_btn.setText("🗗")
            self.is_maximized = True

        else:
            if self.isFloating():
                self.setGeometry(self.normal_geometry)
                self.max_btn.setText("🗖")
                self.is_maximized = False

    def toggle_dock(self):
        if self.is_maximized:
            self.toggle_maximize_restore()

        if self.isFloating():
            self.setFloating(False)
            self.dock_btn.setText("⧉")
        else:
            self.setFloating(True)
            self.move(200, 150)
            self.dock_btn.setText("⧉")



