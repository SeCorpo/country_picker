from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTextEdit
from country_picker.gui.threads.model_schema_thread import ModelSchemaThread


class PydanticDynamicModelView(QDialog):
    """ Dialog to asynchronously display the dynamically generated Pydantic model schema """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Pydantic Dynamic Model")
        self.resize(500, 400)

        # Text area for displaying the model schema
        self.schema_text = QTextEdit(self)
        self.schema_text.setReadOnly(True)
        self.schema_text.setPlaceholderText("Loading model schema...")

        # Layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.schema_text)
        self.setLayout(layout)

        # Start loading schema
        self._load_schema()

    def _load_schema(self):
        self.schema_loader = ModelSchemaThread()
        self.schema_loader.schema_ready.connect(self._on_schema_loaded)
        self.schema_loader.failed.connect(self._on_schema_failed)
        self.schema_loader.start()

    def _on_schema_loaded(self, text: str):
        self.schema_text.setText(text)

    def _on_schema_failed(self, error: str):
        self.schema_text.setText(f"Error loading schema:\n{error}")
