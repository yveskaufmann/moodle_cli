import logging
from urllib.parse import unquote
from bs4 import BeautifulSoup


logger = logging.getLogger(__name__)

class Extractor:

	def __init__(self, ctx):
		self._session = ctx._session

	def extract(self, markup):
		raise NotImplementedError()

	
	def extract_title_and_url(self, markup, redirect=True):
		a_tag = markup.select_one('div.activityinstance a')
		title = a_tag.span.next_element
		url = a_tag.get('href')
		
		if (redirect):
			url = self.resolve_url(url)
		
		return {
			'title': title,
			'url': unquote(url)
		}


	def resolve_url(self, url):
		# Resolve the url to determine the real url
		r = self._session.get(url + '&redirect=1', allow_redirects=False)
		
		is_redirect_response = (r.status_code // 100 != 3)
		if  is_redirect_response:
			logger.warning('URL resolving not for %s not possible. Server reponded with %d', url, r.status_code)
		
		resolved_url = r.headers['Location']

		if logger.isEnabledFor(logging.DEBUG):
			logger.debug('Try to resolve url: {0}'.format(url))
			logger.debug('URL resolved to:    {0}'.format(resolved_url))
		
		return resolved_url