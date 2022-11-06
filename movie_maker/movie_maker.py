import subprocess
from pathlib import Path
from source_converter import SourceConverter, GithubDownloader
from movie_maker.browser import BrowserCreator
from movie_maker import BrowserConfig, ImageConfig
from movie_maker.browser_config import PdfConfig


class MovieMaker:
    """
    This class is used to make movie from website.
    If input GitHub repository URL, download and converted to HTML. Then take screenshots and make movie.
    """

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
                         # Get image_dir/*.file_type
                         '-pattern_type', 'glob', '-i', f'{image_dir}/*.{file_type}',
                         '-c:v', 'h264',  # codec
                         '-pix_fmt', 'yuv420p',  # pixel format (color space)
                         '-preset', 'veryslow',  # encoding speed
                         '-tune', 'stillimage',  # tune for still image
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

    @staticmethod
    def take_screenshots_github_files(browser_config: BrowserConfig) -> Path:
        """
        Create a movie from the given GitHub url.
        """
        image_dir = None
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
        # TODO Split to take local files screen shots.
        browser = None
        try:
            # Take multi files screenshots.
            browser = BrowserCreator(browser_config).create_browser()
            for html_path in html_file_path:
                browser.open(f"file://{html_path.absolute()}")
                if image_dir is None: image_dir = browser.take_screenshots()
        except Exception as e:
            raise e
        finally:
            browser.driver.quit()
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

    # @staticmethod
    # def pdf_to_image(pdf_config: PdfConfig) -> Path:
    #     """
    #     Convert pdf to image.
    #     :param pdf_config:
    #     :return image_dir:
    #     """
    #     output_image_dir = pdf_config.pdf_path.parent / pdf_config.pdf_path.stem
    #     output_image_dir.mkdir(exist_ok=True, parents=True)
    #     command = ['convert', f'{pdf_config.pdf_path}[0]', f'{output_image_dir}/%03d.png']
    #     subprocess.call(command)
    #     print(f'command: {command}')
    #     return output_image_dir
