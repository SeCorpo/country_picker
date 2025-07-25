import json
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTextEdit
from country_picker.core.models.country import Country

class DefinedModelView(QDialog):
    """ Dialog to display the schema of the statically defined Pydantic Country model """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Defined Model")
        self.resize(500, 400)

        # Text area for displaying the model schema
        schema_text = QTextEdit(self)
        schema_text.setReadOnly(True)
        schema_text.setText(_get_model_schema())

        # Layout
        layout = QVBoxLayout(self)
        layout.addWidget(schema_text)
        self.setLayout(layout)

def _get_model_schema() -> str:
    schema = Country.model_json_schema()
    return json.dumps(schema, indent=2)
