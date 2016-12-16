import logging

from moodle_cli.constants import *
from .extractor import Extractor

class ResourceExtractor(Extractor):

	def __init__(self, *args, **kw):
		super().__init__(*args, **kw)

	def extract(self, resource):
		res = self.extract_title_and_url(resource, redirect=True)
		return res
