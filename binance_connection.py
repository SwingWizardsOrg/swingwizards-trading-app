from PyQt5.QtWidgets import QListWidget, QListWidgetItem

class MyWidget(QListWidget):
    def init(self):
        super().init()

#Add items to the list
        self.addItems([
            "Binance", "CTrader", "Deriv",
            "Metatrader4", "Metatrader5", "SwingWizards Terminal"
        ])

        self.setFixedWidth(200)

#Connect the item click signal to a handler
        self.itemClicked.connect(self.on_item_clicked)

    def on_item_clicked(self, item: QListWidgetItem):
        """Handle when an item is clicked."""
        item_text = item.text()

        if item_text == "Binance":
            self._create_configure_binance_tab()  # Call your Binance function
        elif item_text == "CTrader":
            print("CTrader clicked")  # Replace with your function
        elif item_text == "Deriv":
            print("Deriv clicked")   # Replace with your function
        # ... Add other conditions as needed

    def _create_configure_binance_tab(self):
        """Example function for Binance tab."""
        print("Opening Binance configuration...")