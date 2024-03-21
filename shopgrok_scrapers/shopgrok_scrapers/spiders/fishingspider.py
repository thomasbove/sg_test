import scrapy

class FishingSpider(scrapy.Spider):
    name = 'fish'
    start_urls = ['https://tackleworldadelaide.com.au/']

    def parse(self, response):
        nav_bar_items = response.xpath('//*[@id="menu"]/nav/ul[1]/li[position() > 1 and position() < last()]')

        for nav_item in nav_bar_items:

            links = nav_item.xpath('.//a[contains(@class, "navPage-subMenu-action")]/@href').getall()

            for link in links:
                yield scrapy.Request(link, callback=self.parse_page)


    def parse_page(self, response):
        products = response.xpath('//*[@id="product-listing-container"]//*[@class="product"]')
        for product in products:
            image_url = product.xpath('.//img/@src').get()
            product_url = product.xpath('.//div[@class="card__buttons"]/a/@href').get()
            price_now = product.xpath('.//span[@class="price"]/text()').get()
            price_was = product.xpath('.//span[@class="price price--rrp"]/text()').get()
            args = {
                'image_url': image_url,
                'price_now': price_now,
                'price_was': price_was,
                'product_url': product_url
            }
            sku = yield scrapy.Request(product_url, callback=self.parse_sku, cb_kwargs=args)

    def parse_sku(self, response, image_url, price_now, price_was, product_url):
        yield {
            'sku_name': response.xpath('//dd[@class="productView-info-value"]/text()').get(),
            'image_url': image_url,
            'price_now': price_now,
            'price_was': price_was,
            'product_url': product_url
        }
