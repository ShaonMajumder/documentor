#from distutils.core import setup
from setuptools import setup
from os import path

# read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

__version__ = '0.0.0.20.1'


setup(
  name = 'documentor',
  packages = ['documentor'],
  version = '0.0.0.20.1',
  long_description=long_description,
  long_description_content_type='text/markdown',
  author = 'Shaon Majumder',
  author_email = 'smazoomder@gmail.com',
  url = 'https://github.com/ShaonMajumder/documentor',
  download_url = 'https://github.com/ShaonMajumder/documentor/archive/0.0.0.20.1.tar.gz',
  keywords = ['shaon', 'document generator', 'documentation'],
  classifiers = [],
  entry_points={
      'console_scripts': [
          'documentor=documentor.documentor:main',
      ],
  },
)