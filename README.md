# MovieMaker

This project is convert web pages, images, PDFs, etc. to videos for VRChat

## Installation

```bash
pip install git+https://github.com/noricha-vr/MovieMaker
```

## Setup development environment

```bash
git clone https://github.com/noricha-vr/MovieMaker.git
cd MovieMaker
pip install -r requirements.txt
docker build -t movie_maker .
```

## Usage

From web page URL.

```python
from movie_maker import MovieMaker, MovieConfig

# Please set the url, browser size and scroll.
url = "https://www.google.com/"
width = 1280
height = 720
limit_height = 50000
scroll_each = 200
movie_config = MovieConfig(url, width, height, limit_height, scroll_each)

# create movie
movie_maker = MovieMaker(movie_config)
movie_maker.create_movie() 
```

From GitHub repository.

```python
from movie_maker import MovieMaker, MovieConfig

# Please set the repository URL and what types of file you want.
url = 'https://github.com/noricha-vr/source_converter'
targets = ['*.md', '*.py', ]
movie_config = MovieConfig(url, targets=targets)
# create movie
MovieMaker(movie_config).create_github_movie()
```