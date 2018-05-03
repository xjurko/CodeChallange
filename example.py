from markup_parser import MarkupParser
from markup_extractor import MarkupExtractor


if __name__ == '__main__':
	urls = [
		'https://www.codetriage.com/?language=Python&page=1',
		'https://www.codetriage.com/?language=Python&page=2',
		'https://www.codetriage.com/?language=Python&page=3',
		'https://www.codetriage.com/?language=Python&page=4',
    ]

	producer = MarkupExtractor(urls)
	consumer = MarkupParser(producer, 'output.json')

	producer.start()
	consumer.start()
	producer.join()
	consumer.join()