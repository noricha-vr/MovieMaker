from abc import ABCMeta, abstractmethod
import hashlib
from pathlib import Path
from typing import List
from dataclasses import dataclass


@dataclass
class MovieConfig:
    """
    Movie config.
    :param input_image_dir: image directory path.
    :param output_movie_path: output movie file path.
    :param image_type: image file type.
    :param width: movie width.
    :param frame_rate: frame per second.
    :param speed: 'veryslow', 'slower', 'slow', 'medium', 'fast', 'faster', 'veryfast', 'superfast', 'ultrafast'
    """
    input_image_dir: Path
    output_movie_path: Path
    image_type: str = 'png'
    width: int = 1280
    frame_rate: int = 4
    max_frame_rate: int = 4
    encode_speed = 'medium'

    def __post_init__(self):
        if self.frame_rate > self.max_frame_rate:
            raise ValueError(f'frame_rate should be less than {self.max_frame_rate}')
        if self.width % 2 != 0:
            self.width += 1
        if self.output_movie_path.suffix != '.mp4':
            self.output_movie_path = Path(f"{self.output_movie_path}.mp4")


class BaseConfig(metaclass=ABCMeta):
    fps = 1

    def __post_init__(self) -> None:
        self.apply_limit()

    @property
    def hash(self) -> str:
        return hashlib.sha3_256(str(self.__dict__).encode()).hexdigest()

    @abstractmethod
    def apply_limit(self) -> None:
        pass


@dataclass
class ImageConfig(BaseConfig):
    image_dir: Path
    width: int = 1280
    height: int = 720
    max_width = 1920
    max_height = 1920

    def apply_limit(self) -> None:
        if self.max_width < self.width: self.width = self.max_width
        if self.max_height < self.height: self.height = self.max_height


@dataclass
class BrowserConfig(BaseConfig):
    # user inputs
    url: str = ''
    width: int = 1280
    height: int = 720
    page_height: int = 50000
    scroll: int = 200
    targets: List[str] = None
    locale: str = 'en_US'
    lang: str = 'en-US'
    # limits for browser
    min_scroll = 200
    min_page_height = 3000
    max_page_height = 100000
    max_width = 1920
    max_height = 1920
    # driver settings
    driver_path = Path(__file__).parent
    page_load_timeout = 20

    def __post_init__(self):
        if self.url != '': self.domain = self.url.split("/")[2]
        self.lang = self.locale.replace('_', '-')
        super().__post_init__()

    def apply_limit(self) -> None:
        if self.max_width < self.width: self.width = self.max_width
        if self.max_height < self.height: self.height = self.max_height
        if self.max_page_height < self.page_height: self.page_height = self.max_page_height
        if self.scroll < self.min_scroll: self.scroll = self.min_scroll
