from abc import ABCMeta, abstractmethod
import hashlib
from pathlib import Path
from typing import List
from dataclasses import dataclass


@dataclass
class MovieConfig:
    """
    Movie config.
    :param image_dir: image directory path.
    :param movie_path: output movie file path.
    :param image_type: image file type.
    :param width: movie width.
    :param frame_rate: frame per second.
    """
    input_image_dir: Path
    output_movie_path: Path
    image_type: str = 'png'
    width: int = 1280
    frame_rate: int = 4
    max_frame_rate: int = 4

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
    limit_width = 1920
    limit_height = 1920

    def apply_limit(self) -> None:
        if self.limit_width < self.width: self.width = self.limit_width
        if self.limit_height < self.height: self.height = self.limit_height


@dataclass
class BrowserConfig(BaseConfig):
    url: str = ''
    width: int = 1280
    height: int = 720
    max_page_height: int = 50000
    scroll_each: int = 200
    targets: List[str] = None
    # limits for browser
    limit_minimum_scroll = 200
    minimum_page_height = 3000
    limit_page_height = 100000
    limit_width = 1920
    limit_height = 1920
    driver_path = None

    def __post_init__(self):
        if self.url != '': self.domain = self.url.split("/")[2]
        super().__post_init__()

    def apply_limit(self) -> None:
        if self.limit_width < self.width: self.width = self.limit_width
        if self.limit_height < self.height: self.height = self.limit_height
        if self.limit_page_height < self.max_page_height: self.max_page_height = self.limit_page_height
        if self.scroll_each < self.limit_minimum_scroll: self.scroll_each = self.limit_minimum_scroll

# @dataclass
# class PdfConfig(BaseConfig):
#     pdf_path: Path
#     is_slide = True
#     width: int = 1280
#     height: int = 720
#     max_page_height: int = 50000
#     scroll_each: int = 200
#     targets: List[str] = None
#     # limits for browser
#     limit_minimum_scroll = 200
#     minimum_page_height = 3000
#     limit_page_height = 100000
#     limit_width = 1920
#     limit_height = 1920
#     driver_path = None
#
#     def __post_init__(self):
#         self.apply_limit()
#         self.hash = self.make_hash()
#
#     def make_hash(self) -> str:
#         text = f"{self.pdf_path}{self.width}{self.height}{self.max_page_height}{self.scroll_each}{str(self.targets)}".encode()
#         return hashlib.sha3_256(text).hexdigest()
#
#     def apply_limit(self) -> None:
#         if self.limit_width < self.width: self.width = self.limit_width
#         if self.limit_height < self.height: self.height = self.limit_height
#         if self.limit_page_height < self.max_page_height: self.max_page_height = self.limit_page_height
#         if self.scroll_each < self.limit_minimum_scroll: self.scroll_each = self.limit_minimum_scroll
