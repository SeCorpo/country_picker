from PyQt6.QtCore import QObject
from country_picker.gui.threads.country_fetch_thread import CountryFetchThread
from country_picker.gui.views.pydantic_dynamic_model_view import PydanticDynamicModelView

class CountryPickerController(QObject):
    """ Controller connecting view and fetching logic """
    def __init__(self, view, preselect_country=None):
        super().__init__()
        self.view = view
        self.preselect_country = preselect_country
        self._fetcher = None

        self.view.combo_box.currentIndexChanged.connect(self._on_country_selected)
        self.view.info_button.clicked.connect(self._show_model_info)

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

    def _show_model_info(self):
        viewer = PydanticDynamicModelView(self.view)
        viewer.show()