# from PyQt5.QtWidgets import QDockWidget, QWidget, QVBoxLayout, QLabel
# from PyQt5.QtCore import Qt

# class NumberDock(QDockWidget):
#     def __init__(self, parent=None):
#         super().__init__("Number", parent)
#         self.setAllowedAreas(Qt.AllDockWidgetAreas)
#         self.setFloating(True)
#         self.move(200, 150)  # Move to (x=200, y=150) on screen

#         self.setStyleSheet("""
#             QDockWidget {
#                 border: 2px solid #888;
#                 titlebar-close-icon: url(none);
#                 titlebar-normal-icon: url(none);
#             }
#         """)

#         label = QLabel("2")
#         label.setAlignment(Qt.AlignCenter)
#         label.setStyleSheet("font-size: 48px; color: #333; padding: 20px;")
        
#         content = QWidget()
#         content.setStyleSheet("background-color: lightblue;") # <--- Adds margin julius

#         layout = QVBoxLayout(content)
#         layout.setContentsMargins(20, 20, 20, 20)  # <--- Adds margin
#         layout.addWidget(label)
#         self.setWidget(content)
# **** ALL CODE ABOVE WORKS****

# from PyQt5.QtWidgets import (
#     QDockWidget, QWidget, QVBoxLayout, QLabel,
#     QHBoxLayout, QPushButton, QApplication
# )
# from PyQt5.QtCore import Qt, QSize
# from PyQt5.QtGui import QIcon


# class NumberDock(QDockWidget):
#     def __init__(self, parent=None):
#         super().__init__("Number", parent)
#         self.setAllowedAreas(Qt.AllDockWidgetAreas)
#         self.setFloating(True)
#         self.move(200, 150)  # Default position

#         self.setTitleBarWidget(self.create_custom_title_bar())
#         self.is_maximized = False

#         label = QLabel("2")
#         label.setAlignment(Qt.AlignCenter)
#         label.setStyleSheet("font-size: 48px; color: #333; padding: 20px;")

#         content = QWidget()
#         content.setStyleSheet("background-color: lightblue;")

#         layout = QVBoxLayout(content)
#         layout.setContentsMargins(20, 20, 20, 20)
#         layout.addWidget(label)
#         self.setWidget(content)

#     def create_custom_title_bar(self):
#         bar = QWidget()
#         layout = QHBoxLayout(bar)
#         layout.setContentsMargins(5, 2, 5, 2)

#         title = QLabel("Number")
#         title.setStyleSheet("font-weight: bold;")
#         layout.addWidget(title)
#         layout.addStretch()

#         # Maximize/Restore button
#         self.max_btn = QPushButton("🗖")
#         self.max_btn.setFixedSize(QSize(24, 24))
#         self.max_btn.setStyleSheet("background: transparent; border: none;")
#         self.max_btn.clicked.connect(self.toggle_maximize_restore)
#         layout.addWidget(self.max_btn)

#         # Close button
#         close_btn = QPushButton("✕")
#         close_btn.setFixedSize(QSize(24, 24))
#         close_btn.setStyleSheet("background: transparent; border: none;")
#         close_btn.clicked.connect(self.close)
#         layout.addWidget(close_btn)

#         return bar

#     def toggle_maximize_restore(self):
#         screen = QApplication.screenAt(self.frameGeometry().center())
#         if not screen:
#             screen = QApplication.primaryScreen()
#         screen_geometry = screen.availableGeometry()

#         if not self.is_maximized:
#             self.normal_geometry = self.geometry()
#             self.setGeometry(screen_geometry)
#             self.max_btn.setText("🗗")  # Restore icon
#             self.is_maximized = True
#         else:
#             self.setGeometry(self.normal_geometry)
#             self.max_btn.setText("🗖")  # Maximize icon
#             self.is_maximized = False


# from PyQt5.QtWidgets import QDockWidget, QTextEdit
# from PyQt5.QtCore import Qt

# class NumberDock(QDockWidget):
#     def __init__(self, parent=None):
#         super().__init__("Number", parent)
#         self.setAllowedAreas(Qt.AllDockWidgetAreas)
#         self.setFloating(True)

#         self.setStyleSheet("""
#             QDockWidget {
#                 border: 8px solid #FF0000;
#                 titlebar-close-icon: url(none);
#                 titlebar-normal-icon: url(none);
#             }
#             QTextEdit {
#                 font-size: 24px;
#                 color: #333;
#                 padding: 0px;  /* Only affects text padding inside */
#             }
#         """)

#         text_edit = QTextEdit("Number: 2")
#         text_edit.setReadOnly(True)
#         self.setWidget(text_edit)



    # def maximizeDock(self):
    #     if self.isFloating():
    #         screen_geometry = QApplication.primaryScreen().availableGeometry()
    #         self.resize(screen_geometry.width(), screen_geometry.height())
    #         self.move(0, 0)

## we are layoutti##
# from PyQt5.QtWidgets import (
#     QDockWidget, QWidget, QVBoxLayout, QLabel,
#     QHBoxLayout, QPushButton, QApplication
# )
# from PyQt5.QtCore import Qt, QSize, QRect
# from PyQt5.QtGui import QIcon


