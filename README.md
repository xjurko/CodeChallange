![Python 2.7](https://img.shields.io/badge/python-2.7-blue.svg)
![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)
## Code Challenge


  
## MarkupExtractor
  This class extracts raw HTML for each URL passed to it. Raw HTML with original URL is pushed to queue.
  Mutliple URLs can be fetched concurently. Amount of worker threads for fetching is controlled by constructor parrameter.


## MarkupParser
This class parses raw HTML and extracts hyperlinks. Parser subscribes to MarkupExtractor and these classes comunicate via Queue.
Subscription is done by passing the Extractor refference as constructor paramater. Parsed data is written to output file passed in as name to constructor.

## Example Usage
Both classes extend Thread class and can be run concurently. 

```python
from markup_parser import MarkupParser
from markup_extractor import MarkupExtractor

urls = [...]

producer = MarkupExtractor(urls, workers=10)
consumer = MarkupParser(producer, 'output.json')
  
producer.start()
consumer.start()
producer.join()
consumer.join()
```

## MarkupParser Output Format
JSON with following structure:
```json
[
  {
    "root_url": "https://www.example.com/?page=1",
    "hyperlinks": [
      "/example1",
      "/example2"
      ...
    ]
  }
  ...
]
