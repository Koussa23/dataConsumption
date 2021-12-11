import scrapy
from scrapy.http import FormRequest
from ..items import DataconsumptionItem
import pandas as pd


class DataconsumptionspiderSpider(scrapy.Spider):
    name = 'dataConsumptionSpider'
    allowed_domains = ['bcd-bbn.com']
    start_urls = ['http://www.bcd-bbn.com/signin.php']

    def parse(self, response):
        return FormRequest.from_response(response, formdata={
            'username': 'marwanko',
            'password': 'Marwanek1959'
        }, callback=self.start_scraping)

    def start_scraping(self, response):
        items = DataconsumptionItem()
        df = pd.DataFrame()
        dates = []
        totals = []
        uploads = []
        downloads = []

        # Scraping
        table = response.xpath("//div[2]/div[4]//tr")
        for entry in table:
            t_date = entry.xpath("td[1]/text()").extract()
            t_total = entry.xpath("td[2]/text()").extract()
            t_upload = entry.xpath("td[3]/text()").extract()
            t_download = entry.xpath("td[4]/text()").extract()
            dates.append(t_date)
            totals.append(t_total)
            uploads.append(t_upload)
            downloads.append(t_download)

        upload = response.xpath(
            "//div/div[4]//tfoot/tr/th[3]/text()").extract()
        download = response.xpath(
            "//div/div[4]//tfoot/tr/th[4]/text()").extract()
        date = response.xpath("//div[2]/div[3]/strong[2]/text()").extract()

        # Processing
        df['Date'] = dates
        df['Downloads'] = downloads
        df['Uploads'] = uploads
        df['Totals'] = totals

        date = date[0]

        download = download[0]
        download = download.replace('MB', '')
        download = round((float(download.replace(',', '')) / 1000), 2)

        upload = upload[0]
        upload = upload.replace('MB', '')
        upload = round((float(upload.replace(',', '')) / 1000), 2)

        total = round((download + upload), 2)
        dl_pct = round(((download / total) * 100), 2)
        ul_pct = round((100 - dl_pct), 2)
        remaining = round((1000 - total), 2)

        remaining_pct = round((remaining / (total + remaining) * 100), 2)

        # Output
        items['total'] = total
        items['upload'] = upload
        items['download'] = download
        items['remaining'] = remaining
        items['dl_pct'] = dl_pct
        items['ul_pct'] = ul_pct

        print(df)
        print('Date:', date)
        print('Download: ' + str(download) + ' GB')
        print('Upload: ' + str(upload) + ' GB')
        print('Total: ' + str(total) + ' GB')
        print('Remaining: ' + str(remaining) + ' GB\n' +
              '% Remaining: ' + str(remaining_pct) + ' %')
        print('DL % of total: ' + str(dl_pct) + ' %')
        print('UL % of total: ' + str(ul_pct) + ' %')        

