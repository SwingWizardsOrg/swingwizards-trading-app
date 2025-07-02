# gui/menubar_dock.py
from PyQt5.QtWidgets import (
    QDockWidget, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QMessageBox, 
    QScrollArea
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
import os

from gui.chart_dock import ChartDockWidget
from gui.connections import ConnectionsDock
from gui.number_dock import NumberDock


class MenuDock(QDockWidget):
    def __init__(self, main_window, parent=None):
        super().__init__("Menu", parent)
        self.setAllowedAreas(Qt.AllDockWidgetAreas)
        self.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable | QDockWidget.DockWidgetClosable)
        self.setFloating(True)  # <--- Make it float by default
        self.main_window = main_window  # <-- Store QMainWindow reference
        self.number_docks = []          # ✅ add this line to fix the error // AttributeError: 'MenuDock' object has no attribute 'number_docks'

        self.setStyleSheet("""
            QDockWidget {
                border: 2px solid #888;
            }
                           
                QScrollArea {
                    background: transparent;
                }
                QScrollBar:vertical {
                    width: 15px;
                    margin: 0px;
                }
                QScrollBar::handle:vertical {
                    background: #888;
                    min-height: 20px;
                    border-radius: 4px;
                }
                QScrollBar::add-line:vertical,
                QScrollBar::sub-line:vertical {
                    height: 0px;
                }
            QPushButton {
                padding-left: 6px;
                qproperty-iconSize: 18px 18px;
                font-size: 13px;
                background: transparent;
                border: none;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #e8e8e8;
            }
            QLabel {
                color: gray;
            }
        """)

        container = QWidget()
        container.setStyleSheet("background-color: lightblue;") # <--- Adds margin julius
        layout = QVBoxLayout(container)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)

        # layout.addWidget(self.create_section("Charts", [
        #     ("   Market Watch", "flow.png", "Ctrl+M", self.show_market_watch),
        #     ("Data Window", "data_window.png", "Ctrl+D"),
        #     ("Navigator", "navigator.png", self.create_number_dock)
        # ]))


        layout.addWidget(self.create_section("Test", [
            ("   Number Dock", "number.png", "Ctrl+M", self.create_number_dock),
            # ("  Chart Window", "data_window.png", "Ctrl+D", self.create_chart_dock),
            # ("Navigator", "navigator.png", self.create_number_dock)
        ]))


        layout.addWidget(self.create_section("L1 Charts", [
            ("   Simple Chart", "flow.png", "Ctrl+M", self.create_number_dock),
            ("   Footprint Chart", "flow.png", "Ctrl+M", self.create_number_dock),
            ("   TPO Chart", "flow.png", "Ctrl+M", self.create_number_dock),
            ("   Times & Sales Window", "flow.png", "Ctrl+M", self.create_number_dock)
        ]))

        layout.addWidget(self.create_section("L2 Charts", [
            ("   Depth of Market", "flow.png", "Ctrl+M", self.create_number_dock),
            ("   Price Ladder", "flow.png", "Ctrl+M", self.create_number_dock),
            ("   HeatMap", "flow.png", "Ctrl+M", self.create_number_dock),
           
        ]))

        layout.addWidget(self.create_section("FUTURES Charts", [
            ("   Forward Curve", "flow.png", "Ctrl+M", self.create_number_dock),
            ("   **Contango Chart**", "flow.png", "Ctrl+M", self.create_number_dock),
            ("   **Backwardation Chart**", "flow.png", "Ctrl+M", self.create_number_dock),
        ]))


        layout.addWidget(self.create_section("Options Charts", [
            ("   Option Chain", "flow.png", "Ctrl+M", self.create_number_dock),
            ("   Strategy Builder", "flow.png", "Ctrl+M", self.create_number_dock),
            ("   **UOA**", "flow.png", "Ctrl+M", self.create_number_dock),
            ("   Options Flow", "flow.png", "Ctrl+M", self.create_number_dock),
            ("   Options Times & Sales", "flow.png", "Ctrl+M", self.create_number_dock),
            ("   **Exposure Levels**", "flow.png", "Ctrl+M", self.create_number_dock)
        ]))

        layout.addWidget(self.create_section("News Windows", [
            ("   News Deck", "flow.png", "Ctrl+M", self.create_number_dock),
            ("   Symbol News", "flow.png", "Ctrl+M", self.create_number_dock),
            ("   Topic news", "flow.png", "Ctrl+M", self.create_number_dock),
            ("   News Squirk", "flow.png", "Ctrl+M", self.create_number_dock)
        ]))

        layout.addWidget(self.create_section("Messages", [
            ("   Alerts Window", "flow.png", "Ctrl+M", self.create_number_dock),
            ("   Strategy Radar", "flow.png", "Ctrl+M", self.create_number_dock),
            ("   System Logs", "flow.png", "Ctrl+M", self.create_number_dock),
        ]))


        layout.addWidget(self.create_section("Screeners", [
            ("   **Stock Screener**", "flow.png", "Ctrl+M", self.create_number_dock),
            ("   **Options Screener**", "flow.png", "Ctrl+M", self.create_number_dock),
            ("   **Crypto Screener**", "flow.png", "Ctrl+M", self.create_number_dock),

        ]))

        layout.addWidget(self.create_section("AI", [
            ("   Chat Window", "flow.png", "Ctrl+M", self.create_number_dock),
            ("   Research Pipelines", "flow.png", "Ctrl+M", self.create_number_dock),

        ]))

