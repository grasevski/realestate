#!/usr/bin/env python
"""Real estate web crawler"""
import signal
import argparse
import sys
import re
import HTMLParser
import scrapy.item
import scrapy.selector
import scrapy.contrib.linkextractors.sgml
import scrapy.contrib.spiders
import scrapy.contrib.exporter
import scrapy.signals
import scrapy.xlib.pydispatch.dispatcher
import scrapy.conf
import scrapy.crawler


EXPORT_FIELDS = [
        'beds', 'bathrooms', 'cars', 'property_type', 'price',
        'address', 'url', 'title', 'description'
]


class RealestateItem(scrapy.item.Item):
    """A real estate listing summary"""
    beds = scrapy.item.Field()
    bathrooms = scrapy.item.Field()
    cars = scrapy.item.Field()
    property_type = scrapy.item.Field()
    price = scrapy.item.Field()
    address = scrapy.item.Field()
    url = scrapy.item.Field()
    title = scrapy.item.Field()
    description = scrapy.item.Field()


class RealestateSpider(scrapy.contrib.spiders.CrawlSpider):
    """Real estate web crawler"""
    name = 'buyrentsold'
    allowed_domains = ['realestate.com.au']

    def __init__(self, command, search):
        search = re.sub(r'\s+', '+', re.sub(',+', '%2c', search)).lower()
        url = '/{0}/in-{{0}}{{{{0}}}}/list-{{{{1}}}}'.format(command)
        start_url = 'http://www.{0}{1}'
        start_url = start_url.format(
                self.allowed_domains[0], url.format(search)
        )
        self.start_urls = [start_url.format('', 1)]
        extractor = scrapy.contrib.linkextractors.sgml.SgmlLinkExtractor(
                allow=url.format(re.escape(search)).format('.*', '')
        )
        rule = scrapy.contrib.spiders.Rule(
                extractor, callback='parse_items', follow=True
        )
        self.rules = [rule]
        super(RealestateSpider, self).__init__()

    def parse_items(self, response):
        """Parse a page of real estate listings"""
        hxs = scrapy.selector.HtmlXPathSelector(response)
        for i in hxs.select('//div[contains(@class, "resultBody")]'):
            item = RealestateItem()
            path = 'div[contains(@class, "propertyStats")]//text()'
            item['price'] = i.select(path).extract()
            vcard = i.select('div[contains(@class, "vcard")]//a')
            item['address'] = vcard.select('text()').extract()
            url = vcard.select('@href').extract()
            if len(url) == 1:
                item['url'] = 'http://www.{0}{1}'.format(
                        self.allowed_domains[0], url[0]
                )
            listing = i.select('div[contains(@class, "listingInfo")]')
            item['property_type'] = listing.select('span/text()').extract()
            item['title'] = unescape(listing.select('h3/text()').extract())
            item['description'] = unescape(
                    listing.select('p/text()').extract()
            )
            features = listing.select('ul')
            mapping = (
                    ('beds', 'Bedrooms'), ('bathrooms', 'Bathrooms'),
                    ('cars', 'Car Spaces')
            )
            for field, val in mapping:
                path = 'li/img[@alt="{0}"]/../span/text()'.format(val)
                item[field] = features.select(path).extract() or 0
            yield item


def unescape(data):
    """Unescape html text"""
    return HTMLParser.HTMLParser().unescape(','.join(data))


def realestate(command, search, filehandle):
    """Writes the real estate search results to the given file handle"""
    exporter = scrapy.contrib.exporter.CsvItemExporter(
            filehandle, fields_to_export=EXPORT_FIELDS
    )

    def catch_item(sender, item, **kwargs):
        """Output item as a csv line"""
        exporter.export_item(item)

    scrapy.xlib.pydispatch.dispatcher.connect(exporter.start_exporting,
            signal=scrapy.signals.spider_opened)
    scrapy.xlib.pydispatch.dispatcher.connect(exporter.finish_exporting,
            signal=scrapy.signals.spider_closed)
    scrapy.xlib.pydispatch.dispatcher.connect(catch_item,
            signal=scrapy.signals.item_passed)
    scrapy.conf.settings.overrides['LOG_ENABLED'] = False
    crawler = scrapy.crawler.CrawlerProcess(scrapy.conf.settings)
    crawler.install()
    crawler.configure()
    crawler.crawl(RealestateSpider(command, search))
    crawler.start()


def main():
    """Output the real estate search results in csv format"""
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    parser = argparse.ArgumentParser(description='Realestate search results.')
    parser.add_argument('command', choices=['buy', 'rent', 'sold'])
    parser.add_argument('search')
    args = parser.parse_args()
    realestate(args.command, args.search, sys.stdout)
if __name__ == '__main__':
    main()
