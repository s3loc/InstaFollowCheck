from instagramUserInfo import username, password, email
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium import webdriver


class Instagram:
    def __init__(self, email, username, password):
        self.browser = webdriver.Firefox()
        self.email = email
        self.username = username
        self.password = password

    def sign_in(self):
        self.browser.get("https://www.instagram.com/")
        time.sleep(5)

        email_input = self.browser.find_element(By.XPATH, "//input[@name='username']")
        password_input = self.browser.find_element(By.XPATH, "//input[@name='password']")

        email_input.send_keys(self.username)
        password_input.send_keys(self.password)
        password_input.send_keys(Keys.ENTER)
        time.sleep(5)

    def get_list(self, list_type):
        self.browser.get(f"https://www.instagram.com/{self.username}/")
        time.sleep(3)

        if list_type == "followers":
            list_button_xpath = "//a[contains(@href,'/followers/')]"
        elif list_type == "following":
            list_button_xpath = "//a[contains(@href,'/following/')]"
        else:
            raise ValueError("Invalid list type. Choose 'followers' or 'following'.")

        list_button = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, list_button_xpath))
        )
        list_button.click()
        time.sleep(3)

        dialog = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@role='dialog']//ul"))
        )

        # Scrolling down to load all followers/following
        self.scroll_list(dialog)

        users = dialog.find_elements(By.XPATH, "//div[@role='dialog']//ul//li")
        user_list = [user.text.split('\n')[0] for user in users]

        return user_list

    def scroll_list(self, dialog):
        scroll_box = self.browser.find_element(By.XPATH, "//div[@role='dialog']//ul/../..")
        last_height, height = 0, 1
        while last_height != height:
            last_height = height
            time.sleep(1)
            height = self.browser.execute_script("""
                arguments[0].scrollTo(0, arguments[0].scrollHeight);
                return arguments[0].scrollHeight;
            """, scroll_box)

    def get_followers(self):
        return self.get_list("followers")

    def get_following(self):
        return self.get_list("following")

    def compare_followers_following(self):
        followers = self.get_followers()
        following = self.get_following()

        not_following_back = [user for user in following if user not in followers]
        return not_following_back


# Instagram sınıfının örneğini oluşturma
instagram = Instagram(email, username, password)
instagram.sign_in()

not_following_back = instagram.compare_followers_following()
print("These users are not following you back:")
for user in not_following_back:
    print(user)
