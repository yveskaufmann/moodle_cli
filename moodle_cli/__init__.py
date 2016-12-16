# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import
import pkg_resources
import logging
import sys

try:
    __version__ = pkg_resources.get_distribution(__name__).version
except:
    __version__ = 'unknown'


# Initialize root Logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


if logger.isEnabledFor(logging.DEBUG):
    formatter = logging.Formatter('[%(filename)s:%(lineno)d %(funcName)10s()][%(levelname)s] - %(message)s')
else:
    formatter = logging.Formatter('%(message)s')

stream_handler = logging.StreamHandler(stream=sys.stdout)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

from moodle_cli.moodle import MoodleCourseDownloader
