import sys
import argparse
from PyQt6.QtWidgets import QApplication, QMainWindow
from country_picker.gui.views.country_picker_view import CountryPickerView
from country_picker.gui.controllers.country_picker_controller import CountryPickerController

def parse_args():
    parser = argparse.ArgumentParser(description="Country Picker")
    parser.add_argument("--select", type=str, help="Pre-select a country by name", default=None)
    return parser.parse_args()


def main():
    args = parse_args()
    app = QApplication(sys.argv)

    window = QMainWindow()
    window.setWindowTitle("Country Picker")
    window.setGeometry(300, 300, 500, 150)

    page = CountryPickerView()
    controller = CountryPickerController(page, preselect_country=args.select)

    window.setCentralWidget(page)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
