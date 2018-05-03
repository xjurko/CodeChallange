from __future__ import with_statement, absolute_import
from threading import Thread
import logging
from concurrent.futures import ThreadPoolExecutor
import requests
try:
	from queue import Queue
except ImportError:
	from Queue import Queue

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Producer(Thread):
	def __init__(self, urls, workers=1):
		super(Producer, self).__init__()
		self.write_buffer = Queue()
		self.urls = urls
		self.workers = workers

	def run(self):
		self._process_urls()

	def _process_urls(self):
		with ThreadPoolExecutor(self.workers) as pool:
			while self.urls:
				pool.submit(self._process_url, self.urls.pop())

			pool.shutdown() # wait for all submited threads to exit and free resources

	def _process_url(self, url):
		raw_html = self._fetch_raw_html(url)
		if raw_html:
			self.write_buffer.put({'url': url, 'raw_html':raw_html})

	def _fetch_raw_html(self, url):
		try:
			response = requests.get(url)
			if response.ok:
				return response.content
			else:
				error_message = '{} responded with status code {}'.format(
								response.url, response.status_code)
				raise requests.ConnectionError(error_message)

		except requests.ConnectionError as E:
			logger.warning(E)

