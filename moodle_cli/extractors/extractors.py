from bs4 import BeautifulSoup
import logging

from moodle_cli.constants import *
from .url import URLExtractor
from .resource import ResourceExtractor
from .page import PageExtractor
from .folder import FolderExtractor

logger = logging.getLogger(__name__)

class Extractors:

	INSTANCES = {}
	
	@staticmethod
	def get_by_type(ctx, type):
		if type in Extractors.INSTANCES:
			return Extractors.INSTANCES[type]
		
		extactor_instance = None
		if type == ACTIVITY_TYPE_RESOURCE:
			extactor_instance = ResourceExtractor(ctx)
		
		if type == ACTIVITY_TYPE_URL:
			extactor_instance = URLExtractor(ctx)

		if type == ACTIVITY_TYPE_PAGE:
			extactor_instance = PageExtractor(ctx)

		if type == ACTIVITY_TYPE_FOLDER:
			extactor_instance = FolderExtractor(ctx)

		if extactor_instance is not None:
			Extractors.INSTANCES[type] = extactor_instance

		return extactor_instance