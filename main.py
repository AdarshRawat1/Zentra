import tkinter as tk
import threading
import logging
import keyboard
import time
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
        self.current_state = "IDLE"
        self.ui_window = None

        self.hotkey = "shift+/"
        keyboard.add_hotkey(self.hotkey, self.hotkey_callback)
        print(f"Zentra is running. Press '{self.hotkey}' to start/stop recording.")

    def hotkey_callback(self):
        """The main state machine, called by the hotkey."""
        if self.current_state == "IDLE":
            self.start_recording()
        elif self.current_state == "RECORDING":
            self.stop_and_process()

    def start_recording(self):
        self.current_state = "RECORDING"
        print("\nState: IDLE -> RECORDING")

        self.ui_window = tk.Toplevel(self.root)
        self.ui_app = ZentraUI(self.ui_window)
        
        self.recorder.start_recording()
        self.voice.speak("I'm listening.")

    def stop_and_process(self):
        self.current_state = "PROCESSING"
        print("\nState: RECORDING -> PROCESSING")
        self.voice.speak("Got it, processing now.")
        
        command = self.recorder.stop_and_transcribe()

        threading.Thread(target=self.run_agent_task, args=(command,)).start()

    def run_agent_task(self, command):
        """Initializes the agent and processes the command."""
        try:
            if command:
                agent = GeminiAgent() 
                final_response = agent.get_response(command)
                self.voice.speak(final_response)
            else:
                self.voice.speak("I didn't hear a command.")
        finally:
            self.root.after(0, self.cleanup_session)

    def cleanup_session(self):
        """Safely destroys the UI and resets the state."""
        if self.ui_window:
            self.ui_app.stop() 
            self.ui_window.destroy()
            self.ui_window = None
        self.current_state = "IDLE"
        print("State reset to IDLE. Ready for next activation.")


if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = ZentraApp(root)
        root.mainloop()

    except Exception as e:
        logging.critical(f"Application failed to start: {e}")
        print(f"Application failed to start: {e}")
        print("This may be a permissions issue. Try running the script as an administrator.")