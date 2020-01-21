import scrapy

#from secretcv.items import SecretcvItem
from jobscraping.items import JobscrapingItem

class SecretCvSpider(scrapy.Spider):
    # name changed as project name secretcv
    name = 'jobscraping'
    allowed_domains = ['cv-library.co.uk']
    start_urls = ['https://www.cv-library.co.uk/search-jobs?category=&distance=15&geo=SW18+4GD&industry=&offset=0&order=&perpage=250&posted=7&q=Data+Engineer&salarymax=&salarymin=&salarytype=annum&tempperm=Contract']
    

    def parse(self, response):
        
        # basic query
        query = '//*[@id="searchResults"]/li/article[contains(@id, "jobsearchresult")]'
        #query = '//*[contains(@class,"results__item")]'

        for result in response.xpath(query):
            
            # JobscrapingItem object intentiates
            item = JobscrapingItem()
            
            # Detail queries
            item['job_id'] = result.xpath('*/h2/a/@data-job-id').get()
            item['job_title'] = result.xpath('*/h2/a/@data-job-title').get()
            #item['salary'] = result.css('dd.job__details-value.salary::text').extract()[0]
            item['job_type'] = result.css('dd[class = "job__details-value"]::text').extract()[0]
            #item['location'] = result.css('dd.job__details-value.location > span::text').extract()[0].strip()
            #item['url'] = result.xpath('.//a[@class="job-url"]/@href').get()
            link = item['url'] = 'https://www.cv-library.co.uk'+result.xpath('*/h2/a/@href').get()
            
            
            # Scraping each job page
            request = scrapy.Request(link,callback = self.job_parse)
            request.meta['item'] = item
            yield request
            
            
    def job_parse (self,response):
        item =  response.meta['item']
        item['job_salary'] = response.css('dd.job__details-value::text').extract()[1]
        #item['job_type'] = response.xpath('//*[@id="site-main"]/div/div[1]/div/article/div/div[1]/p[5]').get()
        #item['contact_name'] = response.xpath().get()
        #item['mail'] = response.xpath().get()
        #item['tel'] = response.xpath().get()
        item['agency'] = response.css('dd.job__details-value > a::text').extract()[0]
        item['location'] = response.css('dd.job__details-value::text').extract()[0]
        item['job_lenght'] = response.css('dd.job__details-value::text').extract()[6]
        item['job_refid'] = response.css('dd.job__details-value::text').extract()[9]
        #item['description'] = response.xpath('string(//*[@id="cv960"]/div[2]/div[1]/div[1]/div[2]/div[3]//*)').extract()
        
        return item
        
