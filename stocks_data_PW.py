from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup , NavigableString
import pandas as pd

url = 'https://in.tradingview.com/markets/stocks-india/sectorandindustry-industry/information-technology-services/'

def removeExtra(iteration):
    return list(filter(lambda x: type(x) != NavigableString, iteration))

def getLinks(stockPage):
    stockData = stockPage.find('tbody').find_all('tr')
    link_extensions = [st.find('a').attrs['href'] for st in stockData]
    return link_extensions

def stock_scrap(new_page):
    Stock_Name = new_page.find('h1', {'class': 'apply-overflow-tooltip title-HFnhSVZy'}).getText()
    return {'Stock_Name': Stock_Name}

if __name__ == '__main__':
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url)

        page.wait_for_load_state('networkidle')
        page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
        page.screenshot(path='IT_stock.png', full_page=True)

        pageData = page.inner_html('body')
        bSoup = BeautifulSoup(pageData, 'html.parser')

        link_list = getLinks(bSoup)
        parent_URL = 'https://in.tradingview.com'
        stock_links = [parent_URL + extension for extension in link_list]

        stock_details = []

        for link in stock_links[0:2]:
            new_page = browser.new_page()
            new_page.goto(link)
            new_page.wait_for_load_state('networkidle')
            
            stock_data = stock_scrap(new_page)
            stock_details.append(stock_data)

            print(stock_details)
            
            new_page.close()

        

        
