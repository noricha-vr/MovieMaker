from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import os


def create_headless_chromedriver(width: int = 1280, height: int = 720,
                                 locale='en_US', driver_path: str = None) -> webdriver.Chrome:
    """
    Create headless Chrome driver.
    :param width: width of browser
    :param height: height of browser
    :param locale: locale of browser
    :param driver_path: path of driver
    :return: Chrome driver
    """
    # timeout
    page_load_timeout = 20
    # The following options are required to make headless Chrome
    # Work in a Docker container
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--lang=ja-JP")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument(f"window-size={width},{height}")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument(
        "--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36")
    # Initialize a new browser
    # Change local setting on pc
    os.environ['LANG'] = f'{locale}.UTF-8'
    driver = webdriver.Chrome(ChromeDriverManager(path=driver_path).install(), chrome_options=chrome_options)
    driver.set_page_load_timeout(page_load_timeout)
    return driver
