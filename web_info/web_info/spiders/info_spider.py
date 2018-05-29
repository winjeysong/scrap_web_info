# _*_ coding:utf-8 _*_
import scrapy
from scrapy.selector import Selector
from web_info.items import WebInfoItem
# 引入selenium来模拟鼠标点击
# from selenium import webdriver
# from selenium.webdriver.support.ui import WebDriverWait

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}

class InfoSpider(scrapy.Spider):
    name = 'info'
    def __init__(self):
        super(InfoSpider, self).__init__()
        self.allowed_domains = ['yz.chsi.com.cn']
        self.start_urls = ['http://yz.chsi.com.cn/zsml/queryAction.do']
        # self.driver = webdriver.Chrome()
        # self.driver.set_page_load_timeout(10) # 当获取数据时间超过10秒，即抛出异常

    def start_requests(self):
        for i in range(3, 30):
            print '#### 外部第%s页 ####' %i
            url = 'http://yz.chsi.com.cn/zsml/queryAction.do?pageno=%s' %i
            yield scrapy.Request(url, callback=self.parse)
    
    # def parse(self, response):
    #     self.driver.get(response.url)
    #     url_set = set()
    #     i = 0
    #     while True:
    #         wait = WebDriverWait(self.driver, 3)
    #         wait.until(lambda driver:driver.find_element_by_css_selector('table.ch-table tbody>tr>td:nth-child(1) form a'))
    #         sites = self.driver.find_elements_by_css_selector('table.ch-table tbody>tr>td:nth-child(1) form a')
    #         sites_list = [site.get_attribute('href') for site in sites]
    #         url_set |= set(sites_list)
    #         try:
    #             wait = WebDriverWait(self.driver, 3)
    #             wait.until(lambda driver:driver.find_element_by_css_selector('div.zsml-page-box ul>li:nth-last-child(2):not(.unable)>a'))
    #             # sites = self.driver.find_elements_by_css_selector('table.ch-table tbody>tr>td:nth-child(1) form a')
    #             # sites_list = [site.get_attribute('href') for site in sites]
    #             # url_set |= set(sites_list)
    #             next_page = self.driver.find_element_by_css_selector('div.zsml-page-box ul>li:nth-last-child(2):not(.unable)>a')
    #             next_page.click()
    #             i = i + 1
    #             print '###### 外部页数:%s ######' %i
    #         except:
    #             print '###### 已到达最后一页 ######' %i
    #             break
    #         for url in url_set:
    #             yield scrapy.Request(url, callback=self.parse_item)
    
    def parse(self, response):
        for path in response.css('table.ch-table tbody>tr>td:nth-child(1) form a::attr("href")').extract():
            url = 'http://yz.chsi.com.cn' + path
            yield scrapy.Request(url, callback=self.parse_uni)
        # self.driver.get(response.url)
        # url_set = set()
        # li_length = len(response.css('div.zsml-page-box ul>li'))
        # i = 0
        # while True:
        #     wait = WebDriverWait(self.driver, 5)
        #     wait.until(lambda driver:driver.find_element_by_css_selector('table.ch-table tbody>tr>td:nth-child(7) a'))
        #     sites = self.driver.find_elements_by_css_selector('table.ch-table tbody>tr>td:nth-child(7) a')
        #     sites_list = [site.get_attribute('href') for site in sites]
        #     url_set |= set(sites_list)
        #     try:
        #         wait = WebDriverWait(self.driver, 5)
        #         if li_length <= 8 and li_length > 3:
        #             wait.until(lambda driver:driver.find_element_by_css_selector('div.zsml-page-box ul>li:nth-last-child(1):not(.unable)>a'))
        #             next_page = self.driver.find_element_by_css_selector('div.zsml-page-box ul>li:nth-last-child(1):not(.unable)>a')
        #         elif li_length > 8:
        #             wait.until(lambda driver:driver.find_element_by_css_selector('div.zsml-page-box ul>li:nth-last-child(2):not(.unable)>a'))
        #             next_page = self.driver.find_element_by_css_selector('div.zsml-page-box ul>li:nth-last-child(2):not(.unable)>a')
        #         next_page.click()
        #         i = i + 1
        #         print '###### 内部页数:%s ######' %i
        #     except:
        #         print '###### 已到达最后一页 ######'
        #         break
        #     for url in url_set:
        #         yield scrapy.Request(url, callback=self.parse_detail)
        # sel = Selector(response)
        # details = sel.css('table.ch-table tbody>tr>td:nth-child(7)')
        # domain = 'http://yz.chsi.com.cn'
        # for detail in details:
        #     detail_path = detail.css('a::attr("href")').extract()[0]
        #     cl = domain + detail_path
        #     yield scrapy.Request(cl, callback=self.parse_detail)
    def parse_uni(self, response):
        li_length = len(response.css('div.zsml-page-box ul>li'))
        if li_length > 8:
            total_page = response.css('div.zsml-page-box ul>li:nth-last-child(3) a::text').extract()[0]
        else:
            total_page = response.css('div.zsml-page-box ul>li:nth-last-child(2) a::text').extract()[0]
        for i in range(1, int(total_page.encode('utf-8'))):
            url = response.url + '&pageno=%s' %i
            yield scrapy.Request(url, callback=self.parse_detail)

    def parse_detail(self, response):
        for path in response.css('table.ch-table tbody>tr>td:nth-child(7) a::attr("href")').extract():
            url = 'http://yz.chsi.com.cn' + path
            yield scrapy.Request(url, callback=self.parse_item)
    
    def parse_item(self, response):
        length = len(response.css('div.zsml-result tbody.zsml-res-items td'))
        # items = []
        for sel in response.css('div.zsml-wrapper'):
            for index in range(length):
                item = WebInfoItem()
                item['university'] = sel.css('table.zsml-condition tr:nth-child(1) td.zsml-summary::text').extract()
                item['major'] = sel.css('table.zsml-condition tr:nth-child(3) td.zsml-summary:nth-child(2)::text').extract()
                item['subject'] = sel.css('div.zsml-result tbody.zsml-res-items td')[index].re(r'[^\s\d\(\)=\-/<>a-z\"\:\.]+')
                item['sub_symbol'] = sel.css('div.zsml-result tbody.zsml-res-items td')[index].re(r'\d{3}')
                yield(item)
        #         items.append(item)
        # return items
