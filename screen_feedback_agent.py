from vision_module import VisionModule
from gemini_module import GeminiModule
import time

class ScreenFeedbackAgent:
    def __init__(self, delay=1.0):
        self.vision = VisionModule()
        self.gemini = GeminiModule()
        self.delay = delay  # seconds between steps

    def get_screen_description(self, prompt):
        screenshot = self.vision.capture_screenshot()
        description = self.gemini.vision_analyze(prompt, screenshot)
        return description

    def feedback_loop(self, action_sequence, stop_condition=None):
        """
        action_sequence: list of (action_fn, prompt_for_gemini)
        stop_condition: function(description) -> bool
        """
        for action_fn, prompt in action_sequence:
            action_fn()
            time.sleep(self.delay)
            description = self.get_screen_description(prompt)
            print(f"Gemini sees: {description}")
            if stop_condition and stop_condition(description):
                print("Stop condition met.")
                break
        return True 