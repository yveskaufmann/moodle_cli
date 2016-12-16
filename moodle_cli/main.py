import argparse
import json
import os

import moodle_cli
from moodle_cli import utils
from moodle_cli import logger

def main():

	arg_parser = argparse.ArgumentParser(description='Downloads all course files from https://moodle.htw-berlin.de/')
	arg_parser.add_argument('base_dir', type=str, default=os.path.join(os.getcwd(), 'moodle_files'), nargs='?', help='download folder for the course files')
	arg_parser.add_argument('-f', '--force', default=False, help='downloads files even when these already exists.', action='store_true')
	args = arg_parser.parse_args()

	try:
		donwloader = moodle_cli.MoodleCourseDownloader(args.base_dir, not args.force)
		courses = donwloader.extract_course_pages()
		donwloader.extract_and_download(courses)
	except Exception as error:
		logger.exception("Failed to download course content")

	donwloader.shutdown()

	