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
        query = '//*[@id="search-results-jobs"]/*[contains(@class,"job-search-result-row job_description_")]'

        for result in response.xpath(query):
            
            # JobscrapingItem object intentiates
            item = JobscrapingItem()
            
            # Detail queries
            item['job_id'] = result.xpath('@data-job-id').get()
            item['job_title'] = result.xpath('@data-job-title').get()
            item['salary'] = result.xpath('.//div[@id="js-salary-details"]/text()').get()
            #item['url'] = result.xpath('.//a[@class="job-url"]/@href').get()
            link = item['url'] = 'https://www.cv-library.co.uk'+result.xpath('.//div[2]/*/p/a/@href').get()

            # Scraping each job page
            request = scrapy.Request(link,callback = self.job_parse)
            request.meta['item'] = item
            yield request
            break
    
    def job_parse (self,response):
        item =  response.meta['item']
        item['job_salary'] = response.xpath('//*[@id="job-salary"]/text()').get()
        item['job_type'] = response.xpath('//*[@id="cv960"]/div[2]/div[1]/div[1]/div[2]/div[5]/text()').get()
        #item['contact_name'] = response.xpath().get()
        #item['mail'] = response.xpath().get()
        #item['tel'] = response.xpath().get()
        item['agency'] = response.xpath('//*[@id="js-company-details"]/a/text()').get()
        item['location'] = response.xpath('//*[@id="job-location"]/text()').get()
        item['description'] = response.xpath('string(//*[@id="cv960"]/div[2]/div[1]/div[1]/div[2]/div[3]//*)').extract()
        
        return item
        
