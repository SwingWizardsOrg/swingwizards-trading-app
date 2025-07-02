import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QCheckBox, QFrame, QMessageBox, QScrollArea, QSpacerItem,
    QSizePolicy
)
from PyQt5.QtCore import Qt


class LayoutManagerWidget(QWidget):
    def __init__(self, parent=None, save_callback=None, load_callback=None):
        super().__init__(parent)

        self.save_callback = save_callback
        self.load_callback = load_callback
        self.layouts_dir = "layouts"
        os.makedirs(self.layouts_dir, exist_ok=True)

        self.layout_checkboxes = {}

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        container = QWidget()
        scroll_area.setWidget(container)

        self.outer_layout = QVBoxLayout(self)
        self.outer_layout.addWidget(scroll_area)

        self.main_layout = QVBoxLayout(container)
        self.main_layout.setAlignment(Qt.AlignTop)

        self.setMinimumWidth(300)
        self.setWindowTitle("Layout Manager")
        self.setStyleSheet("background-color: #dcdcdc; font-size: 14px;")

        self._build_ui()

    def _build_ui(self):
        self.main_layout.addWidget(self._separator())
        self.main_layout.addWidget(QLabel("💾 Save Layout"))

        save_row = QHBoxLayout()
        save_btn = QPushButton("Save")
        save_as_btn = QPushButton("Save As")
        self._style_button(save_btn)
        self._style_button(save_as_btn)
        save_btn.clicked.connect(lambda: self._on_save(False))
        save_as_btn.clicked.connect(lambda: self._on_save(True))
        save_row.addWidget(save_btn)
        save_row.addWidget(save_as_btn)
        self.main_layout.addLayout(save_row)

        self.main_layout.addWidget(self._separator())
        self.main_layout.addWidget(QLabel("📂 Load Layout"))

        load_selected_btn = QPushButton("Load Selected")
        self._style_button(load_selected_btn)
        load_selected_btn.clicked.connect(self._on_load_selected)
        self.main_layout.addWidget(load_selected_btn)

        self.layout_list_container = QVBoxLayout()
        self.main_layout.addLayout(self.layout_list_container)

        self._load_layouts()

        self.main_layout.addWidget(self._separator())
        self.main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def _separator(self):
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        return line

    def _style_button(self, btn):
        btn.setStyleSheet("""
            QPushButton {
                background-color: #c0bcbc;
                padding: 5px 10px;
            }
        """)

    def _load_layouts(self):
        print("Loading layouts from:", self.layouts_dir)
        for i in reversed(range(self.layout_list_container.count())):
            item = self.layout_list_container.takeAt(i)
            if item.widget():
                item.widget().deleteLater()

        self.layout_checkboxes.clear()

        for filename in os.listdir(self.layouts_dir):
            if filename.endswith(".layout"):
                layout_name = filename[:-7]
                print("Found layout:", layout_name)

                row = QHBoxLayout()
                cb = QCheckBox(layout_name)
                self.layout_checkboxes[layout_name] = cb

                delete_btn = QPushButton("🗑")
                delete_btn.setFixedSize(30, 30)
                delete_btn.setStyleSheet("background: none; font-size: 18px;")
                delete_btn.clicked.connect(lambda _, name=layout_name: self._delete_layout(name))

                row.addWidget(cb)
                row.addStretch()
                row.addWidget(delete_btn)
                self.layout_list_container.addLayout(row)

    def _delete_layout(self, name):
        path = os.path.join(self.layouts_dir, f"{name}.layout")
        if os.path.exists(path):
            os.remove(path)
            print(f"Deleted layout: {name}")
            self._load_layouts()
            QMessageBox.information(self, "Deleted", f"Deleted layout:\n{name}")

    def _on_save(self, as_new=False):
        print("Save button clicked, as_new =", as_new)
        if self.save_callback:
            self.save_callback(as_new)
        else:
            print("No save_callback defined!")
        self._load_layouts()

    def _on_load_selected(self):
        selected = [name for name, cb in self.layout_checkboxes.items() if cb.isChecked()]
        print("Selected layouts to load:", selected)
        if not selected:
            QMessageBox.information(self, "No Selection", "Select at least one layout.")
            return
        for name in selected:
            if self.load_callback:
                self.load_callback(name)
