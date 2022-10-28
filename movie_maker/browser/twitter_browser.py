from typing import List
from movie_maker.browser import BaseBrowser
import time


class TwitterBrowser(BaseBrowser):

    def take_screenshots(self) -> List[str]:
        """
        Take a screenshot of the given URL scrolling each px and returns image_file_paths.
        :return: image_file_paths:
        """
        file_paths = []
        # Take screenshots
        for px in range(0, self.movie_config.max_page_height, self.movie_config.scroll_each):
            self.driver.execute_script(f"window.scrollTo(0, {px})")
            file_path = f"{self.image_folder_path}/{px}.png"
            self.driver.save_screenshot(file_path)
            file_paths.append(file_path)
        self.driver.quit()
        return file_paths

    def wait(self) -> None:
        """
        Wait for the javascript rendering.
        :return: None
        """
        time.sleep(6)