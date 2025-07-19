import customtkinter as ctk
import threading
import logging
import keyboard

from zentra_ui import ZentraUI
from voice_assistant import VoiceAssistant, AudioRecorder
from agent import GeminiAgent

logging.basicConfig(level=logging.INFO, filename='zentra_debug.log',
                    format='%(asctime)s - %(levelname)s - %(message)s')

class ZentraApp:
    def __init__(self, root):
        self.root = root

        self.root.withdraw()
        self.voice = VoiceAssistant()
        self.recorder = AudioRecorder()
        self.agent = None
        self.current_state = "IDLE"
        self.ui_window = None
        self.ui_app = None
        self.hotkey = "shift+/"
        threading.Thread(target=self.setup_hotkey, daemon=True).start()
        print(f"Zentra is running. Press '{self.hotkey}' to start/stop recording.")

    def setup_hotkey(self):
        keyboard.add_hotkey(self.hotkey, self.hotkey_callback)
        keyboard.wait()

    def hotkey_callback(self):
        if self.current_state == "IDLE":
            self.root.after(0, self.start_recording)
        elif self.current_state == "RECORDING":
            self.root.after(0, self.stop_and_process)

    def start_recording(self):
        self.current_state = "RECORDING"
        print("\nState: IDLE -> RECORDING")
        self.ui_window = ctk.CTkToplevel(self.root)
        self.ui_window.attributes("-alpha", 0.9)
        self.ui_app = ZentraUI(self.ui_window)
        self.ui_app.update_status("Listening...")
        self.recorder.start_recording()
        self.voice.speak("I'm listening.")

    def stop_and_process(self):
        self.current_state = "PROCESSING"
        print("\nState: RECORDING -> PROCESSING")
        self.ui_app.update_status("Got it, processing now...")
        self.voice.speak("Got it, processing now.")
        initial_command = self.recorder.stop_and_transcribe()
        if initial_command:
            threading.Thread(target=self.run_agent_task, args=(initial_command,)).start()
        else:
            self.voice.speak("I didn't hear a command.")
            self.root.after(0, self.cleanup_session)

    def run_agent_task(self, initial_command):
        self.agent = GeminiAgent()
        response_text = self.agent.send_message(initial_command)
        
        self.root.after(0, self.ui_app.update_status, response_text)
        self.voice.speak(response_text)
        
        self.root.after(2000, self.cleanup_session)

    def cleanup_session(self):
        if self.ui_window:
            self.ui_app.stop()
            self.ui_window.destroy()
            self.ui_window = None
        self.current_state = "IDLE"
        print("State reset to IDLE. Ready for next activation.")

if __name__ == "__main__":
    try:
        ctk.set_appearance_mode("dark")
        root = ctk.CTk()
        app = ZentraApp(root)
        root.mainloop()
    except Exception as e:
        logging.critical(f"Application failed to start: {e}")
        print(f"Application failed to start: {e}")
        print("This may be a permissions issue. Try running as an administrator.")