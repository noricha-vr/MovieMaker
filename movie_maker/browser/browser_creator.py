from movie_maker.browser.base_browser import BaseBrowser
from movie_maker.browser.general_browser import GeneralBrowser
from movie_maker.browser.twitter_browser import TwitterBrowser

# Which is better set params to constructor or create_browser?
from movie_maker import MovieConfig


class BrowserCreator:
    def __init__(self, movie_config: MovieConfig):
        self.movie_config = movie_config

    def create_browser(self) -> BaseBrowser:
        """Select customized browser for each domain.
        :return: browser: customized browser
        """
        if self.movie_config.domain == "twitter.com": return TwitterBrowser(self.movie_config)
        return GeneralBrowser(self.movie_config)
