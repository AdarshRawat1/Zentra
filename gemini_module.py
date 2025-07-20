import google.generativeai as genai
from config import API_KEY

class GeminiModule:
    def __init__(self, model_name='gemini-1.5-flash-latest'):
        genai.configure(api_key=API_KEY)
        self.model = genai.GenerativeModel(model_name)
        self.chat = self.model.start_chat(enable_automatic_function_calling=True)

    def interpret_command(self, command):
        response = self.chat.send_message(command)
        return response.text

    def vision_analyze(self, prompt, image):
        vision_model = genai.GenerativeModel('gemini-1.5-pro-latest')
        response = vision_model.generate_content([prompt, image])
        return response.text 