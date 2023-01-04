import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.crawler import Request
import os 
import logging

class SerieASpidermatch(scrapy.Spider):
    name = "Serie A"
    start_urls = ["https://www.booking.com/"]

    def start_requests(self):
        for d in [URLS]:
            yield Request(d,callback=self.parse)

    def parse(self, response):
        card = response.xpath('//*[@id="outer-edito-content"]/div[3]/main/div[3]/div[2]/div[1]/div/div')
        for i in card:
            winner = i.css('div.TeamScore__name TeamScore__team--winner').get()
            looser = i.css('TeamScore__name TeamScore__team--looser').get()
            score = i.css('TeamScore__score TeamScore__score--ended').getall()
            dic = {
                'winner': winner , 'looser': looser , 'score': score
            }
            
            
            yield dic

# Define a filename
filename = "serie_A_scrap_matches.json"

# Remove previous file if it allready exist
if filename in os.listdir('src/'):
        os.remove('src/' + filename)

# Define the settings for the crawler process
process = CrawlerProcess(settings = {
    # simulate browser
    'USER_AGENT': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:98.0) Gecko/20100101 Firefox/98.0', 
    # display regular errors
    'LOG_LEVEL': logging.INFO,
    "FEEDS": {
        'src/' + filename : {"format": "json"},
    }
})

# Initiate crawler
process.crawl(SerieASpidermatch)
process.start()