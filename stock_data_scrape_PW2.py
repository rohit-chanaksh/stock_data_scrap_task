from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup , NavigableString
# import pandas as pd

url = 'https://in.tradingview.com/markets/stocks-india/sectorandindustry-industry/information-technology-services/'

def removeExtra(iteration):
    return list(filter(lambda x: type(x) != NavigableString, iteration))


def getLinks(stockPage):
    stockData = stockPage.find('tbody').find_all('tr')
    link_extensions = [st.find('a').attrs['href'] for st in stockData]
    return link_extensions


def stock_scrap(pageData):
    bSoup2 = BeautifulSoup(pageData , 'html.parser')

    key_stat_list = bSoup2.find('div', {'data-container-name': 'key-stats-id'}).find_all('div' , {'class': 'block-GgmpMpKr container-lQwbiR8R'} )
    
    return {
        'Stock_Name': bSoup2.find('h1', {'class': 'apply-overflow-tooltip title-HFnhSVZy'}).getText() ,
        'Stock_Price' : bSoup2.find('span', {'class': 'last-JWoJqCpY js-symbol-last'}).find('span').getText(),
        'Market_Capitalization': bSoup2.find('div', {'data-container-name': 'key-stats-id'}).find('div', {'class': 'content-JhZ1X2FK'}).find('div', {'class': 'apply-overflow-tooltip value-GgmpMpKr'}).getText().strip() ,
        'Dividend_yield_indicated' : key_stat_list[1].find('div', {'class': 'apply-overflow-tooltip value-GgmpMpKr'}).getText(),
        'Price_to_earnings_Ratio_TTM': key_stat_list[2].find('div', {'class': 'apply-overflow-tooltip value-GgmpMpKr'}).getText(),
        'Basic_EPS_TTM' : key_stat_list[3].find('div', {'class': 'apply-overflow-tooltip value-GgmpMpKr'}).getText() ,
        'Net_income_FY' : key_stat_list[4].find('div', {'class': 'apply-overflow-tooltip value-GgmpMpKr'}).getText() ,
        'Revenue_FY' : key_stat_list[5].find('div', {'class': 'apply-overflow-tooltip value-GgmpMpKr'}).getText() ,
        'Shares_float' : key_stat_list[6].find('div', {'class': 'apply-overflow-tooltip value-GgmpMpKr'}).getText().strip() ,
        'Beta_1Y' : key_stat_list[7].find('div', {'class': 'apply-overflow-tooltip value-GgmpMpKr'}).getText()
        }



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
        # print(bSoup)

        link_list = getLinks(bSoup)

        parent_URL = 'https://in.tradingview.com'

        stock_links = [parent_URL + extension for extension in link_list]

        # print(stock_links)

        stock_details = []

        for link in stock_links[0:2]:
            page.goto(link)
            page.wait_for_load_state('networkidle')
            pageData = page.inner_html('body')

            stock_data = stock_scrap(pageData)
            stock_details.append(stock_data)
            
        page.close()

        print(stock_details)


        

        
