from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement

from log.index import Log


class Webdriver:
    def __init__(self):
        self.firefox = webdriver.Firefox()
        self.driver = self.firefox  # Fácil mudança de webdriver caso necessário
        self.log = Log("Webdriver", print_else=True)

    # ---------------------------------------------------------------------------

