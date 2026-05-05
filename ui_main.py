from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
                             QMessageBox)
from PyQt6.QtCore import Qt, pyqtSignal

import data_manager
from ui_dialogs import HotkeyDialog

class MainWindow(QMainWindow):
    # Signal emitted when hotkeys are updated, so app.py can reload the hotkey manager
    hotkeys_updated = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Text Expander Dashboard")
        self.resize(600, 400)
        
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Toolbar / Buttons
        btn_layout = QHBoxLayout()
        self.btn_add = QPushButton("Add Hotkey")
        self.btn_edit = QPushButton("Edit")
        self.btn_delete = QPushButton("Delete")
        
        self.btn_add.clicked.connect(self.on_add)
        self.btn_edit.clicked.connect(self.on_edit)
        self.btn_delete.clicked.connect(self.on_delete)

        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_edit)
        btn_layout.addWidget(self.btn_delete)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Label", "Trigger", "Snippet Preview"])
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.doubleClicked.connect(self.on_edit)
        layout.addWidget(self.table)

    def load_data(self):
        self.hotkeys = data_manager.get_all_hotkeys()
        self.table.setRowCount(len(self.hotkeys))
        for row, hk in enumerate(self.hotkeys):
            self.table.setItem(row, 0, QTableWidgetItem(hk['label']))
            self.table.setItem(row, 1, QTableWidgetItem(hk['keys']))
            # Show a preview of the content
            preview = hk['content'].replace('\n', ' ')
            if len(preview) > 50:
                preview = preview[:47] + "..."
            self.table.setItem(row, 2, QTableWidgetItem(preview))
            
            # Store ID in item data for easy access
            self.table.item(row, 0).setData(Qt.ItemDataRole.UserRole, hk['id'])

        # Notify app to reload hotkey manager
        self.hotkeys_updated.emit(self.hotkeys)

    def get_selected_hk_id(self):
        selected_items = self.table.selectedItems()
        if not selected_items:
            return None
        return self.table.item(selected_items[0].row(), 0).data(Qt.ItemDataRole.UserRole)

    def get_hk_by_id(self, hk_id):
        for hk in self.hotkeys:
            if hk['id'] == hk_id:
                return hk
        return None

    def on_add(self):
        dialog = HotkeyDialog(self)
        if dialog.exec():
            data = dialog.get_data()
            try:
                data_manager.add_hotkey(data['keys'], data['label'], data['content'])
                self.load_data()
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def on_edit(self):
        hk_id = self.get_selected_hk_id()
        if not hk_id:
            QMessageBox.information(self, "Select Item", "Please select a hotkey to edit.")
            return
            
        hk_data = self.get_hk_by_id(hk_id)
        dialog = HotkeyDialog(self, hk_data)
        if dialog.exec():
            data = dialog.get_data()
            try:
                data_manager.update_hotkey(hk_id, data['keys'], data['label'], data['content'])
                self.load_data()
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def on_delete(self):
        hk_id = self.get_selected_hk_id()
        if not hk_id:
            QMessageBox.information(self, "Select Item", "Please select a hotkey to delete.")
            return

        reply = QMessageBox.question(self, "Confirm Delete", 
                                     "Are you sure you want to delete this hotkey?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                data_manager.delete_hotkey(hk_id)
                self.load_data()
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def closeEvent(self, event):
        # Prevent default close, just hide the window to system tray
        event.ignore()
        self.hide()
