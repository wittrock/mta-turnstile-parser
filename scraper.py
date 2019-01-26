import requests
import scrapy
import time

url_xpath = '//*[@id="contentbox"]/div/div/a/@href'

base_url = 'http://web.mta.info/developers'
list_url = base_url + '/turnstile.html'
print('Making request to {}'.format(list_url))
resp = requests.get(list_url)
print('Got response: {}'.format(resp.status_code))
urls = scrapy.Selector(text=resp.text).xpath(url_xpath).extract()

print('Got {} urls'.format(len(urls)))

for url in urls:
    req_url = base_url + '/' + url
    filename = req_url.split('/')[-1]
    print('Retrieving {}'.format(req_url))
    data_resp = requests.get(base_url + '/' + url)
    if not data_resp.ok:
        print('Could not retrieve {}'.format(req_url))
        continue
    with open('./data/' + filename, 'w') as f:
        f.write(data_resp.text)
    time.sleep(1)
