from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from screen_feedback_agent import ScreenFeedbackAgent

class WhatsAppModule:
    def __init__(self, driver_path='chromedriver.exe'):
        self.driver = webdriver.Chrome(driver_path)
        self.driver.get('https://web.whatsapp.com')
        print('Please scan the QR code to log in to WhatsApp Web.')
        time.sleep(15)  # Wait for user to scan QR code
        self.feedback_agent = ScreenFeedbackAgent()

    def send_message(self, contact, message):
        # Step 1: Wait for chat list/search box to be visible
        def wait_for_search_box():
            for _ in range(10):
                try:
                    self.driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
                    return
                except:
                    time.sleep(1)
            raise Exception("Search box not found.")

        # Step 2: Search for contact
        def search_contact():
            search_box = self.driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
            search_box.click()
            search_box.clear()
            search_box.send_keys(contact)
            time.sleep(2)

        # Step 3: Wait for contact to appear
        def wait_for_contact():
            for _ in range(10):
                try:
                    self.driver.find_element(By.XPATH, f'//span[@title="{contact}"]')
                    return
                except:
                    time.sleep(1)
            raise Exception(f"Contact '{contact}' not found.")

        # Step 4: Select contact
        def select_contact():
            contact_title = self.driver.find_element(By.XPATH, f'//span[@title="{contact}"]')
            contact_title.click()
            time.sleep(1)

        # Step 5: Wait for chat to open
        def wait_for_chat():
            for _ in range(10):
                try:
                    self.driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
                    return
                except:
                    time.sleep(1)
            raise Exception("Message box not found.")

        # Step 6: Send message
        def send_msg():
            msg_box = self.driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
            msg_box.send_keys(message + Keys.ENTER)
            print(f'Message sent to {contact}')

        actions = [
            (wait_for_search_box, "Is the WhatsApp chat list and search box visible?"),
            (search_contact, f"Did searching for '{contact}' show the contact in the list?"),
            (wait_for_contact, f"Is the contact '{contact}' visible in the search results?"),
            (select_contact, f"Is the chat open for '{contact}'? Is the message box visible?"),
            (wait_for_chat, f"Is the message box visible for '{contact}'?"),
            (send_msg, f"Was the message sent to '{contact}'? Is there a confirmation or new message in the chat?")
        ]
        self.feedback_agent.feedback_loop(actions)

    def read_last_message(self, contact):
        def search_contact():
            search_box = self.driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
            search_box.click()
            search_box.send_keys(contact)
            time.sleep(2)
        def select_contact():
            contact_title = self.driver.find_element(By.XPATH, f'//span[@title="{contact}"]')
            contact_title.click()
        actions = [
            (search_contact, "Is the contact search box visible? Is the contact found?"),
            (select_contact, "Is the chat open for the contact? Are there messages visible?")
        ]
        self.feedback_agent.feedback_loop(actions)
        messages = self.driver.find_elements(By.XPATH, '//div[contains(@class, "message-in")]//span[@dir="ltr"]')
        if messages:
            return messages[-1].text
        return None 