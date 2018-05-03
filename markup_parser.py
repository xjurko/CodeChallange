from __future__ import with_statement
import json
import logging
from threading import Thread
from bs4 import BeautifulSoup as Soup
try:
	from queue import Empty
except ImportError:
	from Queue import Empty


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class MarkupParser(Thread):
	def __init__(self, producer_thread, output_file):
		super(MarkupParser, self).__init__()
		self.read_buffer = producer_thread.write_buffer
		self.producer = producer_thread
		self.output = output_file

	def run(self):
		output_data = self.process_markup_buffer()
		self._output_write(output_data)

	def process_markup_buffer(self):
		output = []
		while not self._producer_write_complete():
			data = self._try_get_from_buffer()
			if not data:
				continue

			hyperlinks = self._extract_hyperlinks(data['raw_html'])
			output.append({'root_url': data['url'], 'hyperlinks': hyperlinks})

		return output

	def _producer_write_complete(self):
		return not self.producer.is_alive() and self.read_buffer.empty()

	def _try_get_from_buffer(self):
		try:
			data = self.read_buffer.get(timeout=1)
			return data
		except Empty:
			return None

	def _extract_hyperlinks(self, html):
		link_urls = []
		try:
			soup = Soup(html, 'lxml')
			for hyperlink in soup.find_all('a'):
				link_url = hyperlink.get('href')
				if link_url:
					link_urls.append(link_url)

		except Exception as E:
			logger.warning(E)

		return list(set(link_urls))

	def _output_write(self, output_data):
		with open(self.output, 'w') as f:
			json.dump(output_data, f, indent=2)