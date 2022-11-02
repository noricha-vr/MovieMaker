import subprocess
from pathlib import Path
from source_converter import SourceConverter, GithubDownloader
from movie_maker.browser import BrowserCreator
from movie_maker import BrowserConfig


class MovieMaker:

    @staticmethod
    def image_to_movie(image_dir: Path, file_name: str, file_type: str = 'png') -> Path:
        """
        Create a movie from the given file paths.
        :param image_dir:
        :param file_name: Don't include file extension.
        :param file_type:
        :return None:
        """
        if len(list(image_dir.glob(f"*.{file_type}"))) == 0:
            raise Exception(f"No image files in {image_dir.absolute()}")
        movie_path = Path(f"{image_dir}/{file_name}.mp4")
        subprocess.call(['ffmpeg',
                         '-framerate', '1',
                         '-pattern_type', 'glob', '-i', f'{image_dir}/*.{file_type}',  # convert image_dir/*.png
                         '-c:v', 'h264', '-pix_fmt', 'yuv420p',
                         '-preset', 'veryslow',
                         '-movflags', '+faststart',
                         f'{movie_path}'])
        return movie_path

    @staticmethod
    def take_screenshots(browser_config: BrowserConfig) -> Path:
        """
        Take screenshots from the given URL.
        :return:
        """
        browser = None
        try:
            browser = BrowserCreator(browser_config).create_browser()
            browser.open(browser_config.url)
            image_paths = browser.take_screenshots()
        except Exception as e:
            raise e
        finally:
            browser.driver.quit()
        return image_paths

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
