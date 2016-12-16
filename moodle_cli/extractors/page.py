import bs4
import logging
import re


from moodle_cli.constants import *
from .extractor import Extractor

logger = logging.getLogger(__name__)

class PageExtractor(Extractor):

	IS_HEADER = re.compile('h([1-6])', re.IGNORECASE)

	def __init__(self, *args, **kw):
		super().__init__(*args, **kw)

	def extract(self, resource):
		res = self.extract_title_and_url(resource, redirect=False)
	
		r = self._session.get(res['url'])
		if r.status_code != 200:	
			logger.error('Failed to receive mod_page %s', res.url)
			return res
		
		markdown = self.extract_page_markdown(r)
		res['content'] = markdown	
		return res

	def extract_page_markdown(self, page):
		mod_page = bs4.BeautifulSoup(page.text, 'html.parser')
		main_div = mod_page.select_one('div[role="main"]')

		if main_div is  None:
			logger.warn('Received empty page for %s', page.url)
			return ""
		
		return self._extract_page_markdown(main_div)
	
	def _extract_page_markdown(self, page_tag, markdown=""):
		for tag in page_tag.children:			
			markdown += self.extract_tag(tag)

		return markdown
	
	def extract_tag(self, tag):
		markdown = ""
		if not isinstance(tag, bs4.element.NavigableString):
			extract = None
			# filter change date
			if (tag.name == 'div' and 'modified' not in tag.attrs['class']):
				extract = self._extract_page_markdown(tag).strip()
			
			if self.IS_HEADER.match(tag.name):
				extract= self.extract_header(tag)
			
			if tag.name == 'p':
				extract= self.extract_paragraph(tag)

			if tag.name == 'a':
				extract= self.extract_link(tag)

			if extract is not None and len(extract) > 1:
				markdown += extract
			
		else:
			string = tag.strip()
			if len(string) > 0:
				markdown += tag.strip()
		
		return markdown
	
	def extract_header(self, tag):
		m = self.IS_HEADER.match(tag.name)
		header_num = int(m.group(1))
		
		markdown = header_num * "#" 
		markdown += tag.string.strip()
		markdown += "\n\n"
		return markdown

	def extract_paragraph(self, tag):
		markdown = self._extract_page_markdown(tag).strip()
		if markdown and len(markdown) > 0:
			return markdown + "\n\n"
		
		return None
	
	def extract_link(self, tag):
		title = tag.text.strip()
		url = tag.attrs['href']
		if title and url:
			return "[{0}]({1})".format(title, url)
