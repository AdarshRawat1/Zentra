import pyautogui
import json
import os
import time
import google.generativeai as genai

def click_element(description: str):
    """
    Finds and clicks a UI element on the screen based on a text description.
    For example, 'the file menu' or 'the blue login button'.
    """
    print(f"TOOL: Searching for '{description}' to click...")
    screenshot = pyautogui.screenshot()
    prompt = f"Analyze the screenshot to find '{description}'. Respond ONLY with JSON with 'x' and 'y' coordinates."
    
    try:
        vision_model = genai.GenerativeModel('gemini-1.5-flash-latest')
        response = vision_model.generate_content([prompt, screenshot])
        clean_response = response.text.strip().replace("```json", "").replace("```", "")
        coords = json.loads(clean_response)
        x, y = coords.get('x'), coords.get('y')
        
        if x is not None and y is not None:
            pyautogui.click(x, y)
            return f"Successfully clicked on '{description}'."
        else:
            return f"Could not find '{description}' on the screen."
    except Exception as e:
        return f"Error processing click command: {e}"

def type_text(text_to_type: str):
    """Types the given text using the keyboard."""
    print(f"TOOL: Typing text: '{text_to_type}'")
    try:
        pyautogui.write(text_to_type, interval=0.05)
        return "Successfully typed the text."
    except Exception as e:
        return f"Error during typing: {e}"

def open_application(app_name: str):
    """
    Opens a desktop application by searching for it in the Start Menu.
    This is a robust method for Windows.
    """
    print(f"TOOL: Opening '{app_name}' via Start Menu search.")
    try:
        pyautogui.press('win')
        time.sleep(1)
        pyautogui.write(app_name)
        time.sleep(1.5)
        pyautogui.press('enter')
        return f"Successfully launched a search for {app_name}."
    except Exception as e:
        return f"Error opening application via Start Menu: {e}"

def press_key(key_name: str):
    """Presses a specific key on the keyboard (e.g., 'enter', 'esc', 'win')."""
    print(f"TOOL: Pressing key: '{key_name}'")
    try:
        pyautogui.press(key_name)
        return f"Successfully pressed the '{key_name}' key."
    except Exception as e:
        return f"Error pressing key: {e}"