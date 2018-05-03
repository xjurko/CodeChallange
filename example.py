from consumer import Consumer
from producer import Producer


if __name__ == '__main__':
	urls = [
		'https://www.codetriage.com/?language=Python&page=1',
		'https://www.codetriage.com/?language=Python&page=2',
		'https://www.codetriage.com/?language=Python&page=3',
		'https://www.codetriage.com/?language=Python&page=4',
    ]

	producer = Producer(urls)
	consumer = Consumer(producer, 'output.json')

	producer.start()
	consumer.start()
	producer.join()
	consumer.join()