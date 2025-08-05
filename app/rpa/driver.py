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
    def find_many(
        self,
        xpath: str,
        timeout: int = 10,
        bkg_c: str = "orange",
        show_exc: bool = True,
    ):
        """Find and return one HTML element based in the xpath given."""
        try:

            self.log.write(f"Finding clickable: {xpath}", level="FIND_C")

            html_elements = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located((By.XPATH, xpath))
            )

            self.log.write(f"Clickable found: {xpath}", level="FOUND_C")
            if html_elements:
                for el in html_elements:
                    self.driver.execute_script(
                        f"""
                        arguments[0].style.backgroundColor = '{bkg_c}';
                        arguments[0].style.color = 'white';
                        arguments[0].style.fontWeight = 'bold';
                        """,
                        el,
                    )
                return html_elements

        except Exception as e:
            if show_exc:
                ...
                self.log.write(f"Error finding clickable XPATH: {xpath}", level="ERROR")
                self.log.write(f"Error finding clickable ERROR: {e}", level="ERROR")
            if not show_exc:
                ...
                self.log.write(
                f"Clicakble not found, but it was expected to: {xpath}", level="S_ERROR"
                )
    
    def find_in(
        self,
        element: WebElement,
        xpath: str,
        timeout: int = 10,
        bkg_c: str = "blue",
        show_exc: bool = True,
    ):
        """Find and return one HTML element based in the xpath given."""
        try:

            self.log.write(f"Finding clickable: {xpath}", level="FIND_C")

            html_elements = WebDriverWait(element, timeout).until(
                EC.presence_of_all_elements_located((By.XPATH, xpath))
            )

            self.log.write(f"Clickable found: {xpath}", level="FOUND_C")
            if html_elements:
                for el in html_elements:
                    self.driver.execute_script(
                        f"""
                        arguments[0].style.backgroundColor = '{bkg_c}';
                        arguments[0].style.color = 'white';
                        arguments[0].style.fontWeight = 'bold';
                        """,
                        el,
                    )
                return html_elements

        except Exception as e:
            if show_exc:
                ...
                self.log.write(f"Error finding clickable XPATH: {xpath}", level="ERROR")
                self.log.write(f"Error finding clickable ERROR: {e}", level="ERROR")
            if not show_exc:
                ...
                self.log.write(
                f"Clicakble not found, but it was expected to: {xpath}", level="S_ERROR"
                )
    
    def kill(self):
        self.driver.close()
