import scrapy

class StackOverflowSpiderDebug(scrapy.Spider):
    name = 'stackoverflow_debug'
    allowed_domains = ['stackoverflow.com']
    start_urls = ['https://stackoverflow.com/questions/tagged/iot']
    count = 0  # Counter to keep track of number of posts scraped

    def parse(self, response):
        self.logger.info(f'Parsing page: {response.url}')
        
        # Extract links to question pages
        for href in response.css('.s-post-summary--content-title a::attr(href)'):
            if self.count < 1000:
                url = response.urljoin(href.extract())
                yield scrapy.Request(url, callback=self.parse_question)
            else:
                self.logger.info('Reached 1000 posts, stopping crawl.')
                break  # Stop crawling if we reach 1000 posts
        
        # Follow pagination link if post count hasn't reached 1000
        if self.count < 1000:
            next_page = response.css('a[rel="next"]::attr(href)').get()
            if next_page:
                next_page_url = response.urljoin(next_page)
                self.logger.info(f'Following pagination to {next_page_url}')
                yield scrapy.Request(next_page_url, callback=self.parse)
            else:
                self.logger.info('No more pages to follow.')

    def parse_question(self, response):
        self.logger.info(f'Parsing question: {response.url}')
        
        # Extract question title
        title = response.css('#question-header h1 a::text').get()

        # Extract question description
        description = ''.join(response.css('.s-prose.js-post-body > p::text').getall())

        # Check for an accepted answer and extract it if present
        accepted_answer = ''.join(response.css('.answercell.post-layout--right .s-prose.js-post-body p::text').getall())
        if not accepted_answer:
            accepted_answer = None  # Set to None (will appear as null in JSON) if no accepted answer

        # Increment post counter for each scraped question
        self.count += 1

        yield {
            'title': title,
            'description': description,
            'accepted_answer': accepted_answer,
        }

# The command to run the spider and output data to a JSON file remains the same:
# scrapy crawl stackoverflow_debug -o posts.json

# Please note the execution part is commented out to avoid running it here.

