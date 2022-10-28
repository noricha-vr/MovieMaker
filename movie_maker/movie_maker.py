from pathlib import Path
from typing import List
from source_converter import SourceConverter,GithubDownloader
from movie_maker.browser import BrowserCreator
from movie_maker import BrowserConfig
from moviepy.editor import ImageSequenceClip


class MovieMaker:

    def __init__(self, movie_config: BrowserConfig, ):
        self.browser_config = movie_config

    @staticmethod
    def image_to_movie(file_paths: List[str], movie_path: str) -> None:
        """
        Create a movie from the given file paths. Each file is 2 seconds.
        :param file_paths:
        :param movie_path:
        :return None:
        """
        clip = ImageSequenceClip(file_paths, fps=1)
        clip.write_videofile(str(movie_path), fps=1)

    def create_movie(self):
        """
        Create a movie from the given url.
        :return:
        """
        browser = None
        try:
            browser = BrowserCreator(self.browser_config).create_browser()
            browser.open(self.browser_config.url)
            image_paths = browser.take_screenshots()
        except Exception as e:
            raise e
        finally:
            browser.driver.quit()
        self.image_to_movie(image_paths, self.browser_config.movie_path)

    def create_github_movie(self) -> Path:
        """
        Create a movie from the given GitHub url.
        """
        # download source code
        project_name = self.browser_config.url.split("/")[4]
        folder_path = GithubDownloader.download_github_archive_and_unzip_to_file(self.browser_config.url, project_name)
        project_path = GithubDownloader.rename_project(folder_path, project_name)
        # Convert the source codes to html files.
        source_converter = SourceConverter('default')
        html_file_path = source_converter.project_to_html(project_path, self.browser_config.targets)
        image_paths = []
        browser = None
        # Take screenshots multi pages.
        try:
            browser = BrowserCreator(self.browser_config).create_browser()
            for html_path in html_file_path:
                browser.open(f"file://{html_path.absolute()}")
                image_paths.extend(browser.take_screenshots())
        except Exception as e:
            browser.driver.quit()
            raise e
        finally:
            browser.driver.quit()
        self.image_to_movie(image_paths, self.browser_config.movie_path)
        return self.browser_config.movie_path
