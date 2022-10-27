from setuptools import setup,find_packages

setup(
    name="vrc-movie-maker",
    version="0.1.0",
    license='MIT',
    author="Noricha",
    author_email="noricha.vr@gmail.com",
    packages=find_packages(exclude=['tests', 'tests.*']),
    install_requires=[
        'Jinja2>=2.11.3',
        'moviepy>=1.0.3',
        'selenium>=4.5.0',
        'webdriver-manager>=3.8.4',
        'source-converter>=0.1.8',
    ],
    url='https://github.com/noricha-vr/MovieMaker',
    extras_require={
        "develop": ['pytest']
    },
)