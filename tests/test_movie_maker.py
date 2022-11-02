import os
import glob
import pytest
import shutil
from moviepy import editor
from movie_maker import BrowserConfig, MovieMaker

# Rest image and movie folder.
for folder in glob.glob("image/*"): shutil.rmtree(folder)
for file in glob.glob("movie/*.mp4"): os.remove(file)


class TestMovieMaker:
    @pytest.mark.parametrize(('url', 'width', 'height', 'limit_height', 'scroll_each', 'length'), [
        ("http://abehiroshi.la.coocan.jp/", 1280, 720, 5000, 100, 1),  # No scroll page test.
        ("https://pypi.org/", 1280, 720, 5000, 100, 11),  # Language and scroll test.
        ("https://twitter.com/home", 1280, 720, 5000, 100, 1),  # Twitter search test.
        ("https://twitter.com/i/events/1587167761494470656", 1280, 720, 5000, 100, 3),  # Twitter search test.
        ("https://twitter.com/search?q=vrchat&src=typed_query", 1280, 720, 5000, 100, 23),  # Twitter search test.
        ("https://twitter.com/noricha_vr/status/1586177429122711552", 1280, 720, 5000, 100, 13),  # Tweet test.
        ("https://gigazine.net/news/20221012-geforce-rtx-4090-benchmark/", 2000, 2000, 2000, 100, 2),  # Limit test
        ("https://www.youtube.com/", 1280, 720, 5000, 100, 23),  # Youtube top page test
        ("https://www.youtube.com/watch?v=h4wpnoht5y8", 1280, 720, 5000, 300, 6),  # YouTube movie test
        ("https://forest.watch.impress.co.jp/docs/serial/sspcgame/1436345.html", 720, 1280, 5000, 500, 9),
        # Change sizes
    ])
    def test_create_site_movie(self, url, width, height, limit_height, scroll_each, length):
        # Create movie.
        browser_config = BrowserConfig(url, width, height, limit_height, scroll_each)
        movie_maker = MovieMaker()
        image_paths = movie_maker.take_screenshots(browser_config)
        movie_path = movie_maker.image_to_movie(image_paths, browser_config.hash)
        # Check movie and image files.
        assert movie_path.exists(), 'Movie file is not created.'
        assert len(list(image_paths.glob('*.png'))) == length, 'Image file counts does not match.'
        movie_maker.image_to_movie(image_paths, browser_config.hash)

    @pytest.mark.parametrize(('url', 'targets'), [
        ('https://github.com/noricha-vr/source_converter', ['*.md', '*.py', ]),
    ])
    def test_create_github_movie(self, url, targets):
        movie_config = BrowserConfig(url, targets=targets)
        MovieMaker(movie_config).create_github_movie()
        movie = editor.VideoFileClip(str(movie_config.movie_path))
        assert movie.duration == 16
