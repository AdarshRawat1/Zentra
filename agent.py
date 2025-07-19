import google.generativeai as genai
from config import API_KEY
from tools import click_element, type_text, open_application, press_key

class GeminiAgent:
    def __init__(self):
        genai.configure(api_key=API_KEY)
        
        system_instruction = """
        You are Zentra, a fully autonomous AI assistant that controls the computer. 
        Your goal is to execute the user's command from start to finish.

        Your operational process:
        1.  When the user gives a command, create a silent, internal step-by-step plan.
        2.  Execute the entire plan sequentially using your tools. Do NOT ask for permission or confirmation between steps.
        3.  Only communicate with the user to ask for critical clarification if you are truly stuck (e.g., multiple contacts with the same name).
        4.  Once all steps are complete, provide a single, final confirmation message stating the task is done.
        """
        
        self.model = genai.GenerativeModel(
            model_name='gemini-1.5-flash-latest',
            tools=[click_element, type_text, open_application, press_key],
            system_instruction=system_instruction
        )
        self.chat = self.model.start_chat(enable_automatic_function_calling=True)

    def send_message(self, user_command):
        print(f"Sending to Gemini: '{user_command}'")
        response = self.chat.send_message(user_command)
        return response.text