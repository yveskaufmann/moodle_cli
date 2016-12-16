import os
import os.path
import logging
import time

logger = logging.getLogger(__name__)

def remove_dir(path_dir):
	if os.path.isdir(path_dir):
		for child in os.listdir(path_dir):
			remove_dir(os.path.join(path_dir, child))
		os.rmdir(path_dir)
	else:
		os.remove(path_dir)

class DownloadProgess():

	def __init__(self, file_name, file_size=1):
		self.bytes_loaded = 0
		self.start_time = time.time()
		self.max_epochs = 3
		self.epoch_count = 0
		self.file_size = file_size
		self.file_name = file_name
	
	def update(self, loaded_bytes):
		self.bytes_loaded += loaded_bytes
		
		# when file size is known show a percent based download
		if self.file_size > 0: 
			download_progress = round(float(self.bytes_loaded / self.file_size) * 100, 2)
			download_progress_unit = '%' 

		# otherwise show a pending progress bar
		if self.file_size == -1:
			time_consumed = time.time() - start_time	
			
			if time_consumed > 0.5:
				self.epoch_count += 1
				self.start_time = time.time()
						
			if self.epoch_count > self.max_epochs:
				self.epoch_count = 0


			download_progress = "".join(['.' * epoch_count, ' ' * (max_epochs - epoch_count)])
			download_progress_unit = ''

		download_progress = "Downloading {0} {1}{2}".format(self.file_name, download_progress, download_progress_unit)
		print(download_progress, flush=True, end='\r')
	
	def end(self):
		print(end='\n')		

