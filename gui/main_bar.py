import sys
import os
import json
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QToolBar, QAction, QToolButton, QSizePolicy,
    QWidget, QPushButton, QMenu, QWidgetAction, 
    QMessageBox, QFileDialog
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QPoint, QRect, QByteArray

from gui.connections import ConnectionsDock
from gui.menubar_dock import MenuDock
from gui.number_dock import NumberDock
from gui.layoutsdropdown import LayoutManagerWidget

class MainBar(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.is_maximized = False
        self.drag_position = QPoint()
        self.menu_dock = None
        self.number_docks = []


        # Add a button to open the layout manager for testing
        btn = QPushButton("Show Layout Manager")
        btn.clicked.connect(self.show_layout_manager)
        self.setCentralWidget(btn)

        

        # ✅ Set docking behavior first
        self.setDockOptions(
            QMainWindow.AllowNestedDocks |
            QMainWindow.AllowTabbedDocks |
            QMainWindow.AnimatedDocks |
            QMainWindow.GroupedDragging
        )

        
        self.toolbar = QToolBar()
        self.toolbar.setMovable(False)
        self.addToolBar(self.toolbar)
    

        self.actions = [
            ("Menu", "assets/icons/menu.png", self.toggle_menu_dock),
            ("Layouts", "assets/icons/home.png", None),
            ("Collapse/Expand", "assets/icons/monitor.png", self.tabify_all_docks),
            ("QuickAcessTools", "assets/icons/tools.png", None),
            ("TaskManager", "assets/icons/code.png", None),
            ("Connections", "assets/icons/flow.png", self.create_connection_dock),
            ("Settings", "assets/icons/settings.png", None),
            ("Notifications", "assets/icons/Notifications.png", None),
            ("User", "assets/icons/user.png", self.create_number_dock),
        ]

        for name, icon_path, callback in self.actions:
            if not os.path.exists(icon_path):
                print(f"Warning: Icon not found: {icon_path}")
                continue

            if name == "Layouts":
                btn = QToolButton()
                btn.setIcon(QIcon(icon_path))
                btn.setToolTip(name)
                btn.setPopupMode(QToolButton.InstantPopup)

                # 🔽 Create and assign custom dropdown menu
                menu = QMenu(self)
                widget = LayoutManagerWidget(
                    parent=self,
                    save_callback=self.save_layout,
                    load_callback=self.load_layout)
                action = QWidgetAction(menu)
                action.setDefaultWidget(widget)
                menu.addAction(action)

                btn.setMenu(menu)
                self.toolbar.addWidget(btn)
                self.toolbar.addSeparator()
            
            else:
                action = QAction(QIcon(icon_path), name, self)
                action.setToolTip(name)
                if callback:
                    action.triggered.connect(callback)
                self.toolbar.addAction(action)
                self.toolbar.addSeparator()
            
            # ⬇️ Add spacer AFTER QuickAcessTools
            if name == "QuickAcessTools":
                spacer = QWidget()
                spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
                self.toolbar.addWidget(spacer)
                self.toolbar.addSeparator()

            # ⬇️ Add spacer AFTER Settings
            if name == "Settings":
                spacer = QWidget()
                spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
                self.toolbar.addWidget(spacer)
                self.toolbar.addSeparator()

        else:
                    print(f"Warning: Icon not found: {icon_path}")


        self._add_window_controls()

        self.setStyleSheet("""
            QMainWindow, QToolBar {
                background-color: #f0f0f0;
                border: none;
            }
            QToolButton {
                background-color: transparent;
                border: none;
                padding: 5px;
                margin: 2px;
            }
            QToolButton:hover {
                background-color: #e0e0e0;
                border-radius: 3px;
            }
            QToolButton:pressed {
                background-color: #d0d0d0;
            }
        """)

        toolbar_height = self.toolbar.sizeHint().height()
        self.setFixedHeight(toolbar_height)
        self.setGeometry(100, 100, 800, toolbar_height)

    def _add_window_controls(self):
        def add_control(icon_path, tooltip, callback):
            btn = QToolButton()
            if os.path.exists(icon_path):
                btn.setIcon(QIcon(icon_path))
            btn.setToolTip(tooltip)
            btn.clicked.connect(callback)
            self.toolbar.addWidget(btn)
            return btn

        add_control("assets/icons/minimize.png", "Minimize", self.showMinimized)
        self.maximize_btn = add_control("assets/icons/maximize.png", "Maximize", self.toggle_maximize_restore)
        add_control("assets/icons/close.png", "Close", self.close)


    def _clear_number_docks(self):
        """
        Close and remove all NumberDock instances.
        """
        for dock in self.number_docks:
            dock.close()
        self.number_docks.clear()


    def tabify_all_docks(self):
        """
        Dock all floating NumberDocks, then tabify them together with any docked ones.
        """
        all_docks = self.number_docks
        if not all_docks:
            print("No docks found.")
            return

        print(f"Tabifying {len(all_docks)} docks...")

        floating = [d for d in all_docks if d.isFloating()]
        docked = [d for d in all_docks if not d.isFloating()]

        # 1. Force floating docks to dock
        for d in floating:
            d.setFloating(False)
            self.addDockWidget(Qt.RightDockWidgetArea, d)

        # 2. Tabify floating docks
        primary_floating = floating[0] if floating else None
        for d in floating[1:]:
            self.tabifyDockWidget(primary_floating, d)

        # 3. Tabify docked docks
        primary_docked = docked[0] if docked else None
        for d in docked[1:]:
            self.tabifyDockWidget(primary_docked, d)

        # 4. Combine both groups
        if primary_floating and primary_docked:
            self.tabifyDockWidget(primary_floating, primary_docked)

        if primary_floating:
            primary_floating.raise_()
        elif primary_docked:
            primary_docked.raise_()

        print("Tabify complete.")



    def toggle_menu_dock(self):
        if not self.menu_dock:
            self.menu_dock = MenuDock(self)
            self.addDockWidget(Qt.LeftDockWidgetArea, self.menu_dock)
            self.menu_dock.setFloating(True)  # Optional
            self.menu_dock.move(150, 100)     # Optional default position
        self.menu_dock.setVisible(not self.menu_dock.isVisible())


    def create_number_dock(self, dock_id=None):
        dock = NumberDock(self)
        
        if dock_id:
            dock.setObjectName(dock_id)
        else:
            # auto-increment name if not specified
            dock.setObjectName(f"number_dock_{len(self.number_docks) + 1}")

        self.addDockWidget(Qt.RightDockWidgetArea, dock)
        dock.show()
        self.number_docks.append(dock)

        self.number_docks.append(dock)


    def create_connection_dock(self):
        dock = ConnectionsDock(self)
        self.addDockWidget(Qt.LeftDockWidgetArea, dock)
        dock.show()
        self.number_docks.append(dock)



    def toggle_maximize_restore(self):
        screen = QApplication.screenAt(self.frameGeometry().center())
        if screen:
            screen_geometry = screen.availableGeometry()
        else:
            screen_geometry = QApplication.primaryScreen().availableGeometry()

        toolbar_height = self.toolbar.sizeHint().height()

        if self.is_maximized:
            self.is_maximized = False
            self.maximize_btn.setToolTip("Maximize")
            if os.path.exists("assets/icons/maximize.png"):
                self.maximize_btn.setIcon(QIcon("assets/icons/maximize.png"))
            # ✅ Restore to previous geometry
            self.setGeometry(self.normal_geometry)
        else:
            self.is_maximized = True
            self.maximize_btn.setToolTip("Restore")
            if os.path.exists("assets/icons/restore.png"):
                self.maximize_btn.setIcon(QIcon("assets/icons/restore.png"))
            # ✅ Save normal geometry before maximizing
            self.normal_geometry = self.geometry()
            #self.setGeometry(screen_geometry.x(), screen_geometry.y(), screen_geometry.width(), toolbar_height)
        # ✅ Save the space MainBar will occupy
            self.occupied_rect = QRect(
                screen_geometry.x(),
                screen_geometry.y(),
                screen_geometry.width(),
                toolbar_height
            )
            
            self.setGeometry(self.occupied_rect)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and not self.is_maximized:
            self.drag_position = event.globalPos() - self.pos()
            event.accept()

#makes mainbar draggable
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and not self.is_maximized:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

    def closeEvent(self, event):
        if self.menu_dock:
            self.menu_dock.close()
        for dock in self.number_docks:
            dock.close()
        super().closeEvent(event)




    def show_layout_manager(self):
        """Open or raise the layout manager panel"""
        if hasattr(self, "layout_window") and self.layout_window.isVisible():
            print("LayoutManager already visible, raising...")
            self.layout_window.raise_()
            self.layout_window.activateWindow()
        else:
            print("Creating new LayoutManagerWidget...")
            self.layout_window = LayoutManagerWidget(
                parent=self,
                save_callback=self.save_layout,
                load_callback=self.load_layout
            )
            self.layout_window.show()
            print("LayoutManagerWidget shown.")


    def save_layout(self, as_new=False):
        """
        Save the layout:
        - If as_new=True: prompt for filename (Save As)
        - Else: prompt with default filename.
        """
        print("save_layout called, as_new =", as_new)
        os.makedirs("layouts", exist_ok=True)

        default_path = os.path.join("layouts", "my_layout.layout")

        if as_new:
            filename, _ = QFileDialog.getSaveFileName(
                self,
                "Save Layout As",
                default_path,
                "Layout Files (*.layout)"
            )
        else:
            filename, _ = QFileDialog.getSaveFileName(
                self,
                "Save Layout",
                default_path,
                "Layout Files (*.layout)"
            )

        print("Selected filename:", filename)

        if not filename:
            print("User cancelled save dialog.")
            return

        # ✅ Save which docks are present
        dock_ids = [dock.objectName() for dock in self.number_docks]

        state = {
            "windowState": self.saveState().toHex().data().decode(),
            "geometry": self.saveGeometry().toHex().data().decode(),
            "docks": dock_ids
        }

        try:
            with open(filename, "w") as f:
                json.dump(state, f)
            print(f"Layout saved to {filename}")
            QMessageBox.information(self, "Saved", f"Layout saved to:\n{filename}")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to save layout:\n{e}")



    def load_layout(self, name):
        print("load_layout called with name:", name)
        path = os.path.join("layouts", f"{name}.layout")
        if not os.path.exists(path):
            QMessageBox.warning(self, "Error", f"Layout not found:\n{path}")
            return

        try:
            with open(path, "r") as f:
                data = json.load(f)

            geom_hex = data.get("geometry", "")
            state_hex = data.get("windowState", "")
            dock_ids = data.get("docks", [])

            # ✅ Remove any existing docks
            self._clear_number_docks()

            # ✅ Re-create them with the saved names
            for dock_id in dock_ids:
                self.create_number_dock(dock_id=dock_id)

            if geom_hex:
                self.restoreGeometry(QByteArray.fromHex(geom_hex.encode()))
                print("Geometry restored.")
            if state_hex:
                ok = self.restoreState(QByteArray.fromHex(state_hex.encode()))
                print("State restored:", ok)
                if not ok:
                    QMessageBox.warning(
                        self,
                        "Error",
                        "Failed to restore state—some docks may be missing."
                    )
            QMessageBox.information(self, "Loaded", f"Layout loaded: {name}")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error loading layout:\n{e}")

