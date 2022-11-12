from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import os

from movie_maker import BrowserConfig


def create_headless_chromedriver(browser_config: BrowserConfig) -> webdriver.Chrome:
    """
    Create headless Chrome driver.
    :param browser_config: BrowserConfig object
    :return: Chrome driver
    """
    # Change local setting on pc
    os.environ['LANG'] = f'{browser_config.locale}.UTF-8'
    # timeout
    page_load_timeout = 20
    # The following options are required to make headless Chrome
    # Work in a Docker container
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument(f"--lang={browser_config.lang}")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument(f"window-size={browser_config.width},{browser_config.height}")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument(
        "--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36")
    # Initialize a new browser
    driver = webdriver.Chrome(ChromeDriverManager(
        path=browser_config.driver_path).install(), chrome_options=chrome_options)
    driver.set_page_load_timeout(page_load_timeout)
    return driver
