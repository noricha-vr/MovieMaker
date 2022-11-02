import abc
import json
import os
import re
import time
import logging
from pathlib import Path
from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from movie_maker.headless_driver import create_headless_chromedriver
from movie_maker import BrowserConfig

logger = logging.getLogger(__name__)


class BaseBrowser(metaclass=abc.ABCMeta):

    def __init__(self, browser_config: BrowserConfig):
        self.browser_config = browser_config
        self.image_folder_path = self.create_image_folder()
        self.driver = create_headless_chromedriver(
            browser_config.width, browser_config.height, browser_config.driver_path)
        self.driver.implicitly_wait(10)
        self.page_no = 0

    @staticmethod
    def create_image_folder() -> Path:
        """
        Create folder named by timestamp
        :return: Path object
        """
        timestamp = str(time.time())[0:10]
        image_folder_path = f"image/{timestamp}"
        os.makedirs(image_folder_path)
        return Path(image_folder_path)

    def delete_image_folder(self) -> None:
        """
        Delete image folder.
        """
        os.rmdir(self.image_folder_path)

    def _get_window_bottom_height(self) -> int:
        """
        Get window bottom height of page.
        """
        return self.driver.execute_script("return window.innerHeight + window.scrollY")

    def _get_link_count(self) -> int:
        """
        Get links count.
        :return: links count.
        """
        return len(self.driver.find_elements(By.XPATH, "//a"))

    def _get_page_no(self) -> str:
        """
        Get page number. for example: 001, 002, 003, ...
        :return: page number.
        """
        return str(self.page_no).zfill(3)

    def open(self, url: str) -> None:
        """open url and set scroll_height"""
        logger.info(f"Open url: {url}")
        self.driver.get(url)
        self.wait()

    def take_screenshots(self) -> Path:
        """
        Scroll each px and Take a screenshot. Then returns image_file_paths.
        Scroll will stop next patterns.
        1. If current window bottom height is over max_height.
        2. If link_count is over initial_link_count * link_increase_rate.
        3. If link_count is decreased and over minimum_page_height.
        :return: image_file_paths:
        """
        file_paths = []
        window_bottom_height = 0
        scroll_to = self.browser_config.scroll_each
        while window_bottom_height != self._get_window_bottom_height():
            window_bottom_height = self._get_window_bottom_height()
            # Take screenshot
            image_path = self.image_folder_path / f"{self._get_page_no()}_{str(scroll_to).zfill(5)}.png"
            self.driver.save_screenshot(str(image_path.absolute()))
            file_paths.append(image_path)
            # If current window bottom height is over max_height.
            if self.browser_config.max_page_height < window_bottom_height:
                break
            # Scroll and update scroll_to
            self.driver.execute_script(f"window.scrollTo(0, {scroll_to})")
            scroll_to += self.browser_config.scroll_each
        self.page_no += 1
        return self.image_folder_path

    def wait(self) -> None:
        """
        Wait for page loading. Load ./site_settings.json and wait for each element or time.
        """
        parent_path = Path(__file__).parent
        with open(parent_path / "site_settings.json") as f:
            site_settings = json.load(f)
        site_setting = site_settings.get(self.browser_config.domain)
        if site_setting is None: return
        for pattern in site_setting:
            match = re.match(pattern, self.driver.current_url)
            if match is None: continue
            params = site_setting[pattern]
            if "xpath" in params and "xpath_timeout" in params:
                try:
                    WebDriverWait(self.driver, params['xpath_timeout']).until(
                        EC.presence_of_element_located((By.XPATH, params["xpath"])))
                except Exception as e:
                    logger.warning(e)
            if "sleep" in params:
                time.sleep(params["sleep"])
            return
