import os
import glob
import pytest
import shutil
from movie_maker import BrowserConfig, MovieMaker

for folder in glob.glob("image/*"): shutil.rmtree(folder)
for file in glob.glob("movie/*.mp4"): os.remove(file)


class TestMovieMaker:
    @pytest.mark.parametrize(('url', 'width', 'height', 'limit_height', 'scroll_each', 'length'), [
        ("http://abehiroshi.la.coocan.jp/", 1280, 720, 5000, 100, 1),  # No scroll page test.
        ("https://pypi.org/", 1280, 720, 5000, 100, 11),  # Language and scroll test.
        ("https://twitter.com/home", 1280, 720, 5000, 100, 1),  # Twitter search test.
        ("https://twitter.com/noricha_vr/status/1586177429122711552", 1280, 720, 5000, 100, 13),  # Tweet test.
        ("https://gigazine.net/news/20221012-geforce-rtx-4090-benchmark/", 2000, 2000, 2000, 100, 2),  # Limit test
        ("https://forest.watch.impress.co.jp/docs/serial/sspcgame/1436345.html", 720, 1280, 5000, 500, 9),
    ])
    def test_create_static_site_movie(self, url, width, height, limit_height, scroll_each, length):
        # Create movie.
        browser_config = BrowserConfig(url, width, height, limit_height, scroll_each)
        image_paths = MovieMaker.take_screenshots(browser_config)
        assert len(list(image_paths.glob('*.png'))) == length, 'Image file counts does not match.'
        movie_path = MovieMaker.image_to_movie(image_paths, browser_config.hash)
        assert movie_path.exists(), 'Movie file is not created.'

    @pytest.mark.parametrize(('url', 'width', 'height', 'limit_height', 'scroll_each', 'length'), [
        ("https://twitter.com/i/events/1587167761494470656", 1280, 720, 5000, 400, 2),  # Twitter event test.
        ("https://twitter.com/search?q=vrchat&src=typed_query", 1280, 720, 5000, 100, 23),  # Twitter search test.
        ("https://www.youtube.com/", 1280, 720, 5000, 100, 23),  # YouTube top page test
        ("https://www.youtube.com/watch?v=h4wpnoht5y8", 1280, 720, 5000, 500, 2),  # YouTube movie test
    ])
    def test_create_dynamic_site_movie(self, url, width, height, limit_height, scroll_each, length):
        # Create movie.
        browser_config = BrowserConfig(url, width, height, limit_height, scroll_each)
        image_paths = MovieMaker.take_screenshots(browser_config)
        assert len(list(image_paths.glob('*.png'))) >= length, 'Image file counts does not match.'
        movie_path = MovieMaker.image_to_movie(image_paths, browser_config.hash)
        assert movie_path.exists(), 'Movie file is not created.'

    @pytest.mark.parametrize(('url', 'targets', 'length'), [
        ('https://github.com/noricha-vr/source_converter', ['*.md', '*.py', ], 20),
    ])
    def test_create_github_movie(self, url, targets, length):
        browser_config = BrowserConfig(url, targets=targets)
        image_dir = MovieMaker.take_screenshot_github_files(browser_config)
        assert len(list(image_dir.glob('*.png'))) == length, 'Image file counts does not match.'
        movie_path = MovieMaker.image_to_movie(image_dir, browser_config.hash)
        assert movie_path.exists(), 'Movie file is not created.'
