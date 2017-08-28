import scrapy, json
from ..items import MedicinpriserItem
class MedSpider(scrapy.Spider):
    name = 'med'
    start_urls = ['https://api.medicinpriser.se/categories?fields=id,slug,name']
    allowed_domains = ['medicinpriser.se']

    def parse(self, response):
        res = json.loads(response.body)
        cat_len = len(res)
        for cat in range(len(res)):
            yield scrapy.Request('https://api.medicinpriser.se/articles/category/{}/count?sort=priceDiffPercentage:DESC'.format(cat+1), callback=self.count, meta={'count': cat+1})
            # yield scrapy.Request('https://www.medicinpriser.se/#/kategori/%s' % cat['slug'], callback=self.count_prods, meta={'len': cat_len})

        # yield scrapy.Request('https://api.medicinpriser.se/articles/category/1/count?sort=priceDiffPercentage:DESC', callback=self.count)
# https://api.medicinpriser.se/articles/category/6?fields=id,slug,substances,data(tradeName,strength,registrationForm),selectedPackage,availablePackagesLength,price,image&limit=&offset=0&sort=priceDiffPercentage:DESC

    def count(self, response):
        yield scrapy.Request('https://api.medicinpriser.se/articles/category/{}?fields=id,slug,substances,data(tradeName,strength,registrationForm),selectedPackage,availablePackagesLength,price,image&limit={}&offset=0&sort=priceDiffPercentage:DESC'.format(response.meta['count'], json.loads(response.body)['count']), callback=self.items_list)

    def items_list(self, response):
        res = json.loads(response.body)
        for prod in res:
            print(
                  prod['id'],
                  prod['slug'],
                  prod['selectedPackage']['desc'],
                  prod['substances'],
                  )

            yield scrapy.Request('https://api.medicinpriser.se/articles/{}?fields=id,slug,title,description,packages,defaultProductNumber,data(shape,atcCode,fassUrl,strength,tradeName,companyName,articleNplId,registrationForm,atcDescription),substances,Categories(id,name,slug),available'.format(prod['slug']), callback=self.parse_item)

    def parse_item(self, response):
        item = MedicinpriserItem()
        res = json.loads(response.body)
        for size in res['packages']:
            item['article_id'] = size['productNumber']
            if item['article_id'] == "":
                item['article_id'] = 'Product or such package is not available'
            item['name'] = res['title']
            item['substance'] = res['description']
            item['size'] = size['size']['numeric']
            item['size_unit'] = size['size']['numericUnit']
            item['form'] = size['desc']
            item['kategori'] = res['Categories'][0]['name']
            item['atc'] = res['data']['atcCode']
            item['aktiv_substans'] = res['substances']
            yield item