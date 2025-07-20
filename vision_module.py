import pyautogui
import google.generativeai as genai
import json

class VisionModule:
    def __init__(self, model_name='gemini-1.5-pro-latest'):
        self.model = genai.GenerativeModel(model_name)

    def capture_screenshot(self):
        return pyautogui.screenshot()

    def analyze_screenshot(self, description):
        screenshot = self.capture_screenshot()
        prompt = f"Analyze the screenshot to find '{description}'. Respond ONLY with JSON with 'x' and 'y' coordinates."
        response = self.model.generate_content([prompt, screenshot])
        clean_response = response.text.strip().replace('```json', '').replace('```', '')
        coords = json.loads(clean_response)
        return coords 