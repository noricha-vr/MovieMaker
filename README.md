# MovieMaker

This project is convert web pages, images, PDFs, etc. to videos for VRChat

## Installation

```bash
pip install vrc-movie-maker
```

## Setup development environment

```bash
git clone https://github.com/noricha-vr/MovieMaker.git
cd MovieMaker
docker build -t movie_maker .
```

## Sample code

Create movie from URL.

```python
from movie_maker import MovieMaker, BrowserConfig, MovieConfig
from pathlib import Path

# Please set the url, browser size and scroll.
url = "https://www.google.com/"
width = 1280
height = 720
limit_height = 50000
scroll_each = 200
browser_config = BrowserConfig(url, width, height, limit_height, scroll_each)

# create movie
image_dir = MovieMaker.take_screenshots(browser_config)
movie_path = Path(f'movie/{browser_config.hash}.mp4')
movie_config = MovieConfig(image_dir, movie_path)
MovieMaker.image_to_movie(movie_config)
```

Create movie from GitHub repository.

```python
from movie_maker import MovieMaker, BrowserConfig, MovieConfig
from pathlib import Path

# Please set the repository URL and what types of file you want.
url = 'https://github.com/noricha-vr/source_converter'
targets = ['*.md', '*.py', ]
browser_config = BrowserConfig(url, targets=targets)
image_dir = MovieMaker.take_screenshots_github_files(browser_config)
movie_path = Path(f'movie/{browser_config.hash}.mp4')
movie_config = MovieConfig(image_dir, movie_path)
MovieMaker.image_to_movie(movie_config)
```

Create movie from local images.

```python
from movie_maker import MovieMaker, ImageConfig, MovieConfig
from pathlib import Path

image_dir = Path('path/to/image/dir')
image_config = ImageConfig(image_dir)
image_dir = MovieMaker.format_images(image_config)
movie_path = Path(f'movie/{image_config.hash}.mp4')
movie_config = MovieConfig(image_dir, movie_path)
MovieMaker.image_to_movie(movie_config)
```