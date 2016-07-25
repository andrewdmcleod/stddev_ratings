'''
    movie_spider.py

    written by: Quan Zhou
    written on: December 24th, 2014

    A python script to pull movie reviews from www.rottentomatoes.com

'''

print(__doc__)


import scrapy                                                   
import numpy 

# movies.item is a class that you have to write
from movies.items import MoviesItem

# Library for crawling rules
from scrapy.contrib.spiders import CrawlSpider, Rule            
from scrapy.contrib.linkextractors import LinkExtractor         
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
global rev_arr
rev_arr = []

class MovieSpider(CrawlSpider):
    name = "movie"                                      # Must be unique
    allowed_domains = ["www.rottentomatoes.com"]        # Restrict spiders to a certain domain
    start_urls = [
        "https://www.rottentomatoes.com/m/finding_dory/",
        #"https://www.rottentomatoes.com/top/bestofrt/?year=2014",
        #"http://www.rottentomatoes.com/top/bestofrt/?year=2014",    # Where the first spider starts
    ]

    # See readme.md for more on these rules (note: callback is set on our function 'parse_movie')
    rules = (
        Rule(SgmlLinkExtractor(allow=('https:\/\/www\.rottentomatoes\.com\/m\/finding_dory\/$', ), ), follow=True),
        Rule(SgmlLinkExtractor(allow=('\/m\/\w+\/reviews\/\?type=user$', )), callback='parse_movie', follow=True),
        Rule(SgmlLinkExtractor(allow=('\/m\/\w+\/reviews\/\?page=\d+\&type=user\&sort=$', )), callback='parse_movie', follow=True),
    )

    # This function scrapes information from a page
    def parse_movie(self, response):
        # Assume our xpaths only work on our target page
        try:
            title = response.xpath('//div[@id="content"]//h2/text()').extract()
            page  = response.xpath('//span[@class="pageInfo"]/text()').extract()[0]
        except:
            print "Error in URL: %s" % response.url
            return

        
        print 'Title: %s , %s' % (title, page)
        reviews = set()

        # When we hit the appropriate page, try to scrape the review from each table row
        #for sel in response.xpath('//div[@id="reviews"]//table//tr'):
#        print "GOING IN..."
        count = 0 
        divcount = 0
        for div in response.xpath('//*[@id="reviews"]/div[3]/*'):
            divcount = divcount + 1
            count = 0
            # The content of the review
            #print "HIT IT!"
            #print sel.xpath('@class').extract()
            #print "AFTER HIT"
            for user_review in div.xpath('//*[@id="reviews"]/div[3]/div[{}]/div[2]/span[1]/*'.format(divcount)).extract():
                if "glyphicon" in user_review:
                #if user_review.xpath('.//span[contains(@class, "glyphicon glyphicon-star")]'):
                    count = count + 1
                #else:
                #    print user_review 
            try:
                string = div.xpath('//*[@id="reviews"]/div[3]/div[{}]/div[2]/span[1]/text()'.format(divcount)).extract()
#                print "barry", divcount, string
                if u'\xbd' in string or u' \xbd' in string:
                    #print div.xpath('//*[@id="reviews"]/div[3]/div[{}]/div[2]/span[1]/text()'.format(divcount)).extract()[1]
                    count = count + 0.5
            except:
                pass
#                print "Review:"
            #    print stars
            #print "Review #{}, {}/5".format(divcount, count)
            #    print review 

            # Is this review positive or negative?
            #if sel.xpath('//span[contains(@class, "glyphicon")]'):
            #    print "moo", count
            #    rating = 'MOOOOOMOMOMOMOMOM'
            #elif sel.xpath('.//td//div[contains(@class,"rotten")]'):
            #    print "unmoo"
            #    rating = 'rotten'
            rev_arr.append(count)
#            reviews.add((rating, review))
            
        #print rev_arr
# Push the scraped data into the datastructure we've written
        item = MoviesItem()
        item['title'] = title
        #item['reviews'] = list(reviews)
        #item['page'] = page
        item['std_dev'] = numpy.std(rev_arr)

        yield item
    #item = MoviesItem()
    #item['title'] = title
    #item['std_dev'] = numpy.std(rev_arr)

    #yield item

    #print "Standard deviation for this movie is: "
    #print numpy.std(rev_arr)

