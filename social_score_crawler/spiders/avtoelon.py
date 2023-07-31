import scrapy


class AutoelonSpider(scrapy.Spider):
    name = "avtoelon"
    allowed_domains = ["avtoelon.uz"]
    start_urls = ['https://avtoelon.uz/uz/avto/']
    # "https://avtoelon.uz/uz/avto/",
    def parse(self, response):
        print('hello')

        cars = response.xpath("//div[@class='row list-item a-elem']")
        for car in cars:
            car_id = car.attrib['data-id']
            id = f'advert-{car_id}'
            # print(f'//*[@id={id}]/div/div[1]/span/text()')
            # "//*[@id=advert-3726720]/div/div[1]/span/text()"
            # "//*[@id="advert-3726720"]/div/div[1]/span/text()"
            div = car.xpath("//div[@class='a-info-side col-right-list']")
            title = div.xpath("//span[@class='a-el-info-title']//a//text()").get()
            price = div.xpath(f'//*[@id="{id}"]/div/div[1]/span/text()').get()
            year = div.xpath(f'//*[@id="{id}"]/div/div[2]/div/span/text()').get()
            description = div.xpath(f'//*[@id="{id}"]/div/div[2]/div/text()').get()
            region = div.xpath(f'//*[@id="{id}"]/div/div[3]/div/a/text()').get()
            car_info = {
                'title': title,
                'price': price,
                'year': year,
                'description': description,
                'region': region
            }
            yield car_info
        next_page = response.xpath('//*[@id="results"]/div[27]/div/div[2]/div/div/div[2]/div/span[2]/a/@href').get()
        if next_page:
            abs_url = f"https://avtoelon.uz{next_page}"
            print(abs_url)
            yield scrapy.Request(
                url=abs_url,
                callback=self.parse
            )
