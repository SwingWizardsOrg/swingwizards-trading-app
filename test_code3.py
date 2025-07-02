import sys
import os
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from binance.client import Client
from PyQt5.QtWidgets import (QApplication, QMainWindow, QToolBar, QAction, QToolButton, QSizePolicy, QWidget,
                             QDockWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLabel, QLineEdit, QListWidget,
                             QListWidgetItem, QComboBox)  # Removed QWebEngineView from here
from PyQt5.QtWebEngineWidgets import QWebEngineView  # Already correctly imported here
from PyQt5.QtCore import Qt, QPoint, QUrl
from PyQt5.QtGui import QIcon

class MovableDockWidget(QDockWidget):
    def __init__(self, title, parent=None):
        super().__init__(title, parent)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.drag_position = QPoint()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.pos()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

class ChartDockWidget(MovableDockWidget):
    def __init__(self, title, parent=None):
        super().__init__(title, parent)
        self.setFloating(True)
        self.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable | QDockWidget.DockWidgetClosable)
        self.setAllowedAreas(Qt.AllDockWidgetAreas)

        # Chart-related attributes
        self.df = None
        self.fig = None
        self.active_indicators = []
        self.current_symbol = "ETHBTC"
        self.available_symbols = []
        self.current_timeframe = Client.KLINE_INTERVAL_15MINUTE
        self.history_days = 3
        self.available_indicators = ["RSI", "Stochastics"]
        self.indicator_counter = 0
        self.fetch_available_symbols()

        # Create chart content
        self.setup_chart_content()

    def setup_chart_content(self):
        chart_widget = QWidget()
        chart_layout = QVBoxLayout(chart_widget)
        chart_layout.setContentsMargins(3, 1, 3, 3)
        chart_layout.setSpacing(0)

        # Search ribbon
        search_ribbon = QWidget()
        search_ribbon.setStyleSheet("background-color: #222; border-bottom: 1px solid #444;")
        search_ribbon.setFixedHeight(32)
        search_layout = QHBoxLayout(search_ribbon)
        search_layout.setContentsMargins(3, 1, 3, 1)
        search_layout.setSpacing(2)

        # Symbol search
        self.symbol_search = QLineEdit()
        self.symbol_search.setPlaceholderText("Search Symbol")
        self.symbol_search.setFixedWidth(120)
        self.symbol_search.setFixedHeight(30)
        self.symbol_search.setStyleSheet("font-size: 14px;color: white;border: 4px solid #555;")
        self.symbol_search.textChanged.connect(self.update_symbol_grid)
        self.symbol_search.returnPressed.connect(self.search_symbol)
        search_layout.addWidget(self.symbol_search)

        # Timeframe selector
        self.timeframe_combo = QComboBox()
        self.timeframe_combo.addItems(["5 min", "15 min", "1 hour", "4 hour"])
        self.timeframe_combo.setCurrentText("15 min")
        self.timeframe_combo.setFixedWidth(80)
        self.timeframe_combo.setFixedHeight(30)
        self.timeframe_combo.setStyleSheet("font-size: 14px;color: white;border: 4px solid #555;")
        self.timeframe_combo.currentTextChanged.connect(self.change_timeframe)
        search_layout.addWidget(self.timeframe_combo)

        # History days selector
        self.days_combo = QComboBox()
        self.days_combo.addItems(["1 day", "3 days", "7 days", "14 days"])
        self.days_combo.setCurrentText("3 days")
        self.days_combo.setFixedWidth(80)
        self.days_combo.setFixedHeight(30)
        self.days_combo.setStyleSheet("font-size: 14px;color: white;border: 4px solid #555;")
        self.days_combo.currentTextChanged.connect(self.change_days)
        search_layout.addWidget(self.days_combo)

        # Indicator search
        self.indicator_search = QLineEdit()
        self.indicator_search.setPlaceholderText("Search Indicator")
        self.indicator_search.setFixedWidth(120)
        self.indicator_search.setFixedHeight(30)
        self.indicator_search.setStyleSheet("font-size: 14px;color: white;border: 4px solid #555;")
        self.indicator_search.textChanged.connect(self.update_indicator_grid)
        self.indicator_search.returnPressed.connect(self.search_indicator)
        search_layout.addWidget(self.indicator_search)

        search_layout.addStretch()
        chart_layout.addWidget(search_ribbon)

        # Toolbar
        toolbar = QToolBar("Dock Toolbar")
        toolbar.setFixedHeight(32)
        toolbar.setStyleSheet("background-color: #222; border-bottom: 1px solid #444; spacing: 2px;")

        reset_action = QAction("Reset View", self)
        reset_action.triggered.connect(self.reset_view)
        toolbar.addAction(reset_action)

        toolbar.addSeparator()

        refresh_action = QAction("Refresh Data", self)
        refresh_action.triggered.connect(self.refresh_chart)
        toolbar.addAction(refresh_action)

        chart_layout.addWidget(toolbar)

        # Chart
        self.browser = QWebEngineView()
        chart_layout.addWidget(self.browser)

        # Symbol suggestion grid
        self.symbol_grid = QListWidget(chart_widget)
        self.symbol_grid.setFixedWidth(120)
        self.symbol_grid.setFixedHeight(180)
        self.symbol_grid.setStyleSheet("""
            QListWidget {
                background-color: #333;
                color: white;
                border: 1px solid #555;
                border-radius: 1px;
            }
            QListWidget::item {
                padding: 2px;
                font-size: 16px;
            }
            QListWidget::item:selected {
                background-color: #555;
            }
        """)
        self.symbol_grid.setFlow(QListWidget.LeftToRight)
        self.symbol_grid.setWrapping(True)
        self.symbol_grid.setResizeMode(QListWidget.Adjust)
        self.symbol_grid.itemClicked.connect(self.on_symbol_selected)
        self.symbol_grid.hide()

        # Indicator suggestion grid
        self.indicator_grid = QListWidget(chart_widget)
        self.indicator_grid.setFixedWidth(120)
        self.indicator_grid.setFixedHeight(60)
        self.indicator_grid.setStyleSheet("""
            QListWidget {
                background-color: #333;
                color: white;
                border: 1px solid #555;
                border-radius: 1px;
            }
            QListWidget::item {
                padding: 2px;
                font-size: 16px;
            }
            QListWidget::item:selected {
                background-color: #555;
            }
        """)
        self.indicator_grid.setFlow(QListWidget.LeftToRight)
        self.indicator_grid.setWrapping(True)
        self.indicator_grid.setResizeMode(QListWidget.Adjust)
        self.indicator_grid.itemClicked.connect(self.on_indicator_selected)
        self.indicator_grid.hide()

        self.setWidget(chart_widget)
        self.setFixedSize(800, 600)
        self.load_chart()

    def fetch_available_symbols(self):
        try:
            client = Client()
            exchange_info = client.get_exchange_info()
            self.available_symbols = [symbol['symbol'] for symbol in exchange_info['symbols'] if symbol['status'] == 'TRADING']
        except Exception as e:
            print(f"Error fetching symbols: {e}")
            self.available_symbols = ["ETHBTC", "BTCUSDT", "ETHUSDT"]

    def update_symbol_grid(self, text):
        self.symbol_grid.clear()
        if not text:
            self.symbol_grid.hide()
            return
        text = text.upper()
        matching_symbols = [symbol for symbol in self.available_symbols if text in symbol]
        for symbol in matching_symbols[:10]:
            item = QListWidgetItem(symbol)
            item.setTextAlignment(Qt.AlignCenter)
            self.symbol_grid.addItem(item)
        if matching_symbols:
            search_pos = self.symbol_search.mapTo(self.symbol_grid.parent(), QPoint(0, 0))
            self.symbol_grid.setGeometry(search_pos.x(), search_pos.y() + self.symbol_search.height(), 120, 60)
            self.symbol_grid.show()
            self.symbol_grid.raise_()
        else:
            self.symbol_grid.hide()

    def update_indicator_grid(self, text):
        self.indicator_grid.clear()
        if not text:
            self.indicator_grid.hide()
            return
        text = text.upper()
        matching_indicators = [indicator for indicator in self.available_indicators if text in indicator.upper()]
        for indicator in matching_indicators[:5]:
            item = QListWidgetItem(indicator)
            item.setTextAlignment(Qt.AlignCenter)
            self.indicator_grid.addItem(item)
        if matching_indicators:
            search_pos = self.indicator_search.mapTo(self.indicator_grid.parent(), QPoint(0, 0))
            self.indicator_grid.setGeometry(search_pos.x(), search_pos.y() + self.indicator_search.height(), 120, 60)
            self.indicator_grid.show()
            self.indicator_grid.raise_()
        else:
            self.indicator_grid.hide()

    def on_symbol_selected(self, item):
        selected_symbol = item.text()
        self.symbol_search.blockSignals(True)
        self.symbol_search.setText(selected_symbol)
        self.symbol_search.blockSignals(False)
        self.symbol_grid.hide()
        self.search_symbol()

    def on_indicator_selected(self, item):
        selected_indicator = item.text()
        self.indicator_search.blockSignals(True)
        self.indicator_search.setText(selected_indicator)
        self.indicator_search.blockSignals(False)
        self.indicator_grid.hide()
        self.search_indicator()

    def search_symbol(self):
        symbol = self.symbol_search.text().upper()
        if symbol in self.available_symbols:
            self.current_symbol = symbol
            self.df = None
            self.load_chart()
        else:
            print(f"Symbol {symbol} not found.")

    def search_indicator(self):
        indicator = self.indicator_search.text()
        if indicator in self.available_indicators:
            self.add_indicator(indicator)
            self.indicator_search.clear()
        else:
            print(f"Indicator {indicator} not found.")

    def add_indicator(self, indicator_type):
        self.indicator_counter += 1
        self.active_indicators.append({'type': indicator_type, 'id': self.indicator_counter})
        self.load_chart()

    def remove_indicator(self, indicator_id):
        self.active_indicators = [ind for ind in self.active_indicators if ind['id'] != indicator_id]
        self.load_chart()

    def reset_view(self):
        self.browser.page().runJavaScript("Plotly.relayout('plotly-div', {dragmode: 'pan'});")

    def refresh_chart(self):
        self.df = None
        self.load_chart()

    def change_timeframe(self, timeframe_text):
        interval_map = {
            "5 min": Client.KLINE_INTERVAL_5MINUTE,
            "15 min": Client.KLINE_INTERVAL_15MINUTE,
            "1 hour": Client.KLINE_INTERVAL_1HOUR,
            "4 hour": Client.KLINE_INTERVAL_4HOUR
        }
        self.current_timeframe = interval_map[timeframe_text]
        self.df = None
        self.load_chart()

    def change_days(self, days_text):
        self.history_days = int(days_text.split()[0])
        self.df = None
        self.load_chart()

    def fetch_data(self):
        if self.df is not None:
            return

        try:
            client = Client()
            timeframe_minutes = {
                Client.KLINE_INTERVAL_5MINUTE: 5,
                Client.KLINE_INTERVAL_15MINUTE: 15,
                Client.KLINE_INTERVAL_1HOUR: 60,
                Client.KLINE_INTERVAL_4HOUR: 240
            }
            minutes_per_day = 24 * 60
            limit = int(self.history_days * minutes_per_day / timeframe_minutes[self.current_timeframe])
            limit = min(limit, 1500)

            klines = client.futures_klines(
                symbol=self.current_symbol,
                interval=self.current_timeframe,
                limit=limit
            )
        except Exception as e:
            print(f"Error fetching data: {e}")
            return

        df = pd.DataFrame(klines, columns=[
            'open_time', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_asset_volume', 'num_trades',
            'taker_buy_base', 'taker_buy_quote', 'ignore'
        ])
        df['open_time'] = pd.to_datetime(df['open_time'], unit='ms', utc=True).dt.tz_localize(None)
        df[['open', 'high', 'low', 'close', 'volume']] = df[['open', 'high', 'low', 'close', 'volume']].astype(float)
        self.df = df

    def load_chart(self):
        self.fetch_data()
        if self.df is None:
            return

        num_indicators = len(self.active_indicators)
        num_rows = 1 + num_indicators

        row_heights = [0.7] + [0.3 / num_indicators if num_indicators > 0 else 0] * num_indicators

        self.fig = make_subplots(
            rows=num_rows, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.05,
            row_heights=row_heights,
            subplot_titles=[""] * num_rows
        )

        self.fig.add_trace(go.Candlestick(
            x=self.df['open_time'],
            open=self.df['open'],
            high=self.df['high'],
            low=self.df['low'],
            close=self.df['close'],
            increasing_line_color='#00CCFF',
            decreasing_line_color='#FF3333',
            name='Price'
        ), row=1, col=1)

        if num_indicators > 0:
            self.fig.add_hline(
                y=self.df['close'].min(),
                line_dash="dash",
                line_color="rgba(255,255,255,0.5)",
                row=2, col=1,
                annotation_text="",
                annotation_position="top"
            )

        for idx, indicator in enumerate(self.active_indicators, start=2):
            ind_type = indicator['type']
            if ind_type == "RSI":
                close = self.df['close']
                delta = close.diff()
                up = delta.clip(lower=0)
                down = -1 * delta.clip(upper=0)
                avg_gain = up.rolling(14).mean()
                avg_loss = down.rolling(14).mean()
                rs = avg_gain / avg_loss
                rsi = 100 - (100 / (1 + rs))
                self.fig.add_trace(go.Scatter(
                    x=self.df['open_time'],
                    y=rsi,
                    name="RSI",
                    line=dict(color='#FF9900')
                ), row=idx, col=1)
                self.fig.update_yaxes(row=idx, col=1, range=[0, 100], side='left')
            elif ind_type == "Stochastics":
                low_min = self.df['low'].rolling(14).min()
                high_max = self.df['high'].rolling(14).max()
                stoch_k = 100 * ((self.df['close'] - low_min) / (high_max - low_min))
                stoch_d = stoch_k.rolling(3).mean()
                self.fig.add_trace(go.Scatter(
                    x=self.df['open_time'],
                    y=stoch_k,
                    name="%K",
                    line=dict(color='#00CCFF')
                ), row=idx, col=1)
                self.fig.add_trace(go.Scatter(
                    x=self.df['open_time'],
                    y=stoch_d,
                    name="%D",
                    line=dict(color='#FF3399')
                ), row=idx, col=1)
                self.fig.update_yaxes(row=idx, col=1, range=[0, 100], side='left')

            self.fig.add_annotation(
                xref=f"x{idx}",
                yref=f"y{idx}",
                x=self.df['open_time'].max(),
                y=100 if ind_type in ["RSI", "Stochastics"] else 0,
                text="❌",
                showarrow=False,
                font=dict(size=12, color="red"),
                align="center",
                xanchor="right",
                yanchor="top",
                clicktoshow="onout",
                name=f"delete_{indicator['id']}",
                hovertext=f"Remove {ind_type}",
                ax=0,
                ay=0
            )

        self.update_browser()

    def update_browser(self):
        if self.fig is None:
            return

        import time
        unique_id = f"plotly-div-{int(time.time())}"
        num_rows = 1 + len(self.active_indicators)

        self.fig.update_layout(
            template="plotly_dark",
            height=500,
            showlegend=False,
            margin=dict(l=30, r=30, t=60, b=30),
            xaxis_rangeslider_visible=False,
            dragmode="pan",
            hovermode="closest",
            plot_bgcolor='rgba(0,0,0,0.9)',
            paper_bgcolor='rgba(0,0,0,0.9)',
            annotations=[
                dict(
                    name=ann.name,
                    x=ann.x,
                    y=ann.y,
                    xref=ann.xref,
                    yref=ann.yref,
                    text=ann.text,
                    showarrow=ann.showarrow,
                    font=ann.font,
                    align=ann.align,
                    xanchor=ann.xanchor,
                    yanchor=ann.yanchor,
                    hovertext=ann.hovertext,
                    clicktoshow=ann.clicktoshow
                ) for ann in self.fig.layout.annotations
            ]
        )

        for row in range(1, num_rows + 1):
            self.fig.update_xaxes(
                row=row, col=1,
                showgrid=False,
                zeroline=False,
                showline=True,
                linecolor='rgba(255,255,255,0.2)',
                ticks="outside",
                title_text=""
            )
            self.fig.update_yaxes(
                row=row, col=1,
                title_text="",
                showgrid=True,
                gridcolor="rgba(255,255,255,0.1)",
                zeroline=False,
                showline=True,
                linecolor='rgba(255,255,255,0.2)',
                ticks="outside",
                side='right'
            )

        html = self.fig.to_html(include_plotlyjs='cdn', config={
            'scrollZoom': True,
            'displayModeBar': True,
            'responsive': True,
            'modeBarButtonsToRemove': ['zoomIn', 'zoomOut', 'autoScale', 'lasso2d', 'select']
        })

        custom_js = """
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                var plotDiv = document.getElementsByClassName('plotly-graph-div')[0];
                plotDiv.on('plotly_clickannotation', function(event, data) {
                    if (data.annotation.name.startsWith('delete_')) {
                        var indicatorId = data.annotation.name.split('_')[1];
                        fetch('/delete_indicator/' + indicatorId, {method: 'POST'})
                            .then(response => response.json())
                            .then(data => {
                                if (data.success) {
                                    location.reload();
                                }
                            });
                    }
                });
            });
        </script>
        """
        html = html.replace('</body>', custom_js + '</body>')

        self.browser.setHtml("", QUrl.fromLocalFile(""))
        self.browser.setHtml(html, QUrl.fromLocalFile(""))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle("Flat Design Toolbar Example")
        self.is_maximized = False
        self.drag_position = QPoint()
        self.chart_docks = []  # List to track chart dock widgets
        self.chart_counter = 0  # Counter for unique chart titles

        # Create a central widget (required for docking to work properly)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create a toolbar
        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        # Add actions (buttons) with icons to the toolbar
        actions = [
            ("Menu", "icons/menu.png", self.toggle_menu_dock),
            ("Home", "icons/home.png", None),
            ("Tools", "icons/tools.png", None),
            ("Code", "icons/code.png", None),
            ("Monitor", "icons/monitor.png", None),
            ("Flow", "icons/flow.png", None),
            ("Settings", "icons/settings.png", None),
            ("User", "icons/user.png", None),
        ]

        for name, icon_path, callback in actions:
            action = QAction(QIcon(icon_path), name, self)
            action.setToolTip(name)
            if callback:
                action.triggered.connect(callback)
            toolbar.addAction(action)

        # Add a spacer to push buttons to the left
        toolbar.addSeparator()
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        spacer.setMinimumWidth(100)
        toolbar.addWidget(spacer)

        # Add custom minimize button
        minimize_btn = QToolButton()
        minimize_btn.setIcon(QIcon("icons/minimize.png"))
        minimize_btn.setToolTip("Minimize")
        minimize_btn.clicked.connect(self.minimize_window)
        toolbar.addWidget(minimize_btn)

        # Add custom maximize/restore button
        self.maximize_btn = QToolButton()
        self.maximize_btn.setIcon(QIcon("icons/maximize.png"))
        self.maximize_btn.setToolTip("Maximize")
        self.maximize_btn.clicked.connect(self.toggle_maximize_restore)
        toolbar.addWidget(self.maximize_btn)

        # Add custom close button
        close_btn = QToolButton()
        close_btn.setIcon(QIcon("icons/close.png"))
        close_btn.setToolTip("Close")
        close_btn.clicked.connect(self.close)
        toolbar.addWidget(close_btn)

        # Create the menu dock widget
        self.menu_dock = MovableDockWidget("Menu", self)
        self.menu_dock.setFloating(True)
        self.menu_dock.setVisible(False)
        self.menu_dock.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable | QDockWidget.DockWidgetClosable)
        self.menu_dock.setAllowedAreas(Qt.AllDockWidgetAreas)

        # Create a widget to hold the menu dock's contents
        menu_content = QWidget()
        menu_layout = QVBoxLayout(menu_content)

        # Add buttons to the menu dock widget
        chart_btn = QPushButton("Chart")
        chart_btn.clicked.connect(self.create_chart_dock)
        chart_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                padding: 10px;
                text-align: left;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
                border-radius: 3px;
            }
            QPushButton:pressed {
                background-color: #d0d0d0;
            }
        """)
        menu_layout.addWidget(chart_btn)

        for label in ["Option 2", "Option 3"]:
            btn = QPushButton(label)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: none;
                    padding: 10px;
                    text-align: left;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #e0e0e0;
                    border-radius: 3px;
                }
                QPushButton:pressed {
                    background-color: #d0d0d0;
                }
            """)
            menu_layout.addWidget(btn)

        self.menu_dock.setWidget(menu_content)
        self.menu_dock.setFixedSize(200, 150)

        # Apply flat design stylesheet
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QToolBar {
                background-color: #f0f0f0;
                border: none;
                padding: 5px;
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
            QDockWidget {
                background-color: #f0f0f0;
                border: none;
            }
            QDockWidget::title {
                background: #f0f0f0;
                padding: 5px;
            }
        """)

        # Adjust window size to fit only the toolbar
        toolbar_height = toolbar.sizeHint().height()
        self.setFixedHeight(toolbar_height)
        self.setGeometry(100, 100, 800, toolbar_height)

    def create_chart_dock(self):
        self.chart_counter += 1
        chart_dock = ChartDockWidget(f"Chart {self.chart_counter}", self)
        chart_dock.setVisible(True)
        self.chart_docks.append(chart_dock)

        # Position the new chart dock widget below the toolbar
        toolbar_height = self.findChild(QToolBar).sizeHint().height()
        dock_pos = self.pos() + QPoint(10 + (self.chart_counter * 20), toolbar_height + 5 + (self.chart_counter * 20))
        chart_dock.move(dock_pos)

        # Add the chart dock widget to the main window
        self.addDockWidget(Qt.RightDockWidgetArea, chart_dock)

    def toggle_menu_dock(self):
        print("Toggling menu dock widget visibility")
        if self.menu_dock.isVisible():
            self.menu_dock.setVisible(False)
        else:
            toolbar_height = self.findChild(QToolBar).sizeHint().height()
            dock_pos = self.pos() + QPoint(10, toolbar_height + 5)
            self.menu_dock.move(dock_pos)
            self.menu_dock.setVisible(True)
            print(f"Menu dock widget positioned at: {dock_pos}")

    def minimize_window(self):
        self.showMinimized()

    def toggle_maximize_restore(self):
        if self.is_maximized:
            self.showNormal()
            self.is_maximized = False
            self.maximize_btn.setIcon(QIcon("icons/maximize.png"))
            self.maximize_btn.setToolTip("Maximize")
            toolbar_height = self.findChild(QToolBar).sizeHint().height()
            self.setFixedHeight(toolbar_height)
        else:
            self.showMaximized()
            self.is_maximized = True
            self.maximize_btn.setIcon(QIcon("icons/restore.png"))
            self.maximize_btn.setToolTip("Restore")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and not self.is_maximized:
            self.drag_position = event.globalPos() - self.pos()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and not self.is_maximized:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())