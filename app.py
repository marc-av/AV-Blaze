import sys
import os
import re
import time
import datetime
import pyperclip
from pynput import keyboard
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QMessageBox
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt

from ui_main import MainWindow
from hotkey_manager import HotkeyManager
from ui_form_dialog import FormDialog
import variable_manager

class TextExpanderApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)

        self.hotkey_mgr = HotkeyManager()
        self.hotkey_mgr.trigger_detected.connect(self.on_trigger_detected)
        
        self.main_window = MainWindow()
        self.main_window.hotkeys_updated.connect(self.on_hotkeys_updated)
        
        self.setup_tray()
        
        self.hotkey_mgr.start(self.main_window.hotkeys)
        
        self.main_window.show()

    def setup_tray(self):
        pixmap = QPixmap(32, 32)
        pixmap.fill(Qt.GlobalColor.blue)
        icon = QIcon(pixmap)
        
        self.tray_icon = QSystemTrayIcon(icon, self.app)
        self.tray_icon.setToolTip("Text Expander")
        
        menu = QMenu()
        
        action_show = menu.addAction("Show Dashboard")
        action_show.triggered.connect(self.main_window.showNormal)
        action_show.triggered.connect(self.main_window.activateWindow)
        
        menu.addSeparator()
        
        action_quit = menu.addAction("Quit")
        action_quit.triggered.connect(self.quit_app)
        
        self.tray_icon.setContextMenu(menu)
        self.tray_icon.activated.connect(self.tray_icon_activated)
        self.tray_icon.show()

    def tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.main_window.showNormal()
            self.main_window.activateWindow()

    def on_hotkeys_updated(self, hotkeys):
        self.hotkey_mgr.reload_hotkeys(hotkeys)

    def on_trigger_detected(self, trigger, content):
        pattern = r"\{([a-z]+):([^}]+)\}"
        matches = re.findall(pattern, content)
        
        required_forms = []
        for match_type, name in matches:
            if match_type in ('form', 'store') and name not in required_forms:
                required_forms.append(name)
                
        local_vars = {}
        if required_forms:
            # We must open the UI dialog
            dialog = FormDialog(required_vars=required_forms)
            if dialog.exec():
                local_vars = dialog.get_values()
            else:
                # Cancelled, do not paste anything
                return
                
        # Now process all replacements using a replacer function
        def replacer(match):
            m_type = match.group(1)
            name = match.group(2)
            
            if m_type == 'form':
                return local_vars.get(name, "")
            elif m_type == 'var':
                return local_vars.get(name, "")
            elif m_type == 'store':
                val = local_vars.get(name, "")
                variable_manager.set_var(name, val)
                return val
            elif m_type == 'recall':
                return variable_manager.get_var(name, "")
            elif m_type == 'func':
                if name == 'todayDate':
                    return datetime.date.today().strftime("%Y-%m-%d")
            return ""
            
        final_text = re.sub(pattern, replacer, content)
        
        self.paste_text(final_text)

    def paste_text(self, text):
        try:
            original = pyperclip.paste()
        except Exception:
            original = ""
            
        time.sleep(0.05)
        
        try:
            pyperclip.copy(text)
            
            controller = keyboard.Controller()
            modifier = keyboard.Key.cmd if sys.platform == 'darwin' else keyboard.Key.ctrl
            
            with controller.pressed(modifier):
                controller.press('v')
                controller.release('v')
                
            time.sleep(0.2)
        except Exception as e:
            print(f"Paste error: {e}")
        finally:
            try:
                pyperclip.copy(original)
            except Exception:
                pass

    def quit_app(self):
        self.hotkey_mgr.stop()
        self.tray_icon.hide()
        self.app.quit()

    def run(self):
        sys.exit(self.app.exec())

if __name__ == "__main__":
    app = TextExpanderApp()
    app.run()
