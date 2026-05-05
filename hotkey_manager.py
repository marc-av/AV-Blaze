import keyboard
import threading
import time
from PyQt6.QtCore import QObject, pyqtSignal

class HotkeyManager(QObject):
    # Emits (trigger, content)
    trigger_detected = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()
        self._lock = threading.Lock()  # Protects registered_hotkeys + buffer
        self.registered_hotkeys = {}
        self.buffer = ""
        self.hook_handle = None
        self._processing = False  # Guard against re-entrant backspace events

    def start(self, hotkey_list):
        """Register all snippets and start listening."""
        self.reload_hotkeys(hotkey_list)
        
        if not self.hook_handle:
            self.hook_handle = keyboard.on_press(self._on_key_press, suppress=False)

    def reload_hotkeys(self, hotkey_list):
        """Thread-safe reload: pauses hook processing, swaps the dict, clears buffer."""
        new_hotkeys = {}
        for hk in hotkey_list:
            trigger = hk['keys'].lower()
            new_hotkeys[trigger] = hk['content']

        with self._lock:
            self.registered_hotkeys = new_hotkeys
            self.buffer = ""  # Clear stale buffer to prevent phantom matches

    def _on_key_press(self, event):
        # Ignore events while we are sending simulated backspaces
        if self._processing:
            return

        name = event.name
        
        if name == 'backspace':
            char = '\b'
        elif name == 'space':
            char = ' '
        elif name == 'enter':
            char = '\n'
        elif len(name) == 1:
            char = name.lower()
        else:
            # Ignore modifier/control keys (shift, ctrl, alt, etc.)
            return

        with self._lock:
            if char == '\b':
                self.buffer = self.buffer[:-1]
            else:
                self.buffer += char

            # Keep buffer small
            if len(self.buffer) > 50:
                self.buffer = self.buffer[-50:]

            # Take a snapshot of triggers to check against
            triggers_snapshot = dict(self.registered_hotkeys)

        # Check outside the lock to keep it short
        for trigger, content in triggers_snapshot.items():
            if self.buffer.endswith(trigger):
                with self._lock:
                    self.buffer = ""
                # Defer heavy work to a separate thread
                threading.Thread(
                    target=self._handle_trigger,
                    args=(trigger, content),
                    daemon=True
                ).start()
                break

    def _handle_trigger(self, trigger, content):
        """Run outside the hook callback to avoid blocking Windows hooks."""
        self._processing = True
        try:
            # Small pause to let the hook fully return first
            time.sleep(0.05)
            for _ in range(len(trigger)):
                keyboard.send('backspace')
                time.sleep(0.01)
        finally:
            self._processing = False

        # Emit signal to handle parsing and pasting on the main thread
        self.trigger_detected.emit(trigger, content)

    def stop(self):
        if self.hook_handle:
            keyboard.unhook(self.hook_handle)
            self.hook_handle = None
        with self._lock:
            self.registered_hotkeys.clear()
            self.buffer = ""
