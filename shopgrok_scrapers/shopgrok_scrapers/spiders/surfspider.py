import scrapy

class FishingSpider(scrapy.Spider):
    name = 'surf'
    start_urls = ['https://www.surfboardempire.com.au/products.json?page=1']
    
    page = 1
    website = "https://www.surfboardempire.com.au/products.json?page="

    def parse(self, response):
        jsonResponse = response.json()
        products = jsonResponse['products']

        for p in products:
            url = "https://www.surfboardempire.com.au/products/" + p['handle']
            yield {
                'sku_name'      : p['title'],
                'product_id'    : p['id'],
                'brand'         : p['vendor'],
                'product_url'   : url
            }

        if len(products) != 0:
            self.page = self.page + 1
            yield scrapy.Request(self.website + str(self.page), callback=self.parse)