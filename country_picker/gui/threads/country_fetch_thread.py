import locale
from PyQt6.QtCore import QThread, pyqtSignal
from requests.exceptions import ConnectionError, Timeout, HTTPError
from pydantic import ValidationError
from country_picker.core.service.fetch_countries_dynamic import fetch_countries_dynamic

class CountryFetchThread(QThread):
    """
    Background thread to fetch and emit a locale-sorted (fixes Åland Islands from being last) list of country names
    Can run with fetch_countries_raw and fetch_countries_dynamic
    """
    countries_fetched = pyqtSignal(list)
    fetch_failed = pyqtSignal(str)

    def run(self):
        try:
            try:
                locale.setlocale(locale.LC_ALL, '')
            except locale.Error:
                locale.setlocale(locale.LC_ALL, 'C')
            countries = fetch_countries_dynamic()
            names = []
            for c in countries:
                if isinstance(c, dict) and "name" in c:
                    names.append(c["name"])
                elif hasattr(c, "name") and getattr(c, "name", None):
                    names.append(c.name)
            country_names = sorted(names, key=locale.strxfrm)
            self.countries_fetched.emit(country_names)
        except ConnectionError:
            self.fetch_failed.emit("Connection error")
        except Timeout:
            self.fetch_failed.emit("Timeout error")
        except HTTPError as e:
            self.fetch_failed.emit(f"HTTP error: {e.response.status_code}")
        except ValidationError as ve:
            self.fetch_failed.emit("Data validation failed.")
        except Exception as e:
            self.fetch_failed.emit(f"Unexpected error: {str(e)}")