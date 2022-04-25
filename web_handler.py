from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
import re
import email_handling as eh


class WebHandleing():
    def __init__(self, userid):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.set_window_size(900, 650)
        self.userid = userid

    def check_url(self, in_url):
        keywords = {"stop":""}
        in_url = in_url
        if in_url[:4] != "http":
            in_url = "https://www.google.com/search?q=" + re.sub("\s", "+", in_url) + "&hl=en"
        return in_url

    def get(self, inp):
        inp = self.check_url(inp)
        self.driver.get(inp)

    def send_tabs(self, amount):
        actions = ActionChains(self.driver)
        for _ in range(int(amount) + 17):
            actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.ENTER)
        actions.perform()

    def screen(self, name="screenshot"):
        self.driver.save_screenshot("output/" + name + ".png")

    def close(self):
        self.driver.close()

    def intial_search(self, website):
        self.get(website)
        self.screen(self.userid)
        eh.sendPic(self.userid, "output/" + self.userid + ".png", "responce", name="Real Tester")

    def secondary_search(self, num):
        print(f"running secondary search on user {self.userid} with {num} amount of tabs")
        self.send_tabs(num)
        self.screen(self.userid)
        eh.sendPic(self.userid, "output/" + self.userid + ".png", "responce", name="Real Tester")
        print("finished secondary search")

    def del_user(self):
        import os
        print(f"delteing file output/{self.userid}.png")
        os.remove(f"output/{self.userid}.png")


def check_type(inp):
    try:
        int(inp)
        return False
    except ValueError:
        return True
