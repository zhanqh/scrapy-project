# -*- coding: utf-8 -*-
import scrapy
import re
from usedcar.items import UsedcarItem


class Che168Spider(scrapy.Spider):
    name = 'che168'
    allowed_domains = ['www.che168.com']

    # 车龄限制，多少年以内
    start_year = 0
    end_year = 8
    # 爬取车型列表，元组类型(品牌， 型号)
    car_list = [('hafu', 'hafuh6'), ('fengtian', 'rav4rongfang'), ('richan', 'qijun'), ('bentian', 'bentiancrv'), ('dazhong', 'tuguan'), ('fengtian', 'kaimeirui'), ('richan', 'tianzuo'), ('baoma', 'baoma3xi'), ('bentian', 'yage'), ('dazhong', 'maiteng'), ('richan', 'xuanyi'), ('dazhong', 'langyi'), ('bieke', 'yinglang'), ('fengtian', 'kaluola'), ('bentian', 'siyu')]
    # 页码控制即为倒数第8、9位字符，p1 为第一页
    base_url = 'http://www.che168.com/china/{branch}/{model}/a{start_year}_{end_year}msdgscncgpi1ltocsp1exv1x0/'

    def start_requests(self):
        for car in self.car_list:
            yield scrapy.Request(self.base_url.format(branch=car[0], model=car[1], start_year=self.start_year, end_year=self.end_year), callback=self.parse)

    def parse(self, response):
        results = response.xpath('//ul[@id="viewlist_ul"]/li')
        for result in results:
            infoid = result.xpath('./@infoid').extract_first()
            # 不用 re 模块，使用 re_first() 选择器即可
            url = response.urljoin(re.search(r'(/dealer.*?html)', result.xpath('./a/@href').extract_first()).group(1))
            car = result.xpath('.//div[@class="list-photo-info"]/h3/text()').extract_first()
            mileage = result.xpath('.//div[@class="time"]/text()').extract_first().split('／')[0]
            registration_time = result.xpath('.//div[@class="time"]/text()').extract_first().split('／')[1]
            location = result.xpath('.//div[@class="time"]/span[@class="onclick"]/text()').extract_first()
            price = result.xpath('.//div[@class="price"]/em/b/text()').extract_first()
            new_car_tax_price = result.xpath('.//div[@class="price"]/s/text()').extract_first()
            associate_new_car = result.xpath('.//div[@class="tag-area"]/a[@class="tag-quality"]/@title').extract_first()
            warranty_period = result.xpath('.//div[@class="tag-area"]/a[@class="tag-new-almost"]/@title').extract_first()

            usedcar_item = UsedcarItem()
            for field in usedcar_item.fields:
                try:
                    usedcar_item[field] = eval(field)
                except NameError:
                    self.logger.debug(field, '字段没有定义')
            yield usedcar_item

            next_page = response.urljoin(response.xpath('//a[@class="page-item-next"]/@href').extract_first())
            if next_page:
                yield scrapy.Request(next_page, callback=self.parse)
