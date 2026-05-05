from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QTextEdit, QPushButton, QMessageBox)

class HotkeyDialog(QDialog):
    def __init__(self, parent=None, hotkey_data=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Hotkey" if hotkey_data else "Add Hotkey")
        self.resize(400, 300)
        self.hotkey_data = hotkey_data
        
        self.setup_ui()
        if self.hotkey_data:
            self.load_data()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Label
        label_layout = QHBoxLayout()
        lbl_label = QLabel("Label:")
        lbl_label.setFixedWidth(80)
        self.edit_label = QLineEdit()
        self.edit_label.setPlaceholderText("e.g. Greeting")
        label_layout.addWidget(lbl_label)
        label_layout.addWidget(self.edit_label)
        layout.addLayout(label_layout)

        # Keys
        keys_layout = QHBoxLayout()
        lbl_keys = QLabel("Trigger:")
        lbl_keys.setFixedWidth(80)
        self.edit_keys = QLineEdit()
        self.edit_keys.setPlaceholderText("e.g. /email")
        keys_layout.addWidget(lbl_keys)
        keys_layout.addWidget(self.edit_keys)
        layout.addLayout(keys_layout)
        
        # Hint for keys
        hint_label = QLabel("<i>Format: /shortcut, .greeting, etc.</i>")
        hint_label.setStyleSheet("color: gray;")
        layout.addWidget(hint_label)

        # Content
        content_layout = QVBoxLayout()
        lbl_content = QLabel("Snippet Content:")
        self.edit_content = QTextEdit()
        content_layout.addWidget(lbl_content)
        content_layout.addWidget(self.edit_content)
        layout.addLayout(content_layout)

        # Buttons
        btn_layout = QHBoxLayout()
        self.btn_save = QPushButton("Save")
        self.btn_cancel = QPushButton("Cancel")
        self.btn_save.clicked.connect(self.accept_data)
        self.btn_cancel.clicked.connect(self.reject)
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_save)
        btn_layout.addWidget(self.btn_cancel)
        layout.addLayout(btn_layout)

    def load_data(self):
        self.edit_label.setText(self.hotkey_data.get("label", ""))
        self.edit_keys.setText(self.hotkey_data.get("keys", ""))
        self.edit_content.setPlainText(self.hotkey_data.get("content", ""))

    def accept_data(self):
        if not self.edit_label.text().strip():
            QMessageBox.warning(self, "Validation Error", "Label cannot be empty.")
            return
        if not self.edit_keys.text().strip():
            QMessageBox.warning(self, "Validation Error", "Keys cannot be empty.")
            return
        if not self.edit_content.toPlainText().strip():
            QMessageBox.warning(self, "Validation Error", "Snippet content cannot be empty.")
            return
        
        # Accept the dialog
        self.accept()

    def get_data(self):
        return {
            "label": self.edit_label.text().strip(),
            "keys": self.edit_keys.text().strip().lower(),
            "content": self.edit_content.toPlainText().strip()
        }
