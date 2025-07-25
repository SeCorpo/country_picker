import json
from PyQt6.QtCore import QThread, pyqtSignal
from country_picker.core.service.fetch_countries_raw import fetch_countries_raw
from country_picker.core.utils.dynamic_schema_from_response import dynamic_model_from_response

class ModelSchemaThread(QThread):
    """ Background thread to generate and emit a dynamic Pydantic model schema """
    schema_ready = pyqtSignal(str)
    failed = pyqtSignal(str)

    def run(self):
        try:
            countries = fetch_countries_raw()
            if not countries:
                raise ValueError("No countries returned from API.")

            model = dynamic_model_from_response(countries, model_name="Country")
            schema = model.model_json_schema()

            if not schema.get("properties"):
                raise ValueError("Generated model has no properties.")

            model_text = json.dumps(schema, indent=2)
            self.schema_ready.emit(model_text)

        except Exception as e:
            self.failed.emit(str(e))
