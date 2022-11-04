import hashlib
from typing import List
from dataclasses import dataclass


@dataclass
class BrowserConfig:
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

    def __post_init__(self):
        if self.url != '': self.domain = self.url.split("/")[2]
        self.driver_path = None
        self.apply_limit()
        self.hash = self.params_to_hash()

    def params_to_hash(self) -> str:
        text = f"{self.url}{self.width}{self.height}{self.max_page_height}{self.scroll_each}{str(self.targets)}".encode()
        return hashlib.sha3_256(text).hexdigest()

    def apply_limit(self) -> None:
        if self.limit_width < self.width: self.width = self.limit_width
        if self.limit_height < self.height: self.height = self.limit_height
        if self.limit_page_height < self.max_page_height: self.max_page_height = self.limit_page_height
        if self.scroll_each < self.limit_minimum_scroll: self.scroll_each = self.limit_minimum_scroll
