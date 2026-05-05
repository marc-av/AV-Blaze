from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout
from PyQt6.QtCore import Qt

class FormDialog(QDialog):
    def __init__(self, parent=None, required_vars=None):
        super().__init__(parent)
        self.setWindowTitle("Input Required")
        self.resize(300, 100)
        
        # Make the dialog always stay on top since it is triggered system-wide
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
        
        self.required_vars = required_vars or []
        self.inputs = {}
        
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        form_layout = QFormLayout()
        for var in self.required_vars:
            line_edit = QLineEdit()
            self.inputs[var] = line_edit
            form_layout.addRow(QLabel(f"{var}:"), line_edit)
            
        layout.addLayout(form_layout)
        
        btn_layout = QHBoxLayout()
        self.btn_submit = QPushButton("Confirm")
        self.btn_cancel = QPushButton("Cancel")
        
        # Make Enter key submit the form
        self.btn_submit.setDefault(True)
        
        self.btn_submit.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)
        
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_submit)
        
        layout.addLayout(btn_layout)

    def get_values(self):
        return {var: line_edit.text() for var, line_edit in self.inputs.items()}
