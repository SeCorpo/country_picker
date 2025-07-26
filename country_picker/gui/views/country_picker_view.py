from PyQt6.QtWidgets import QWidget, QVBoxLayout, QComboBox, QLabel
from PyQt6.QtCore import Qt

class CountryPickerView(QWidget):
    """ Styled page widget for picking a country """
    def __init__(self, parent=None):
        super().__init__(parent)

        self.combo_box = QComboBox(self)
        self.combo_box.setPlaceholderText("Select a country...")
        self.combo_box.currentTextChanged.connect(self.update_selected_country)

        self.label = QLabel("Selected: None", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.addWidget(self.combo_box)
        layout.addWidget(self.label)

        self.setLayout(layout)
        self.setMinimumWidth(300)

        self.apply_dark_mode_style()

    def update_countries(self, country_names):
        """ Set the list of countries in the combobox """
        self.combo_box.clear()
        self.combo_box.addItems(country_names)

    def update_selected_country(self, country):
        """ Update label with the selected country """
        self.label.setText(f"Selected: {country}" if country else "Selected: None")

    def apply_dark_mode_style(self):
        """ Apply dark mode stylesheet """
        self.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                color: #ffffff;
                font-size: 14px;
                font-family: Segoe UI, sans-serif;
            }
            QComboBox {
                background-color: #3c3c3c;
                border: 1px solid #555;
                padding: 5px;
                border-radius: 4px;
                color: #ffffff;
            }
            QComboBox QAbstractItemView {
                background-color: #3c3c3c;
                color: #ffffff;
                selection-background-color: #555555;
            }
            QLabel {
                color: #dddddd;
            }
        """)
