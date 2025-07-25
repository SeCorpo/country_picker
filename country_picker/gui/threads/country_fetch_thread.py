from PyQt6.QtCore import QThread, pyqtSignal
import locale
from country_picker.core.service.fetch_countries_raw import fetch_countries_raw
from requests.exceptions import ConnectionError, Timeout, HTTPError


class CountryFetchThread(QThread):
    """ Background thread to fetch and emit a locale-sorted (fixes Åland Islands from being last) list of country names """
    countries_fetched = pyqtSignal(list)
    fetch_failed = pyqtSignal(str)

    def run(self):
        try:
            try:
                locale.setlocale(locale.LC_ALL, '')
            except locale.Error:
                locale.setlocale(locale.LC_ALL, 'C')
            countries = fetch_countries_raw()
            names = [c["name"] for c in countries if isinstance(c, dict) and "name" in c]
            sorted_names = sorted(names, key=locale.strxfrm)
            self.countries_fetched.emit(sorted_names)
        except ConnectionError:
            self.fetch_failed.emit("Connection error")
        except Timeout:
            self.fetch_failed.emit("Timeout error")
        except HTTPError as e:
            self.fetch_failed.emit(f"HTTP error: {e.response.status_code}")
        except Exception as e:
            self.fetch_failed.emit(f"Unexpected error: {str(e)}")
