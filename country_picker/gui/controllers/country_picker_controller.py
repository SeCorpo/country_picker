from PyQt6.QtCore import QObject, QThread, pyqtSignal
import locale
from country_picker.core.service.fetch_countries_raw import fetch_countries_raw

class CountryFetchThread(QThread):
    """ Background thread to fetch and emit a locale-sorted (fixes Åland Islands from being last) list of country names """
    countries_fetched = pyqtSignal(list)
    fetch_failed = pyqtSignal(str)

    def run(self):
        try:
            locale.setlocale(locale.LC_ALL, '')
            countries = fetch_countries_raw()
            names = [c["name"] for c in countries if isinstance(c, dict) and "name" in c]
            sorted_names = sorted(names, key=locale.strxfrm)
            self.countries_fetched.emit(sorted_names)
        except Exception as e:
            self.fetch_failed.emit(str(e))


class CountryPickerController(QObject):
    """Controller connecting view and fetching logic."""
    def __init__(self, view, preselect_country=None):
        super().__init__()
        self.view = view
        self.preselect_country = preselect_country
        self._fetcher = None

        self.view.combo_box.currentIndexChanged.connect(self._on_country_selected)

        self.fetch_countries()

    def fetch_countries(self):
        self._fetcher = CountryFetchThread()
        self._fetcher.countries_fetched.connect(self._on_countries_fetched)
        self._fetcher.fetch_failed.connect(self._on_fetch_failed)
        self._fetcher.start()

    def _on_countries_fetched(self, country_names):
        self.view.update_countries(country_names)
        if self.preselect_country and self.preselect_country in country_names:
            index = country_names.index(self.preselect_country)
            self.view.combo_box.setCurrentIndex(index)
        else:
            self._on_country_selected(self.view.combo_box.currentIndex())

    def _on_fetch_failed(self, error_message):
        # Display error in the label
        self.view.label.setText(f"Error fetching countries: {error_message}")

    def _on_country_selected(self, index):
        country = self.view.combo_box.currentText() if index >= 0 else ""
        self.view.update_selected_country(country)
