#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from setuptools import setup
from codecs import open

version = '0.1.0'

packages = ['moodle_cli']
requires = []
test_requires = []

with open('requirements.txt', 'r', 'utf-8') as f:
    requires = f.read().split('\n')

with open('test-requirements.txt', 'r', 'utf-8') as f:
    test_requires = f.read().split('\n')

with open('README.rst', 'r', 'utf-8') as f:
    readme = f.read()

with open('CHANGES.rst', 'r', 'utf-8') as f:
    history = f.read()

needs_sphinx = {'build_sphinx', 'upload_docs'}.intersection(sys.argv)
sphinx = ['sphinx'] if needs_sphinx else []

setup(
    name='moodle_cli',
    description=' This program downloads all your course files from https://moodle.htw-berlin.de/',
    long_description= readme + '\n\n' + history,
    version=version,
    author='Yves Kaufmann',
    author_email = 'fxdapokalypse@googlemail.com',
    url = 'http://github.com/yveskaufmann/moodle_cli',
    license='MIT',
    packages=packages,
    install_requires=requires,
    tests_require=test_requires,
    classifiers=(
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only'
    ),
    keywords='moodle-downloader moddle-crawler',
    setup_requires=['six'] + sphinx,
    use_pyscaffold=True,
    entry_points = {'console_scripts': ['moodle_cli=moodle_cli.main:main']},
)



