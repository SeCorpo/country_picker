from PyQt6.QtWidgets import QWidget, QVBoxLayout, QComboBox, QLabel

class CountryPickerView(QWidget):
    """Minimal page widget for picking a country."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.combo_box = QComboBox(self)
        self.label = QLabel(self)
        layout = QVBoxLayout(self)
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
