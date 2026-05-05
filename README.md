# 🚀 Text Expander

A lightning-fast, system-wide text expansion tool for Windows. Type a short trigger anywhere on your system and instantly paste full messages, templates, and dynamic snippets — no copy-pasting required.

> Think [Text Blaze](https://blaze.today) meets desktop power — completely free and open source.

---

## ✨ Features

- **System-Wide Triggers** — Works in _any_ application: Notepad, Chrome, Slack, Word, you name it.
- **Instant Expansion** — Type `/greet` and watch it vanish, replaced by your full message in milliseconds.
- **Dynamic Form Prompts** — Use `{form:Name}` in your snippets to get a pop-up asking for input before pasting.
- **Persistent Variables** — Store values with `{store:Key}` and recall them later with `{recall:Key}`, even across restarts.
- **Built-in Functions** — Insert today's date automatically with `{func:todayDate}`.
- **Unlimited Snippets** — Create, edit, and delete as many triggers as you need from the dashboard.
- **System Tray** — Runs silently in the background; double-click the tray icon to manage snippets.
- **Bonus: Web Editor** — Includes a standalone browser-based snippet editor for quick testing.

---

## 📦 Installation

### Option 1: Download the EXE (Recommended)

1. Go to the [**Releases**](../../releases) page.
2. Download `TextExpander.exe`.
3. Run it — no installation or Python required.

> **Note:** Windows may show a SmartScreen warning since the app is unsigned. Click **"More info" → "Run anyway"** to proceed.

### Option 2: Run from Source

```bash
# Clone the repo
git clone https://github.com/marc-av/AV-Blaze.git
cd AV-Blaze

# Create a virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Launch the app
python app.py
```

> **Requires:** Python 3.10+ on Windows.

---

## 🛠️ Usage

### 1. Add a Snippet

Open the dashboard and click **"Add Hotkey"**:

| Field       | Example                                             |
|-------------|-----------------------------------------------------|
| **Label**   | Sales Intro                                         |
| **Trigger** | `/intro`                                            |
| **Content** | `Hi! My name's {form:Name}, I'm a {form:Role}...`  |

### 2. Use It Anywhere

1. Minimize the dashboard (it stays in your system tray).
2. Open **any** app — Notepad, your browser, a chat window.
3. Type your trigger: `/intro`
4. The trigger text is erased and a form pops up asking for `Name` and `Role`.
5. Fill in the fields, hit **Confirm**, and the fully expanded text is pasted instantly.

### 3. Snippet Syntax Reference

| Syntax              | Description                                            | Example                          |
|---------------------|--------------------------------------------------------|----------------------------------|
| `{form:FieldName}`  | Prompts the user for input when the trigger fires.     | `Hello {form:ClientName}!`       |
| `{var:FieldName}`   | Reuses a value already collected by `{form:}`.         | `Best, {var:ClientName}`         |
| `{store:Key}`       | Prompts for input and saves it to disk permanently.    | `Agent: {store:MyName}`          |
| `{recall:Key}`      | Recalls a previously stored value (no prompt).         | `Signed, {recall:MyName}`        |
| `{func:todayDate}`  | Inserts today's date automatically.                    | `Date: {func:todayDate}`         |

---

## 🏗️ Build from Source

To create your own standalone `.exe`:

```bash
# Install build tool
pip install pyinstaller

# Build (or just run build.bat)
pyinstaller --noconfirm --onefile --windowed --name "TextExpander" --add-data "TextBlazeWeb;TextBlazeWeb" app.py
```

The output will be in `dist/TextExpander.exe`.

---

## 📁 Project Structure

```
TextExpander/
├── app.py                  # Application entry point & system tray
├── hotkey_manager.py       # System-wide keystroke monitor & trigger engine
├── data_manager.py         # Snippet CRUD & JSON persistence
├── variable_manager.py     # Persistent variable storage ({store}/{recall})
├── ui_main.py              # Dashboard window (PyQt6)
├── ui_dialogs.py           # Add/Edit snippet dialog
├── ui_form_dialog.py       # Dynamic form prompt dialog
├── requirements.txt        # Python dependencies
├── build.bat               # One-click EXE build script
├── TextBlazeWeb/           # Bonus: browser-based snippet editor
│   ├── index.html
│   └── engine.js
└── README.md
```

---

## ⚠️ Important Notes

- **Run as Administrator** — The app uses a low-level keyboard hook to detect triggers system-wide. Some environments may require elevated privileges.
- **Antivirus False Positives** — Keyboard monitoring tools are occasionally flagged by antivirus software. This is a false positive; the app does **not** log, transmit, or store your keystrokes. You can verify by reading the source code.
- **Windows Only** — This application relies on Windows-specific APIs and is not compatible with macOS or Linux.

---

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/awesome-feature`)
3. Commit your changes (`git commit -m 'Add awesome feature'`)
4. Push to the branch (`git push origin feature/awesome-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
