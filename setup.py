from setuptools import setup, find_packages

setup(
    name="vrc-movie-maker",
    version="0.2.6",
    license='MIT',
    author="Noricha",
    author_email="noricha.vr@gmail.com",
    packages=find_packages(exclude=['tests', 'tests.*']),
    include_package_data=True,
    install_requires=[
        'selenium>=4.5.0',
        'webdriver-manager>=3.8.4',
        'source-converter>=0.1.14',
        'Pillow>=9.3.0',
    ],
    url='https://github.com/noricha-vr/MovieMaker',
    extras_require={
        "develop": ['pytest']
    },
)
