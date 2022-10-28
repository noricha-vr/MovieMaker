import time
from typing import List
from movie_maker.browser import BaseBrowser


class GeneralBrowser(BaseBrowser):

    def take_screenshots(self) -> List[str]:
        """
        Take a screenshot of the given URL scrolling each px and returns image_file_paths.
        If current window bottom height is over max_height, stop scrolling.
        :return: image_file_paths:
        """
        file_paths = []
        window_bottom_height = self.get_window_bottom_height()
        page_height = self.get_page_height()
        scroll_to = self.movie_config.scroll_each
        while window_bottom_height <= page_height:
            # Take screenshot
            file_path = f"{self.image_folder_path}/{self._get_page_no()}_{window_bottom_height}.png"
            self.driver.save_screenshot(file_path)
            file_paths.append(file_path)
            if self.movie_config.max_page_height < window_bottom_height or \
                    window_bottom_height == page_height:
                break
            # Scroll and update window_bottom_height
            self.driver.execute_script(f"window.scrollTo(0, {scroll_to})")
            scroll_to += self.movie_config.scroll_each
            window_bottom_height = self.get_window_bottom_height()
        self.page_no += 1
        return file_paths

    def take_multi_page_screenshots(self, urls: List[str]) -> List[str]:
        """
        Take a screenshot of the given URLs scrolling each px and returns image_file_paths.
        :return: image_file_paths:
        """
        file_paths = []
        for i, url in enumerate(urls):
            print(f"Take screenshot: {i + 1}/{len(urls)}: {url}")
            self.driver.get(url)
            # time.sleep(5)
            file_paths.extend(self.take_screenshots())
        return file_paths

    def wait(self) -> None:
        pass
