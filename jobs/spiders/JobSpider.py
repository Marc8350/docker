import scrapy
import datetime
import logging
import time
import os 
class JobSpider(scrapy.Spider):
    name = "test"
    allowed_domains = ["make-it-in-germany.com"]
    start_urls = [f"https://www.make-it-in-germany.com/en/working-in-germany/job-listings?tx_solr%5Bfilter%5D%5B0%5D=region%3A1&tx_solr%5Bfilter%5D%5B1%5D=timelimit%3A2&tx_solr%5Bfilter%5D%5B2%5D=workingplan%3A1&tx_solr%5Bpage%5D={i}&tx_solr%5Bq%5D=#list45536" for i in range(1, 10)]
    today = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d')
    log_dir = "jobs/logs"
    log_file = os.path.join(log_dir, f"{today}.log")
    custom_settings = {'LOG_LEVEL': 'INFO', 'LOG_FILE': log_file}

    def parse(self, response):
        # Check if this is the first page
        urls = response.xpath('//*[@id="tx-solr-search"]/ul').css("a::attr(href)").getall()
        filtered_urls = [url for url in urls if "job-listings" in url]
        yield from response.follow_all(filtered_urls, self.parse_job)


    def parse_job(self, response):
        crawl_ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        job_title = response.css('#main > div:nth-child(4) > article > article.detail-page__overview.overview--job.overview.bg--overflow > header > h1::text').get()
        company = response.css('#main > div:nth-child(4) > article > article.detail-page__overview.overview--job.overview.bg--overflow > header > h1::text').get()
        job_description = ''.join([x.get().strip() for x in response.xpath('//*[@id="main"]/div[4]/article/article[2]/p/text()')])
        working_hours = response.xpath('//*[@id="main"]/div[4]/article/article[1]/div/ul/li[1]/span').get().replace('<span class="element"> <strong> Working hours: </strong> ', "").replace(" </span>", "")
        work_place = response.xpath('//*[@id="main"]/div[4]/article/article[1]/div/ul/li[2]/span').get().replace('<span class="element"> <strong>Workplace:</strong> ', '').replace(' </span>', '')
        type_of_employment = response.xpath('//*[@id="main"]/div[4]/article/article[1]/div/ul/li[4]/span').get().replace('<span class="element"> <strong>Type of employment contract:</strong> ', '').replace(' </span>', '')
        company_size = response.xpath('//*[@id="main"]/div[4]/article/article[1]/div/ul/li[3]/span').get().replace('<span class="element"> <strong>Company size:</strong> ', '').replace(' </span>', '')
        contact_person = response.xpath('//*[@id="main"]/div[4]/article/aside[2]/div/p[2]').get()
        if contact_person is not None:
            contact_person = contact_person.replace('<p> <strong>Contact person:</strong><br> ', '').replace('<br> </p>', '')
            contact_person_email = response.css('#main > div:nth-child(4) > article > aside.detail-page__additional.detail-page__additional--row-position.additional > div > p:nth-child(3) > a::text').get()
            contact_person_phone = response.css("#main > div:nth-child(4) > article > aside.detail-page__additional.detail-page__additional--row-position.additional > div > address > p:nth-child(3) > a::text").get()
            contact_person_adress = response.xpath('//*[@id="main"]/div[4]/article/aside[2]/div/address/p[2]').get().replace('<p class="additional__item"> ','').replace('<br>', '').replace('</p>', '')
        else:
            contact_person = ""
            contact_person_email = ""
            contact_person_phone = ""
            contact_person_adress = ""
            logging.info("No contact person found")
        website = response.css("#main > div:nth-child(4) > article > aside.detail-page__additional.detail-page__additional--row-position.additional > div > address > p:nth-child(4) > a::text").get()
        logging.info(f"Scraped job: {job_title} from {company} at {crawl_ts}")
        yield {
            "job_title": job_title,
            "company": company,
            "job_description": job_description,
            "working_hours": working_hours,
            "work_place": work_place,
            "type_of_employment": type_of_employment,
            "company_size": company_size,
            "contact_person": contact_person,
            "contact_person_email": contact_person_email,
            "contact_person_phone": contact_person_phone,
            "contact_person_adress": contact_person_adress,
            "website": website,
            "crawl_ts": crawl_ts
        }
