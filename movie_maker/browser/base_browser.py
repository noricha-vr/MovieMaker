import abc
import os
import time
import logging
from pathlib import Path
from typing import List
from movie_maker.headless_driver import create_headless_chromedriver
from movie_maker import BrowserConfig

logger = logging.getLogger(__name__)

class BaseBrowser(metaclass=abc.ABCMeta):

    def __init__(self, browser_config: BrowserConfig):
        self.movie_config = browser_config
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

    def get_page_height(self) -> int:
        """
        Get page height.
        """
        return self.driver.execute_script("return document.body.scrollHeight")

    def get_window_bottom_height(self) -> int:
        """
        Get window bottom height of page.
        """
        return self.driver.execute_script("return window.innerHeight + window.scrollY")

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

    @abc.abstractmethod
    def take_screenshots(self) -> List[str]:
        """
        Take a screenshot of the given URL scrolling each px and returns image_file_paths.
        :return: image_file_paths:
        """

    @abc.abstractmethod
    def wait(self) -> None:
        """
        Wait for page loading.
        """