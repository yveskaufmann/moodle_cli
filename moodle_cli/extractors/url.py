import logging

from moodle_cli.constants import *
from .extractor import Extractor

logger = logging.getLogger(__name__)

class URLExtractor(Extractor):

	def __init__(self, *args, **kw):
		super().__init__(*args, **kw)

	def extract(self, resource):
		res = self.extract_title_and_url(resource)
		return res

class URLCollector:

	def __init__(self):
		self.links = []
		self._content = None

	def append(self, link): 
		self.links.append(link)
	
	@property
	def content(self):

		def link_to_str(link):
			return "- [{0}]({1})".format(link['title'], link['url'])

		if self._content is None and len(self.links) > 0:
			self._content =  "Link" + "\n"
			self._content += "----" + "\n"
			self._content += "\n"

			link_str = [ link_to_str(link) for link in self.links]
			self._content += "\n".join(link_str)
		
		return self._content

	@property
	def name(self):
		return "links.md"

	def __str__(self):
		return self.content
