import setuptools
from distutils.core import setup

setup(
    name='bible-fetcher',
    version='0.0.1',
    description='Fetches bible passages from ChatGPT or BibleGateway',
    author='Darrell Hill',
    author_email='darrellcolehill@gmail.com',
    packages=['fetcher'],
    entry_points={
        'console_scripts': ['bible-fetcher=fetcher.index:entry_point'],
    },
    install_requires=[
        'requests',
    ],
)
