# setup.py

from setuptools import setup, find_packages

setup(
    name='zillow_scraper',
    version='1.0.0',
    description='A Python package for extracting housing information from Zillow',
    author='John Doe',
    author_email='john@example.com',
    packages=find_packages(),
    install_requires=[
        'beautifulsoup4',
        'requests',
    ],
)
