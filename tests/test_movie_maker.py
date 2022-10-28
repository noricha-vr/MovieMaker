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
        ("https://www.google.com", 1280, 720, 5000, 100, 1),  # No scroll page test.
        ("https://twitter.com/search?q=vrchat&src=typed_query", 1280, 720, 5000, 100, 25),  # Twitter test.
        ("https://forest.watch.impress.co.jp/docs/serial/sspcgame/1436345.html", 720, 1280, 5000, 500, 9),
        # Change sizes
        ("https://gigazine.net/news/20221012-geforce-rtx-4090-benchmark/", 2000, 2000, 2000, 100, 2),  # Limit test
    ])
    def test_create_site_movie(self, url, width, height, limit_height, scroll_each, length):
        # Create movie.
        movie_config = BrowserConfig(url, width, height, limit_height, scroll_each)
        movie_maker = MovieMaker(movie_config)
        movie_maker.create_movie()
        # Check movie.
        movie = editor.VideoFileClip(str(movie_config.movie_path))
        if width > 1920: width = 1920
        if height > 1920: height = 1920
        assert length == movie.duration
        assert movie.w == width
        assert movie.h == height

    @pytest.mark.parametrize(('url', 'targets'), [
        ('https://github.com/noricha-vr/source_converter', ['*.md', '*.py', ]),
    ])
    def test_create_github_movie(self, url, targets):
        movie_config = BrowserConfig(url, targets=targets)
        MovieMaker(movie_config).create_github_movie()
        movie = editor.VideoFileClip(str(movie_config.movie_path))
        assert movie.duration == 16.0
