from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup , NavigableString

import requests as rq

#selectox

url = 'https://in.tradingview.com/markets/stocks-india/sectorandindustry-industry/information-technology-services/'

def removeExtra(itration):
    return list(filter(lambda x: type(x) != NavigableString, itration))
 

def getLinks(stockPage) :
    # print(stockPage.find_all('tbody'))   # checking
    # print(stockPage.find('tbody').find_all('tr' , attrs= {'data-rowkey' : 'NSE:TCS'}))  # checking
    stockData = stockPage.find('tbody').find_all('tr')
    link_extensions = [ st.find('a').attrs['href'] for st in stockData]
    return link_extensions


 


if __name__ == '__main__' :
    with sync_playwright() as p :
        browser = p.chromium.launch(headless=True )

        page = browser.new_page()
        page.goto(url)

        page.wait_for_load_state('networkidle')
        page.evaluate('()=> window.scroll(1 ,document.body.scrollHeight)')
        page.screenshot(path='IT_stock.png' , full_page=True)

        pageData = page.inner_html('body')

        bSoup = BeautifulSoup(pageData , 'html.parser')
        # print(bSoup)

        link_list = getLinks(bSoup)
        # print(link_list)

        parent_URL = 'https://in.tradingview.com'

        stock_links = [ parent_URL + extension  for extension in link_list]
        print(stock_links)

    
for link in stock_links :
    sl_resp = rq.get(link)
    print(sl_resp.status_code)
    





