#!/usr/bin/env python
"""Real estate web crawler"""
import re
import scrapy.item
import scrapy.selector
import scrapy.contrib.linkextractors.sgml
import scrapy.contrib.spiders
import scrapy.contrib.exporter
import scrapy.signals
import scrapy.xlib.pydispatch.dispatcher
import scrapy.conf
import scrapy.crawler


class RealestateItem(scrapy.item.Item):
    """A real estate listing summary"""
    name = scrapy.item.Field()
    price = scrapy.item.Field()
    propertyType = scrapy.item.Field()
    propertyFeatures = scrapy.item.Field()
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
        start_url = start_url.format(self.allowed_domains[0],
                url.format(search))
        self.start_urls = [start_url.format('', 1)]
        extractor = scrapy.contrib.linkextractors.sgml.SgmlLinkExtractor(
                allow=url.format(re.escape(search)).format('.*', ''))
        rule = scrapy.contrib.spiders.Rule(extractor,
                callback='parse_items', follow=True)
        self.rules = [rule]
        super(RealestateSpider, self).__init__()

    def parse_items(self, response):
        """Parse a page of real estate listings"""
        hxs = scrapy.selector.HtmlXPathSelector(response)
        xpath = '//{0}[contains(@class, "{1}")]'
        for i in hxs.select(xpath.format('div', 'resultBody')):
            item = RealestateItem()
            for field in item.fields:
                path = '.{0}//text()'.format(xpath.format('*', field))
                item[field] = i.select(path).extract()
            yield item


def main():
    """Output the real estate search results in csv format"""
    import signal
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    import argparse
    parser = argparse.ArgumentParser(description='Realestate search results.')
    parser.add_argument('command', choices=['buy', 'rent', 'sold'])
    parser.add_argument('search')
    args = parser.parse_args()
    import sys
    exporter = scrapy.contrib.exporter.CsvItemExporter(sys.stdout)

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
    crawler.crawl(RealestateSpider(args.command, args.search))
    crawler.start()

if __name__ == '__main__':
    main()
