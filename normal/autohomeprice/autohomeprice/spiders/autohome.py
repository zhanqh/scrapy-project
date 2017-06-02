# -*- coding: utf-8 -*-
import scrapy
import re
from autohomeprice.items import AutohomepriceItem


class AutohomeSpider(scrapy.Spider):
    name = 'autohome'
    allowed_domains = ['autohome.com.cn']
    # 135思域、3170奥迪A3、飞度81、crv314……
    car_ids = ['135', '3085', '3104', '81', '526', '3462', '111', '448', '425', '3294', '78', '634', '110', '3154','3582', '3460', '314', '4102', '4147', '770', '771', '564', '656', '3968', '2987', '145', '2922', '16', '871', '633', '614', '3457', '442', '3170', '528', '496', '66', '692', '588', '197', '65', '18', '874', '2561', '3248', '2951', '812', '3862', '4274']

    # 0默认，1有发票，2没发票
    invoice = '1'


    def start_requests(self):
        for id in self.car_ids:
            yield scrapy.Request('http://jiage.autohome.com.cn/price/carlist/s-'+id, callback=self.parse)


    def parse(self, response):
        car_list = response.xpath('//li[@class="model-list-item"]//a[@class="model-name"]/@href').extract()
        for car in car_list:
            # 车主价格页面的 URL 格式为：http://jiage.autohome.com.cn/price/carlist/p-25892-0-0-1-0-0-1
            # p-25892 是车辆代号，后面 6 位数字依次为按时间排序、按裸车价格排序、有无发票筛选、省份代码、城市代码、页码
            # 时间排序，0为默认，1为从新到旧，2为从旧到新
            # 裸车价格排序，0为默认，1为从高到低，2为从低到高
            # 发票筛选，0为默认，1为有发票，2为没有发票
            url = response.urljoin(re.search(r'(/price.*?)#', car).group(1)) + '-0-0-{invoice}-0-0-1'
            yield scrapy.Request(url.format(invoice=self.invoice), callback=self.parse_detail)

    def parse_detail(self, response):
        results = response.xpath('//ul[@class="price-list"]/li')
        if results.xpath('.//a[@class="uname"]/text()').extract_first():
            for result in results:
                pid = result.xpath('./@data-pkid').extract_first()
                user_name = result.xpath('.//a[@class="uname"]/text()').extract_first().strip()
                user_id = result.xpath('.//div[@class="user-name"]/span[@id="helpspan"]/@data-mid').extract_first()
                # 认证车主
                verified_owner = result.xpath('.//a[@class="uname"]/i[contains(@title, "认证车主")]').extract_first()
                # 发布时间
                post_time = result.xpath('.//span[@class="fn-desc"]/text()').extract_first()
                car_model = result.xpath('.//li[@class="head-item"]/div[@class="txcon"]/a/text()').extract_first()
                price_item_bd = result.xpath('.//div[@class="price-item-bd"]').extract_first()
                # 裸车价
                invoice_price = re.search(r'裸车价.*?price-desc">(.*?)</span>', price_item_bd, re.S).group(1)
                # msrp Manufacture Suggested Retail Price，即厂商指导价
                msrp = re.search(r'指导价.*?txcon">(.*?)</div>', price_item_bd, re.S).group(1)
                purchase_tax = re.search(r'购置税.*?txcon">(.*?)</div>', price_item_bd, re.S).group(1).strip()
                commercial_insurance = re.search(r'商业保险.*?txcon">(.*?)</div>', price_item_bd, re.S).group(1).strip()
                registration_cost = re.search(r'上牌费用.*?txcon">(.*?)</div>', price_item_bd, re.S).group(1).strip()
                vehicle_tax = re.search(r'车船使用税.*?txcon">(.*?)</div>', price_item_bd, re.S).group(1).strip()
                accidents_compulsory_insurance = re.search(r'交强险.*?txcon">(.*?)</div>', price_item_bd, re.S).group(1).strip()
                total_price = re.search(r'合计价格.*?price-desc">(.*?)</span>', price_item_bd, re.S).group(1)

                others_content = re.findall(r'<span>(.*?)</span>.*?"txcon">(.*?)</div>', re.search(r'交强险.*?</li>(.*?)"name">促销套餐', price_item_bd, re.S).group(1), re.S)
                others = []
                for other in others_content:
                    if other[0]:
                        others.append((other[0].strip(), other[1].strip()))

                promotion_package = re.search(r'促销套餐.*?desc">(.*?)</p>', price_item_bd, re.S).group(1)
                buying_time = re.search(r'购车时间.*?txcon">(.*?)</div>', price_item_bd, re.S).group(1)
                buying_province = re.search(r'购车地点.*?pid="(.*?)".*?</div>', price_item_bd, re.S).group(1)
                buying_city = re.search(r'购车地点.*?cid="(.*?)".*?</div>', price_item_bd, re.S).group(1)

                shop_detail = re.search(r'购买商家.*?<p>(.*?)</p>', price_item_bd, re.S).group(1)
                if not re.search('未添加', shop_detail):
                    shop_name = re.search('_blank">(.*?)</a>', shop_detail, re.S).group(1)
                    shop_phone = re.search('phone-num">(.*?)</em>', shop_detail, re.S).group(1)
                    shop_addr = re.search('地址.*?<span>(.*?)</span>', price_item_bd, re.S).group(1)
                    buying_shop = {}
                    buying_shop['shop_name'] = shop_name
                    buying_shop['shop_phone'] = shop_phone
                    buying_shop['shop_addr'] = shop_addr
                else:
                    buying_shop = '该用户未添加购买车辆的商家信息。'

                comment = re.search(r'购买商家.*?</i>(.*?)</span>', price_item_bd, re.S).group(1)
                experiences = re.search(r'购买感受.*?txt-cont">(.*?)</p>', price_item_bd, re.S).group(1).strip()
                
                price_item = AutohomepriceItem()
                for field in price_item.fields:
                    try:
                        price_item[field] = eval(field)
                    except NameError:
                        self.logger.error(field, '字段没有定义')
                yield price_item

        if response.xpath('//a[@class="page-item-next"]'):
            next_page_url = re.search(r'(/price.*?)#', response.xpath('//a[@class="page-item-next"]/@href').extract_first()).group(1)
            yield scrapy.Request(response.urljoin(next_page_url), callback=self.parse_detail)
