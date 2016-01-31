#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylin: disable=attribute-defined-outside-init
'''
    Distribution module
'''

import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


VERSION = '0.0.1'

try:
    from pypandoc import convert
    read_md = lambda f: convert(f, 'rst')
except ImportError:
    print("warning: pypandoc module not found,"
          " could not convert Markdown to RST")
    read_md = lambda f: open(f, 'r').read()

print read_md('README.md')


class Tox(TestCommand):
    '''
        Provides a way to run tox tests via './setup.py test' call
    '''

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import tox
        sys.exit(tox.cmdline(self.test_args))


# to install:
# sudo apt-get install python-dev virtualenvwrapper pandoc pkg-config graphviz-dev
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
      install_requires=['pygraphviz', 'SQLAlchemy', 'jinja2'],
      tests_require=['tox', 'virtualenv'],
      cmdclass={'test': Tox},
      setup_requires=['pypandoc'])