#TREE MAPS
# PERFOMANCE - PERCENTAGE MOVES, GAPS
# order entry tools
# trader tools - watchlist
# journaling tools - trade journal, trade stats, trade analytics
# backtesting tools - backtest, strategy builder, strategy tester
# screener tools - stock screener, options screener, futures screener, crypto screener

#TICKER INFOR --- NEWS, FUNDAMENTALS, 
# ACCOUNT DETAILS - BALANCE, PNL, POSITIONS, ORDERS, TRADES


        layout.addStretch()
        # self.setWidget(container)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(container)
        self.setWidget(scroll_area)


        # Set fixed size for floating window
        self.resize(260, 600)

    def create_section(self, title, items):
        section = QWidget()
        vbox = QVBoxLayout(section)
        vbox.setSpacing(5)
        vbox.setContentsMargins(0, 0, 0, 0)

        vbox.addWidget(self.divider(title))

        for label, icon_name, shortcut, *callback in items:
            hbox = QHBoxLayout()
            hbox.setContentsMargins(0, 0, 0, 0)
            hbox.setSpacing(8)

            btn = QPushButton(label)
            btn.setCursor(Qt.PointingHandCursor)

            icon_path = os.path.join("assets/icons", icon_name)
            if os.path.exists(icon_path):
                btn.setIcon(QIcon(icon_path))
                btn.setIconSize(QSize(18, 18))

            if callback:
                btn.clicked.connect(callback[0])

            shortcut_label = QLabel(shortcut)
            shortcut_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            shortcut_label.setStyleSheet("color: gray;")

            hbox.addWidget(btn, 1)
            hbox.addWidget(shortcut_label, 0)

            vbox.addLayout(hbox)

        return section

    def divider(self, text):
        widget = QWidget()
        hbox = QHBoxLayout(widget)
        hbox.setContentsMargins(0, 0, 0, 0)

        line_left = QFrame()
        line_left.setFrameShape(QFrame.HLine)
        line_left.setFrameShadow(QFrame.Sunken)

        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("color: gray; font-weight: bold;")

        line_right = QFrame()
        line_right.setFrameShape(QFrame.HLine)
        line_right.setFrameShadow(QFrame.Sunken)

        hbox.addWidget(line_left)
        hbox.addWidget(label)
        hbox.addWidget(line_right)

        return widget

    # def show_market_watch(self):
    #     QMessageBox.information(self, "Market Watch", "3")

    # def create_connection_dock(self):
    #     dock = ConnectionsDock(self)
    #     self.addDockWidget(Qt.LeftDockWidgetArea, dock)
    #     dock.show()
    #     self.number_docks.append(dock)
    
    def create_number_dock(self):
        dock = NumberDock(self.main_window)  # pass main_window as parent
        self.main_window.addDockWidget(Qt.RightDockWidgetArea, dock)
        dock.show()
        self.number_docks.append(dock)

    def create_chart_dock(self):
        dock = ChartDockWidget(self.main_window)  # pass main_window as parent
        self.main_window.addDockWidget(Qt.RightDockWidgetArea, dock)
        dock.show()
        self.chart_docks.append(dock)