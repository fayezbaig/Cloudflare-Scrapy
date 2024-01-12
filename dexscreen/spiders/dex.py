import scrapy
from scrapy.http import Request
from selenium import webdriver
from ..items import DexscreenItem
from urllib.parse import urlencode, quote

def get_zenrows_api_url(url, api_key):
    # Creates a ZenRows proxy URL for a given target_URL using the provided API key.
    payload = {
        'url': url,
        'js_render': 'true',
        'antibot': 'true',
        'premium_proxy': 'true',
    }

    #     # Construct the API URL by appending the encoded payload to the base URL with the API key


    api_url = f'https://api.zenrows.com/v1/?apikey={api_key}&{urlencode(payload)}'
    return api_url
    

class DexSpider(scrapy.Spider):
    name = "dex"
    allowed_domains = ["quotes.toscrape.com","dexscreener.com","api.zenrows.com","api.scraperapi.com"]

    headers = {
        "x-asbd-id": 198387,
        "x-csrftoken": "gqeYY9dr1dCwfvtyZCgy88tcMn1A2N85",
        "x-ig-app-id": 936619743392459,
        "x-requested-with": "XMLHttpRequest"
    }

    def start_requests(self):
        urls = [
            'https://dexscreener.com/?rankBy=trendingScoreH6&order=desc&minLiq=1000&minFdv=15000&maxFdv=100000&minAge=720&maxAge=8640',
        ]
        api_key = '861e2123580f76559d5d80107dbd20c13acdde8f'
        for url in urls:
            # make a GET request using the ZenRows API URL
            api_url = get_zenrows_api_url(url, api_key)
            yield scrapy.Request(api_url, callback=self.parse)


    def parse(self, response):
        
        table_page = response.css('div.ds-dex-table.ds-dex-table-top a.ds-dex-table-row.ds-dex-table-row-top')

        for element in table_page:

            base_url = 'https://dexscreener.com'

            end_point = element.css('::attr(href)').get()
            print(end_point)

            api_key = '861e2123580f76559d5d80107dbd20c13acdde8f'

            # api_url = get_zenrows_api_url(end_point, api_key)

            full_link = response.urljoin(base_url + end_point)

            api_url = get_zenrows_api_url(full_link, api_key)

            if element.css('div.ds-table-data-cell.ds-dex-table-row-col-price span.chakra-text.custom-0'):

                yield scrapy.Request(api_url, callback = self.parse_detail
                                      ,meta = { 
                    'token': element.css('div.ds-table-data-cell.ds-dex-table-row-col-token span.ds-dex-table-row-base-token-symbol::text').get(),
                    'name': element.css('div.ds-table-data-cell.ds-dex-table-row-col-token span.ds-dex-table-row-base-token-name::text').get(),
                    'TRNC': element.css('div.ds-table-data-cell::text').extract()[0],
                    'Volume': element.css('div.ds-table-data-cell::text').extract()[2],
                    'Liquidity': element.css('div.ds-table-data-cell::text').extract()[5],
                    'FDV': element.css('div.ds-table-data-cell::text').extract()[7],
                    'Link' : full_link,
                    'response':response
                    }
                )
                print("********break*******")
                
            else:
                yield scrapy.Request(api_url,callback = self.parse_detail
                                      , meta ={
                    'token': element.css('div.ds-table-data-cell.ds-dex-table-row-col-token span.ds-dex-table-row-base-token-symbol::text').get(),
                    'name': element.css('div.ds-table-data-cell.ds-dex-table-row-col-token span.ds-dex-table-row-base-token-name::text').get(),
                    'TRNC': element.css('div.ds-table-data-cell::text').extract()[2],
                    'Volume': element.css('div.ds-table-data-cell::text').extract()[4],
                    'Liquidity': element.css('div.ds-table-data-cell::text').extract()[7],
                    'FDV': element.css('div.ds-table-data-cell::text').extract()[9],
                    'Link' : full_link,
                    'response':response
                                      })
                               
                
        print('***********end*********')
        # chrome.quit()

    def parse_detail(self,response):

        item = DexscreenItem()

        response2 = response.meta.get('response',response)

        item['token'] = response.meta.get('token')
        item['name'] = response.meta.get('name')
        item['TRNC'] = response.meta.get('TRNC')
        item['Volume'] = response.meta.get('Volume')
        item['Liquidity'] = response.meta.get('Liquidity')
        item['FDV'] = response.meta.get('FDV')
        item['Link'] = response.meta.get('Link')
        item['chain'] = response.css('div.chakra-wrap.custom-1el71j0 a.chakra-link.chakra-wrap__listitem.custom-gbqtda::text').get()

        
    
        yield item

    
        



'''Place this code after def parse'''

         # chrome = Chrome()

        # chrome.execute_script("window.open('https://dexscreener.com/?rankBy=trendingScoreH6&order=desc&minLiq=1000&minFdv=15000&maxFdv=100000&minAge=720&maxAge=8640', '_blank')")
        # time.sleep(15)
        # chrome.switch_to.window(chrome.window_handles[1])
        
       
        # chrome.implicitly_wait(10)

        # time.sleep(5)

        # page_source = chrome.page_source

        # time.sleep(10)

        # response = scrapy.http.HtmlResponse(url=response.url, body=page_source, encoding='utf-8')

        # time.sleep(5)
