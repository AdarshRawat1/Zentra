import google.generativeai as genai
from config import API_KEY
from tools import click_element, type_text, open_application, press_key

class GeminiAgent:
    """Manages the conversation and function calling with the Gemini API."""
    def __init__(self):
        try:
            genai.configure(api_key=API_KEY)
            
            system_instruction = """
            You are Zentra, a highly intelligent and autonomous AI assistant that controls the computer. Your primary goal is to help the user achieve their objective by breaking it down into a series of logical steps.

            Your operational loop is: THINK, PLAN, EXECUTE.

            1.  THINK: When the user gives you a complex command (e.g., "send a WhatsApp message to Ridwan"), first understand the entire goal. Do not act immediately.

            2.  PLAN: Your first response should be to outline a step-by-step plan in a numbered list. For example: "Okay, to do that, here is my plan: 1. I will open WhatsApp. 2. I will search for 'Ridwan'. 3. I will click on his chat. 4. I will type your message. 5. I will send the message."

            3.  EXECUTE: After presenting the plan, execute ONLY the first step. Then, confirm its completion and describe what you see on the screen now. For example: "I have now opened WhatsApp. I can see the main chat list."

            4.  ADAPT & PROMPT: Wait for the user's confirmation ("okay," "proceed," "yes") or their next instruction. If you encounter ambiguity (e.g., "I see two people named Ridwan"), describe the options and ask the user for clarification ("Which one should I message? The one with the blue profile picture, or the one with no picture?").

            Always use the conversation history as your memory to track your progress through the plan. Be proactive and methodical.
            """
            
            self.model = genai.GenerativeModel(
                model_name='gemini-1.5-flash-latest',
                tools=[click_element, type_text, open_application, press_key],
                system_instruction=system_instruction
            )
            self.chat = self.model.start_chat(enable_automatic_function_calling=True)
            print("Autonomous Gemini Agent initialized successfully.")
        except Exception as e:
            print(f"FATAL: Could not initialize Gemini Agent: {e}")
            self.model = None

    def get_response(self, user_command):
        """Sends a command to the ongoing chat and gets the final response."""
        if not self.model:
            return "Gemini Agent is not available."
        
        try:
            print("Sending command to Gemini for planning/execution...")
            response = self.chat.send_message(user_command)
            return response.text
        except Exception as e:
            return f"An error occurred while communicating with Gemini: {e}"