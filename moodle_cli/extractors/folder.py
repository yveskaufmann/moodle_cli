import logging
from bs4 import BeautifulSoup

from moodle_cli.constants import *
from .extractor import Extractor

class FolderExtractor(Extractor):

	def __init__(self, *args, **kw):
		super().__init__(*args, **kw)

	def extract(self, resource):
		res = self.extract_title_and_url(resource, redirect=False)
		
		r = self._session.get(res['url'])
		if r.status_code != 200:
			raise RuntimeError('Failed to extract folder: {0}'.format(res['title']))
		soup = BeautifulSoup(r.text, 'html.parser')
		files = []
		
		for entry in soup.select('span.fp-filename-icon a'):
			files.append({
				'url': entry['href'],
				'filename': entry.select_one('span.fp-filename').text
			})
		
		res['files'] = files
		
		return res
