from setuptools import setup,find_packages

setup(
    name="MovieMaker",
    version="0.0.1",
    license='MIT',
    author="Noricha",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'Jinja2==2.11.3',
        'moviepy==1.0.3',
        'selenium==4.5.0',
        'webdriver-manager==3.8.4',
        'source-converter==0.1.8',
    ],
    url='https://github.com/noricha-vr/MovieMaker',
    extras_require={
        "develop": ['pytest']
    },
)