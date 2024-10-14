import setuptools
from distutils.core import setup

setup(
    name='bible-fetcher',
    version='0.0.2',
    description='Fetches bible passages from ChatGPT or BibleGateway',
    author='Darrell Hill',
    author_email='darrellcolehill@gmail.com',
    packages=['fetcher'],
    entry_points={
        'console_scripts': ['bible-fetcher=fetcher.index:entry_point'],
    },
    install_requires=[
        "requests",                # For making HTTP requests
        "beautifulsoup4",          # For parsing HTML (BeautifulSoup)
        "python-dotenv",           # For loading environment variables from a .env file
        "openai",                  # OpenAI library for accessing GPT APIs
        "argparse",                # Standard Python library (already included in Python >= 3.2)
    ],
)
