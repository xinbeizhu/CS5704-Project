import scrapy


class StackOverflowSpider(scrapy.Spider):
    name = 'stackoverflow_java'
    allowed_domains = ['stackoverflow.com']
    start_urls = ['https://stackoverflow.com/questions/tagged/iot+java']

    def parse(self, response):
        # Extract links to question pages
        for href in response.css('.s-post-summary--content-title a::attr(href)'):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_question)

    def parse_question(self, response):
        
        # Extract question title
        title = response.css('#question-header h1 a::text').get()

        # Extract question description
        description = ''.join(response.css('.s-prose.js-post-body > p::text').getall())

        # Check for an accepted answer and extract it if present
        accepted_answer = ''.join(response.css('.answercell.post-layout--right .s-prose.js-post-body p::text').getall())
        if not accepted_answer:
            accepted_answer = None  # Set to None (will appear as null in JSON) if no accepted answer

        yield {
            'title': title,
            'description': description,
            'accepted_answer': accepted_answer,
        }


# The command to run the spider and output data to a JSON file remains the same:
# scrapy crawl stackoverflow -o posts.json0
