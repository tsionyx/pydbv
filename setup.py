#!/usr/bin/env python
# pylint: disable=attribute-defined-outside-init

"""
    Distribution module
"""

from setuptools import setup, find_packages


VERSION = '0.0.1'


def read_md(f):
    return open(f, 'r').read()


setup(name='pydbv',
      version=VERSION,
      description='Python database visualizer tools',
      long_description=read_md('README.md'),
      author='Ivan Ladelshchikov',
      author_email='tsionyx@gmail.com',
      url='https://github.com/tsionyx/pydbv',
      license='MIT',
      keywords='database visualize diagram',
      packages=find_packages(),
      install_requires=['pygraphviz', 'SQLAlchemy', 'jinja2'])
