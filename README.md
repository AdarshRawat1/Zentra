# Zentra: Python-Based Voice + Screen Personal Assistant

## Features
- Voice I/O (STT/TTS)
- Gemini Flash/Pro/Vision integration
- Google Calendar (OAuth2, CRUD events)
- WhatsApp Web automation (Selenium)
- Visual UI interaction (Gemini Vision)
- Floating UI (CustomTkinter)
- Privacy-first: no background monitoring, no persistent storage

## Setup
1. **Clone the repo**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Google Calendar:**
   - Create a project in Google Cloud Console
   - Enable Calendar API
   - Download `credentials.json` to project root
   - First run will prompt OAuth2 consent
4. **WhatsApp Web:**
   - Download ChromeDriver and place in project root
   - On first run, scan QR code in browser
5. **Gemini API:**
   - Get API key from Google AI Studio
   - Add to `config.py` as `API_KEY = 'your-key'`

## Running Zentra
```bash
python main.py
```
- Use the hotkey (Shift+/) to activate voice assistant
- Speak your command

## Packaging as Executable
- Install PyInstaller:
  ```bash
  pip install pyinstaller
  ```
- Build:
  ```bash
  pyinstaller --onefile main.py
  ```
- The `.exe` will be in the `dist/` folder

## Privacy
- No background screen/mic monitoring
- No file/folder access unless asked
- No logging or persistent storage
- User prompts before sensitive actions

## Modules
- `zentra_ui.py` — Floating UI
- `voice_assistant.py` — Voice I/O
- `calendar_module.py` — Google Calendar
- `whatsapp_module.py` — WhatsApp Web
- `vision_module.py` — Screen + Gemini Vision
- `gemini_module.py` — Gemini API

---
MIT License 