from PyQt5.QtWidgets import (
    QDockWidget, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QListWidget, QTabWidget, QTableWidget, QTableWidgetItem,
    QFrame, QSplitter, QLineEdit, QPushButton, QFormLayout
)
from PyQt5.QtCore import Qt


class ConnectionsDock(QDockWidget):
    def __init__(self, parent=None):
        super().__init__("Connections", parent)
        self.setAllowedAreas(Qt.AllDockWidgetAreas)
        self.setFloating(True)

        self.setStyleSheet("""
            QDockWidget {
                border: 2px solid #888;
            }
            QListWidget {
                background-color: #333;
                color: lightgray;
                border: none;
            }
            QListWidget::item {
                padding: 8px;
            }
            QListWidget::item:selected {
                background-color: #555;
                color: white;
            }
            QTabBar::tab {
                background: #ccc;
                padding: 10px;
                min-width: 150px;
            }
            QTabBar::tab:selected {
                background: #eee;
                font-weight: bold;
            }
            QLabel {
                color: #666;
                font-size: 16px;
            }
        """)

        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)

        # List container
        list_container = QWidget()
        list_layout = QVBoxLayout(list_container)
        list_layout.setContentsMargins(0, 0, 0, 0)
        list_container.setFixedWidth(240)

        list_label = QLabel("AVAILABLE CONNECTIONS")
        list_label.setAlignment(Qt.AlignCenter)
        list_label.setStyleSheet("font-weight: bold; font-size: 14px; padding: 6px;")

        list_widget = QListWidget()
        list_widget.addItems([
            "Binance", "Alpaca", "CTrader", "Deriv",
            "Metatrader4", "Metatrader5", "SwingWizards Terminal"
        ])
        list_widget.setFixedWidth(200)
        list_widget.currentTextChanged.connect(self.on_connection_selected)

        list_layout.addWidget(list_label)
        list_layout.addWidget(list_widget)
        layout.addWidget(list_container)

        # Tabs
        self.tabs = QTabWidget()

        # Configure tab container (will be dynamically updated)
        self.configure_tab = QWidget()
        self.configure_tab_layout = QVBoxLayout(self.configure_tab)
        self.configure_tab_layout.setContentsMargins(0, 0, 0, 0)
        # Load initial content
        self.configure_tab_layout.addWidget(self._create_configure_tab())

        # Add tabs
        self.tabs.addTab(self.configure_tab, "Configure a Connection")
        self.tabs.addTab(self._create_tab("Configured Connections Area"), "Configured Connections")
        self.tabs.addTab(self._create_tab("Connected Connections Area"), "Connected Connections")

        layout.addWidget(self.tabs)

        self.setWidget(container)

    def _create_tab(self, tab_name: str):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(0, 0, 0, 0)

        splitter = QSplitter(Qt.Vertical)

        table = QTableWidget(9, 4)
        table.setHorizontalHeaderLabels(["headline", "link", "company", "ticker"])
        dummy_data = [
            ("Calls Them 'Speculative'", "m-Speculative-50215428/", "UNITD SPIRITS LIMITED", "UNITDSPIR"),
            ("posal from Long Harbour", "Long-Harbour-50215427/", "THE PRS REIT PLC", "PRSR"),
            ("lakes Move on PRS REIT", "-on-PRS-REIT-50215401/", "THE PRS REIT PLC", "PRSR"),
            ("Banks for 710 Billion Sale", "10-Billion-Sale-50214696/", "JET MANAGEMENT LTD.", "BAML"),
            ("nina Häagen-Dazs Stores", "n-Dazs-Stores-50214501/", "GENERAL MILLS, INC.", "GIS"),
            ("nvestment Bank Avendus", "ank-Avendus-50214050/", "FINANCIAL GROUP, INC.", "8411.T"),
            ("r Buying Some BP Assets", "me-BP-Assets-50214034/", "BP PLC", "BP"),
            ("ditya Birla Capital Limited", "apital-Limited-50213786/", "BIRLA CAPITAL LIMITED", "ABCAPITAL"),
            ("ger With Huafu Securities", "afu-Securities-50212795/", "J SECURITIES CO.,LTD.", "601377")
        ]
        for row, (headline, link, company, ticker) in enumerate(dummy_data):
            table.setItem(row, 0, QTableWidgetItem(headline))
            table.setItem(row, 1, QTableWidgetItem(link))
            table.setItem(row, 2, QTableWidgetItem(company))
            table.setItem(row, 3, QTableWidgetItem(ticker))

        bottom_info = QWidget()
        bottom_layout = QVBoxLayout(bottom_info)
        bottom_layout.setContentsMargins(10, 5, 10, 5)

        top_line = QFrame()
        top_line.setFrameShape(QFrame.HLine)
        top_line.setFrameShadow(QFrame.Sunken)
        bottom_layout.addWidget(top_line)

        inner_splitter = QSplitter(Qt.Horizontal)

        side1 = QWidget()
        s1_layout = QVBoxLayout(side1)
        s1_layout.setContentsMargins(10, 5, 10, 5)
        s1_layout.addWidget(QLabel("LATENCY"))
        s1_layout.addWidget(QLabel("PING"))

        side2 = QWidget()
        s2_layout = QVBoxLayout(side2)
        s2_layout.setContentsMargins(10, 5, 10, 5)
        s2_layout.addWidget(QLabel("SYMBOLS"))
        s2_layout.addWidget(QLabel("ENDPOINTS"))

        inner_splitter.addWidget(side1)
        inner_splitter.addWidget(side2)
        inner_splitter.setSizes([150, 150])

        bottom_layout.addWidget(inner_splitter)

        splitter.addWidget(table)
        splitter.addWidget(bottom_info)
        splitter.setSizes([400, 120])

        layout.addWidget(splitter)
        return tab

    def on_connection_selected(self, name: str):
        # Clear old widgets
        while self.configure_tab_layout.count():
            item = self.configure_tab_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # Choose which configuration widget to show
        if name == "Binance":
            new_widget = self._create_configure_binance_tab()
        elif name == "Alpaca":
            new_widget = self._create_configure_alpaca_tab()
        elif name == "Deriv":
            new_widget = self._create_configure_deriv_tab()
        else:
            new_widget = self._create_configure_tab()

        self.configure_tab_layout.addWidget(new_widget)
        self.tabs.setCurrentWidget(self.configure_tab)

    def _create_configure_tab(self):
        return self._create_generic_config_tab("Generic Connection")

    def _create_configure_binance_tab(self):
        return self._create_generic_config_tab("Binance Connection")

    def _create_configure_alpaca_tab(self):
        return self._create_generic_config_tab("Alpaca Connection")

    def _create_generic_config_tab(self, title):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(10, 10, 10, 10)

        form = QWidget()
        form_layout = QFormLayout()

        secret_label = QLabel(f"{title} - Secret Key")
        secret_input = QLineEdit()

        api_label = QLabel(f"{title} - API Key")
        api_input = QLineEdit()

        username_label = QLabel("Username")
        username_input = QLineEdit()

        connect_btn = QPushButton("CONNECT")
        connect_btn.setFixedWidth(80)

        form_layout.addRow(secret_label, secret_input)
        form_layout.addRow(api_label, api_input)
        form_layout.addRow(username_label, username_input)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(connect_btn)
        btn_layout.addStretch()

        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addSpacing(10)
        main_layout.addLayout(btn_layout)

        form.setLayout(main_layout)
        layout.addWidget(form)
        return tab
    
    def _create_configure_deriv_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(10, 10, 10, 10)

        # Create an instance of the login form
        login_form = QWidget()
        form_layout = QFormLayout()

        secret_label = QLabel("alpaca")
        secret_input = QLineEdit()

        api_label = QLabel("alpaca")
        api_input = QLineEdit()

        username_label = QLabel("Username")
        username_input = QLineEdit()

        connect_btn = QPushButton("CONNECT")
        connect_btn.setFixedWidth(80)

        # Form layout
        form_layout.addRow(secret_label, secret_input)
        form_layout.addRow(api_label, api_input)
        form_layout.addRow(username_label, username_input)

        # Button centered horizontally
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(connect_btn)
        btn_layout.addStretch()

        # Combine form and button into a vertical layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addSpacing(10)
        main_layout.addLayout(btn_layout)

        login_form.setLayout(main_layout)

        # Add the login form widget into the tab layout
        layout.addWidget(login_form)

        return tab