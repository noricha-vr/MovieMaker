import hashlib
from pathlib import Path
from typing import List


class BrowserConfig:
    limit_minimum_scroll = 200
    limit_page_height = 100000
    limit_width = 1920
    limit_height = 1920

    def __init__(self, url: str = '', width: int = 1280, height: int = 720,
                 max_page_height: int = 50000, scroll_each: int = 200, targets: List[str] = None):
        self.url = url
        if url != '': self.domain = url.split("/")[2]
        self.width = width
        self.height = height
        self.max_page_height = max_page_height
        self.scroll_each = scroll_each
        self.targets = targets
        self.params_hash = self.params_to_hash()
        self.movie_path = Path(f"movie/{self.params_hash}.mp4")
        self.driver_path = None
        self.apply_limit()

    def params_to_hash(self):
        text = f"{self.url}{self.width}{self.height}{self.limit_height}{self.scroll_each}{str(self.targets)}".encode()
        return hashlib.sha3_256(text).hexdigest()

    def apply_limit(self):
        if self.width > self.limit_width: self.width = self.limit_width
        if self.height > self.limit_height: self.height = self.limit_height
        if self.limit_height > self.limit_page_height: self.limit_height = self.limit_page_height
        if self.scroll_each < self.limit_minimum_scroll: self.scroll_each = self.limit_minimum_scroll