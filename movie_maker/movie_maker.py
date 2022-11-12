import shutil
import subprocess
import time
from pathlib import Path
from threading import Thread
from typing import List

from source_converter import SourceConverter, GithubDownloader
from movie_maker.browser import BrowserCreator
from movie_maker import BrowserConfig, ImageConfig
from movie_maker.config import MovieConfig


class MovieMaker:
    """
    This class is used to make movie from website.
    If input GitHub repository URL, download and converted to HTML. Then take screenshots and make movie.
    """

    @staticmethod
    def __copy_for_frame_rate_images(image_paths: List[Path], frame_rate) -> None:
        """
        Copy files to create images for frame rate.
        :param image_paths:
        :param frame_rate:
        :return:
        """
        # copy images framerate times -1
        t = []
        for i in range(1, frame_rate):
            for image_path in image_paths:
                # copy image. file name is {image.stem}_{i}.{image.suffix}
                t.append(Thread(target=shutil.copy,
                                args=(
                                    image_path,
                                    image_path.parent.joinpath(f'{image_path.stem}_{i}{image_path.suffix}'))))
        [thread.start() for thread in t]
        [thread.join() for thread in t]

    @staticmethod
    def image_to_movie(movie_config: MovieConfig) -> None:
        """
        Create image_dir files to movie.
        :param image_dir:
        :param movie_path:
        :param file_type: select input file type.
        :param frame_rate: 1 or 2 frame get black screen. 3 or 4 is good.
        :param width: movie width should be even number.
        :return None:
        """
        image_paths = sorted(movie_config.input_image_dir.glob(f'*.{movie_config.image_type}'))
        if len(image_paths) == 0:
            raise Exception(f"No image files in {movie_config.input_image_dir.absolute()}")
        MovieMaker.__copy_for_frame_rate_images(image_paths, movie_config.frame_rate)
        # stop watch
        start = time.time()
        subprocess.call(['ffmpeg',
                         '-framerate', f'{movie_config.frame_rate}',
                         # Select image_dir/*.file_type
                         '-pattern_type', 'glob', '-i', f'{movie_config.input_image_dir}/*.{movie_config.image_type}',
                         '-vf', f"scale='min({movie_config.width},iw)':-2",  # iw is input width, -2 is auto height
                         '-c:v', 'h264',  # codec
                         '-pix_fmt', 'yuv420p',  # pixel format (color space)
                         '-preset', movie_config.encode_speed,
                         '-tune', 'stillimage',  # tune for still image
                         f'{movie_config.output_movie_path}'])
        print(f"MovieMaker.image_to_movie: {time.time() - start} sec")

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

    @staticmethod
    def take_local_file_screenshots(file_paths: List[Path], browser_config: BrowserConfig) -> Path:
        """
        Take screenshots from the given local files.
        :param file_paths:
        :param browser_config:
        :return: image_dir
        """
        image_dir = None
        browser = None
        try:
            # Take multi files screenshots.
            browser = BrowserCreator(browser_config).create_browser()
            for html_path in file_paths:
                browser.open(f"file://{html_path.absolute()}")
                image_dir = browser.take_screenshots()
        except Exception as e:
            raise e
        finally:
            browser.driver.quit()
        return image_dir

    @staticmethod
    def take_screenshots_github_files(browser_config: BrowserConfig) -> Path:
        """
        Create a movie from the given GitHub url.
        :param browser_config:
        :return: movie_path
        """
        # download source code
        words = browser_config.url.split("/")
        if len(words) < 5:
            raise Exception(f"Invalid GitHub URL: {browser_config.url}")
        project_name = words[4]
        folder_path = GithubDownloader.download_github_archive_and_unzip_to_file(browser_config.url, project_name)
        project_path = GithubDownloader.rename_project(folder_path, project_name)
        # Convert the source codes to html files.
        source_converter = SourceConverter('default')
        html_file_path = source_converter.project_to_html(project_path, browser_config.targets)
        image_dir = MovieMaker.take_local_file_screenshots(html_file_path, browser_config)
        return image_dir

    @staticmethod
    def format_images(image_config: ImageConfig) -> Path:
        """
        Get types of image paths. Resize image and convert to png.
        Format images.
        :param image_config:
        :return:
        """
        types = ['jpg', 'jpeg', 'png', 'webp', 'bmp', 'tiff', 'tif', 'svg', 'avif', 'pdf']
        image_paths = []
        for _type in types:
            image_paths.extend(list(image_config.image_dir.glob(f"*.{_type}")))
        output_image_dir = Path(f"{image_config.image_dir}/output")
        output_image_dir.mkdir(exist_ok=True)
        for image_path in image_paths:
            output_path = output_image_dir / f"{image_path.stem}.png"  # convert to png
            # resize image.
            subprocess.call(['convert', f'{image_path}',
                             '-resize', f'{image_config.width}x{image_config.height}',
                             '-quality', '100',
                             f'{output_path}'])
            # fit image width and height.
            subprocess.call(['convert', f'{output_path}',
                             '-background', 'black',
                             '-extent', f'{image_config.width}x{image_config.height}',
                             '-quality', '100',
                             f'{output_path}'])
        return output_image_dir
