clientid


clientsecret
access token



Great—let’s find something close.

You’re describing:
**A rectangle with an arrow pointing northwest** (↖).

While **Unicode does not** have a single character showing *a rectangle containing an arrow*, it *does* have:

✅ **Standalone northwest arrow symbols:**

* **↖** U+2196 *NORTH WEST ARROW*
  ↖
* **⬉** U+2B09 *NORTH WEST BLACK ARROW*
  ⬉

✅ **Enclosed arrows:**
Unicode *does not* define arrows inside boxes specifically, but you can approximate a *boxed arrow* by using emoji-style squares and arrows side by side:

```
⬜️↖
```

⬜️ = WHITE LARGE SQUARE
↖ = NORTH WEST ARROW

✅ **Diagonal Arrow in a Square Emoji:**
There isn’t a standard emoji combining both.

✅ **Similar Unicode pictograms:**
You might also consider the **RETURN SYMBOL**:
⏎ U+23CE
…but that points down-left and isn’t exactly what you described.

---

**Conclusion:**
✅ **Closest Unicode character to your description:**
**↖** U+2196 NORTH WEST ARROW

If you really need a *rectangle containing the arrow as a single glyph*, you’d have to:

* Make an **SVG icon** or
* Use a custom icon font.

Want help creating an SVG or exploring icon fonts?







this works weeh manually switched

from PyQt5.QtWidgets import (
    QDockWidget, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QListWidget, QTabWidget, QTableWidget, QTableWidgetItem,
    QFrame, QSplitter, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QFormLayout, QHBoxLayout

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

        # list_widget = QListWidget()
        # list_widget.addItems([
        #     "Binance", "CTrader", "Deriv",
        #     "Metatrader4", "Metatrader5", "SwingWizards Terminal"
        # ])
        # list_widget.setFixedWidth(200)
        # layout.addWidget(list_widget)

        # Container for label + list
        list_container = QWidget()
        list_layout = QVBoxLayout(list_container)
        list_layout.setContentsMargins(0, 0, 0, 0)
        list_container.setFixedWidth(240)

        # Label
        list_label = QLabel("AVAILABLE CONNECTIONS")
        list_label.setAlignment(Qt.AlignCenter)
        list_label.setStyleSheet("font-weight: bold; font-size: 14px; padding: 6px;")

        # List
        list_widget = QListWidget()
        list_widget.addItems([
            "Binance", "CTrader", "Deriv",
            "Metatrader4", "Metatrader5", "SwingWizards Terminal"
        ])
        list_widget.setFixedWidth(200)

        # Add to layout
        list_layout.addWidget(list_label)
        list_layout.addWidget(list_widget)

        # Add to main layout
        layout.addWidget(list_container)


        tabs = QTabWidget()
        tabs.addTab(self._create_configure_alpaca_tab(), "Configure a Connection")
        tabs.addTab(self._create_tab("Configured Connections Area"), "Configured Connections")
        tabs.addTab(self._create_tab("Connected Connections Area"), "Connnected Connections")
        layout.addWidget(tabs)

        self.setWidget(container)

    def _create_tab(self, tab_name: str):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(0, 0, 0, 0)

        # Main vertical splitter
        splitter = QSplitter(Qt.Vertical)

        # --- Top: Table Widget ---
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

        # --- Bottom: Info panel with horizontal splitter ---
        bottom_info = QWidget()
        bottom_layout = QVBoxLayout(bottom_info)
        bottom_layout.setContentsMargins(10, 5, 10, 5)

        # Optional: horizontal line separator
        top_line = QFrame()
        top_line.setFrameShape(QFrame.HLine)
        top_line.setFrameShadow(QFrame.Sunken)
        bottom_layout.addWidget(top_line)

        inner_splitter = QSplitter(Qt.Horizontal)

        # Side 1: LATENCY + PING
        side1 = QWidget()
        s1_layout = QVBoxLayout(side1)
        s1_layout.setContentsMargins(10, 5, 10, 5)
        s1_layout.addWidget(QLabel("LATENCY"))
        s1_layout.addWidget(QLabel("PING"))

        # Side 2: SYMBOLS + ENDPOINTS
        side2 = QWidget()
        s2_layout = QVBoxLayout(side2)
        s2_layout.setContentsMargins(10, 5, 10, 5)
        s2_layout.addWidget(QLabel("SYMBOLS"))
        s2_layout.addWidget(QLabel("ENDPOINTS"))

        # Add both sides to the horizontal splitter
        inner_splitter.addWidget(side1)
        inner_splitter.addWidget(side2)
        inner_splitter.setSizes([150, 150])

        bottom_layout.addWidget(inner_splitter)

        # --- Final assembly ---
        splitter.addWidget(table)
        splitter.addWidget(bottom_info)
        splitter.setSizes([400, 120])  # Optional: set initial heights

        layout.addWidget(splitter)
        return tab

    def _create_configure_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(10, 10, 10, 10)

        # Create an instance of the login form
        login_form = QWidget()
        form_layout = QFormLayout()

        secret_label = QLabel("Secret key")
        secret_input = QLineEdit()

        api_label = QLabel("API key")
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


    def _create_configure_binance_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(10, 10, 10, 10)

        # Create an instance of the login form
        login_form = QWidget()
        form_layout = QFormLayout()

        secret_label = QLabel("binance")
        secret_input = QLineEdit()

        api_label = QLabel("binance")
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
    
    def _create_configure_alpaca_tab(self):
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

