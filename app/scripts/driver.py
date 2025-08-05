from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def init_driver():
    """Boot WebDriver."""
    driver = webdriver.Firefox()
    return driver


driver = init_driver()
driver.get("https://www.bcb.gov.br")


# ---------------------------------------------------------------------------
def find_clickable(
    self, xpath: str, timeout: int = 10, bkg_c: str = "orange", show_exc: bool = True
):
    """Find and return one HTML element based in the xpath given."""
    try:
        loading_xpaths = self.utils.get_xpaths()["siget"]["screens_loading"]
        for loading_xpath in loading_xpaths:
            self.utils.loading_screen(
                self.log, self.driver, loading_xpaths[loading_xpath]
            )

        self.log.write_log(f"Finding clickable: {xpath}", level="FIND_C")

        html_element = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )

        self.log.write_log(f"Clickable found: {xpath}", level="FOUND_C")

        self.driver.execute_script(
            f"""
            arguments[0].style.backgroundColor = '{bkg_c}';
            arguments[0].style.color = 'white';
            arguments[0].style.fontWeight = 'bold';
        """,
            html_element,
        )

    except Exception as e:
        if show_exc:
            self.log.write_log(f"Error finding clickable XPATH: {xpath}", level="ERROR")
            self.log.write_log(f"Error finding clickable ERROR: {e}", level="ERROR")
        if not show_exc:
            self.log.write_log(
                f"Clicakble not found, but it was expected to: {xpath}", level="S_ERROR"
            )
