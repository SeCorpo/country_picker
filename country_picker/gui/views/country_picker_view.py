from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QLabel, QPushButton

class CountryPickerView(QWidget):
    """Minimal page widget for picking a country."""
    def __init__(self, parent=None):
        super().__init__(parent)

        self.combo_box = QComboBox(self)
        self.label = QLabel(self)
        self.info_button = QPushButton("ℹ", self)
        self.info_button.setFixedWidth(30)

        # Layout for info button in top-right corner
        top_bar = QHBoxLayout()
        top_bar.addStretch()
        top_bar.addWidget(self.info_button)

        layout = QVBoxLayout(self)
        layout.addLayout(top_bar)
        layout.addWidget(self.combo_box)
        layout.addWidget(self.label)
        self.setLayout(layout)

    def update_countries(self, country_names):
        """Set the list of countries in the combobox."""
        self.combo_box.clear()
        self.combo_box.addItems(country_names)

    def update_selected_country(self, country):
        """Update label with the selected country."""
        self.label.setText(f"Selected: {country}" if country else "")