# class NumberDock(QDockWidget):
#     def __init__(self, parent=None):
#         super().__init__("Number", parent)
#         self.setAllowedAreas(Qt.AllDockWidgetAreas)
#         self.setFloating(True)
#         self.move(200, 150)
#         self.setObjectName("number_dock")


#         self.setFeatures(QDockWidget.DockWidgetClosable | 
#                  QDockWidget.DockWidgetMovable | 
#                  QDockWidget.DockWidgetFloatable)

#         self.is_maximized = False
#         self.normal_geometry = self.geometry()

#         self.setTitleBarWidget(self.create_custom_title_bar())

#         label = QLabel("2")
#         label.setAlignment(Qt.AlignCenter)
#         label.setStyleSheet("font-size: 48px; color: #333; padding: 20px;")

#         content = QWidget()
#         content.setStyleSheet("background-color: lightblue;")

#         layout = QVBoxLayout(content)
#         layout.setContentsMargins(20, 20, 20, 20)
#         layout.addWidget(label)
#         self.setWidget(content)

#     def create_custom_title_bar(self):
#         bar = QWidget()
#         layout = QHBoxLayout(bar)
#         layout.setContentsMargins(5, 2, 5, 2)

#         title = QLabel("Number")
#         title.setStyleSheet("font-weight: bold;")
#         layout.addWidget(title)
#         layout.addStretch()

#         # Dock/Undock button
#         self.dock_btn = QPushButton("⧉")  # ⛶ or ⧉
#         self.dock_btn.setFixedSize(QSize(24, 24))
#         self.dock_btn.setStyleSheet("background: transparent; border: none;")
#         self.dock_btn.clicked.connect(self.toggle_dock)
#         layout.addWidget(self.dock_btn)

#         # Maximize/Restore button
#         self.max_btn = QPushButton("🗖")
#         self.max_btn.setFixedSize(QSize(24, 24))
#         self.max_btn.setStyleSheet("background: transparent; border: none;")
#         self.max_btn.clicked.connect(self.toggle_maximize_restore)
#         layout.addWidget(self.max_btn)

#         # Close button
#         close_btn = QPushButton("✕")
#         close_btn.setFixedSize(QSize(24, 24))
#         close_btn.setStyleSheet("background: transparent; border: none;")
#         close_btn.clicked.connect(self.close)
#         layout.addWidget(close_btn)

#         return bar

#     def toggle_maximize_restore(self):
#         screen = QApplication.screenAt(self.frameGeometry().center()) or QApplication.primaryScreen()
#         screen_geometry = screen.availableGeometry()

#         if not self.is_maximized:
#             # Save current undocked geometry (if undocked)
#             if self.isFloating():
#                 self.normal_geometry = self.geometry()
#             else:
#                 self.normal_geometry = self.frameGeometry()
#                 self.setFloating(True)  # Undock before maximizing

#             # Check if parent MainBar has occupied area saved
#             mainbar = self.parentWidget()
#             if hasattr(mainbar, "occupied_rect"):
#                 remaining_geometry = QRect(screen_geometry)
#                 remaining_geometry.setTop(mainbar.occupied_rect.bottom() + 1)
#                 self.setGeometry(remaining_geometry)
#             else:
#                 self.setGeometry(screen_geometry)

#             self.max_btn.setText("🗗")
#             self.is_maximized = True

#         else:
#             if self.isFloating():
#                 self.setGeometry(self.normal_geometry)
#                 self.max_btn.setText("🗖")
#                 self.is_maximized = False


#     def toggle_dock(self):
#         if self.is_maximized:
#         # Restore first if maximized
#             self.toggle_maximize_restore()

#         if self.isFloating():
#             self.setFloating(False)
#             #self.dock_btn.setText("➚")  # Undock icon
#             self.dock_btn.setIcon(QIcon("D:\swingwizard_client_terminal\assets\icons\maximize.png"))
#         else:
#             self.setFloating(True)
#             self.move(200, 150)
#             self.dock_btn.setText("⧉")  # Dock icon
            
## we are layoutti##

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QDockWidget, QWidget,
    QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QAction, QMenuBar
)
from PyQt5.QtCore import Qt, QSize, QRect
from PyQt5.QtGui import QIcon


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


# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Number Dock Example")
#         self.resize(1000, 700)

#         self.number_docks = []

#         self.create_menu()

#     def create_menu(self):
#         menubar = self.menuBar()
#         dock_menu = menubar.addMenu("Docks")

#         add_dock_action = QAction("Add Number Dock", self)
#         add_dock_action.triggered.connect(self.create_number_dock)
#         dock_menu.addAction(add_dock_action)

# #     def create_number_dock(self):
#         dock = NumberDock(self)
#         self.addDockWidget(Qt.RightDockWidgetArea, dock)
#         dock.show()
#         self.number_docks.append(dock)


# if __name__ == "__main__":
#     app = QApplication([])
#     window = MainWindow()
#     window.show()
#     app.exec_()
