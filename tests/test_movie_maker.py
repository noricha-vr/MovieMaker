import os
import glob
from pathlib import Path
import pytest
import shutil
from movie_maker import BrowserConfig, MovieMaker, ImageConfig, BaseBrowser
from movie_maker.config import MovieConfig
import logging

logging.basicConfig(level=logging.INFO, handlers=[logging.StreamHandler()])
for folder in glob.glob("image/*"): shutil.rmtree(folder)
for file in glob.glob("movie/*.mp4"): os.remove(file)


class TestMovieMaker:
    @pytest.mark.parametrize(('url', 'width', 'height', 'limit_height', 'scroll_each', 'length'), [
        ("http://abehiroshi.la.coocan.jp/", 1280, 720, 5000, 100, 1),  # No scroll page test.
        # Language and scroll test.
        ("https://pypi.org/", 1280, 720, 5000, 100, 11),
        # Twitter search test.
        ("https://twitter.com/home", 1280, 720, 5000, 100, 1),
        # Tweet test.
        ("https://twitter.com/noricha_vr/status/1586177429122711552", 1280, 720, 5000, 100, 13),
        # width height limit test
        ("https://gigazine.net/news/20221012-geforce-rtx-4090-benchmark/", 2000, 2000, 2000, 100, 2),
        ("https://forest.watch.impress.co.jp/docs/serial/sspcgame/1436345.html", 720, 1280, 50000, 500, 42),
        (
                "https://www.google.com/maps/place/HUB%E7%A7%8B%E8%91%89%E5%8E%9F%E5%BA%97/@35.700164,138.7193184,9z/data=!3m1!5s0x60188ea7985323af:0x1c68bb773edd834a!4m9!1m2!2m1!1z56eL44OP44OW!3m5!1s0x60188ea7bd68888d:0x25f90a2ae6b34060!8m2!3d35.700164!4d139.7740059!15sCgnnp4vjg4_jg5YiA4gBAVoMIgrnp4sg44OP44OWkgEDcHVimgEkQ2hkRFNVaE5NRzluUzBWSlEwRm5TVVE0YkZsbVFuZG5SUkFC4AEA?hl=ja",
                1280, 720, 0, 500, 1),
        (
                "https://www.google.com/search?q=VRChat&tbm=isch&ved=2ahUKEwij_POxpaX7AhXwS_UHHWbpBQgQ2-cCegQIABAA&oq=VRChat&gs_lcp=CgNpbWcQAzIFCAAQgAQyBQgAEIAEMgUIABCABDIHCAAQBBCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDoECCMQJzoLCAAQgAQQsQMQsQM6BwgjEOoCECc6CAgAEIAEELEDOgsIABAEEIAEECUQIDoNCAAQBBCABBAlECAQGDoPCAAQBBCABBAKECUQIBAYUMkEWPMTYOsWaAFwAHgBgAGHA4gBqwqSAQcxLjIuMi4xmAEAoAEBqgELZ3dzLXdpei1pbWewAQfAAQE&sclient=img&ei=rs9tY6PtMPCX1e8P5tKXQA&bih=1041&biw=1252&rlz=1C5GCEM_enJP1012JP1012",
                1280, 720, 5000, 500, 10),
    ])
    def test_create_static_site_movie(self, url, width, height, limit_height, scroll_each, length):
        # Create movie.
        browser_config = BrowserConfig(url, width, height, limit_height, scroll_each)
        image_dir = MovieMaker.take_screenshots(browser_config)
        assert len(list(image_dir.glob('*.png'))) // browser_config.fps == length, 'Image file counts does not match.'
        movie_path = Path(f'movie/{browser_config.hash}.mp4')
        movie_config = MovieConfig(image_dir, movie_path)
        MovieMaker.image_to_movie(movie_config)
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
        image_dir = MovieMaker.take_screenshots(browser_config)
        assert len(list(image_dir.glob('*.png'))) // browser_config.fps >= length, 'Image file counts does not match.'
        movie_path = Path(f'movie/{browser_config.hash}.mp4')
        movie_config = MovieConfig(image_dir, movie_path)
        MovieMaker.image_to_movie(movie_config)
        assert movie_path.exists(), 'Movie file is not created.'

    @pytest.mark.parametrize(('url', 'targets', 'length'), [
        ('https://github.com/noricha-vr/source_converter', ['*.md', '*.py', ], 22),
    ])
    def test_create_github_movie(self, url, targets, length):
        browser_config = BrowserConfig(url, targets=targets)
        image_dir = MovieMaker.take_screenshots_github_files(browser_config)
        assert len(list(image_dir.glob('*.png'))) // browser_config.fps == length, 'Image file counts does not match.'
        movie_path = Path(f'movie/{browser_config.hash}.mp4')
        movie_config = MovieConfig(image_dir, movie_path)
        MovieMaker.image_to_movie(movie_config)
        assert movie_path.exists(), 'Movie file is not created.'

    @pytest.mark.parametrize(('image_dir', 'length'), [
        (Path('test_image'), 7),
    ])
    def test_create_movie_from_image(self, image_dir, length):
        shutil.rmtree(image_dir / 'output', ignore_errors=True)
        image_config = ImageConfig(image_dir=image_dir)
        formatted_image_dir = MovieMaker.format_images(image_config)
        assert len(list(formatted_image_dir.glob("*"))) // image_config.fps == length, \
            'Image file counts does not match.'
        movie_path = Path(f'movie/{image_config.hash}.mp4')
        movie_config = MovieConfig(formatted_image_dir, movie_path)
        MovieMaker.image_to_movie(movie_config)
        assert movie_path.exists(), 'Movie file is not created.'

    # If you use multi tests, This test can not pass.
    # I don't know why, browser locale is kept with first test locale.
    @pytest.mark.parametrize(('url', 'locale'), [
        ("https://pypi.org/", 'ja_JP'),
        # ("https://pypi.org/", 'zh_CN'),
        # ("https://pypi.org/", 'ko_KR'),
        # ("https://pypi.org/", 'en_US'),
    ])
    def test_switch_locale(self, url, locale):
        browser_config = BrowserConfig(url, locale=locale)
        logging.info(f'Locale: {browser_config.locale}')
        browser = BaseBrowser(browser_config)
        browser.driver.get(browser_config.url)
        browser.driver.save_screenshot(str(browser.image_dir / 'test.png'))
        browser_locale = browser.driver.execute_script('return navigator.language')
        assert browser_locale == locale.replace('_', '-') or browser_locale == locale.split('_')[0], \
            'Locale does not match.'
