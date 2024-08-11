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

def stock_scrap(new_page):
    new_pageData = new_page.inner_html('body')
    # print(new_pageData)  # checking
    bSoup2 = BeautifulSoup(new_pageData , 'html.parser')
    # print(bSoup2.prettify())  # checking


    Stock_Name = bSoup2.find('h1', {'class': 'apply-overflow-tooltip title-HFnhSVZy'}).getText()
    Stock_Price = bSoup2.find('span', {'class': 'last-JWoJqCpY js-symbol-last'}).find('span').getText()

    Market_Capitalization = bSoup2.find('div', {'data-container-name': 'key-stats-id'}).find('div', {'class': 'content-JhZ1X2FK'}).find('div', {'class': 'apply-overflow-tooltip value-GgmpMpKr'}).getText()
    key_stat_list = bSoup2.find('div', {'data-container-name': 'key-stats-id'}).find_all('div' , {'class': 'block-GgmpMpKr container-lQwbiR8R'} )
    # print(len(key_stat_list))
    Dividend_yield_indicated =  key_stat_list[1].find('div', {'class': 'apply-overflow-tooltip value-GgmpMpKr'}).getText()
    Price_to_earnings_Ratio_TTM =  key_stat_list[2].find('div', {'class': 'apply-overflow-tooltip value-GgmpMpKr'}).getText()
    Basic_EPS_TTM =  key_stat_list[3].find('div', {'class': 'apply-overflow-tooltip value-GgmpMpKr'}).getText()
    Net_income_FY =  key_stat_list[4].find('div', {'class': 'apply-overflow-tooltip value-GgmpMpKr'}).getText()
    Revenue_FY =  key_stat_list[5].find('div', {'class': 'apply-overflow-tooltip value-GgmpMpKr'}).getText()
    Shares_float=  key_stat_list[6].find('div', {'class': 'apply-overflow-tooltip value-GgmpMpKr'}).getText()
    Beta_1Y =  key_stat_list[7].find('div', {'class': 'apply-overflow-tooltip value-GgmpMpKr'}).getText()



    # print('Stock Name:-' ,bSoup2.find('h1', {'class': 'apply-overflow-tooltip title-HFnhSVZy'}).getText())
    # print('Stock Price:-' ,bSoup2.find('span', {'class': 'last-JWoJqCpY js-symbol-last'}).find('span').getText())
    # print('Market Capitalization :- ', bSoup2.find('div', {'data-container-name': 'key-stats-id'}).find('div', {'class': 'content-JhZ1X2FK'}).find('div', {'class': 'apply-overflow-tooltip value-GgmpMpKr'}).getText())
    # key_stat_list = bSoup2.find('div', {'data-container-name': 'key-stats-id'}).find_all('div' , {'class': 'block-GgmpMpKr container-lQwbiR8R'} )
    # # print(len(key_stat_list))
    # print('Dividend yield (indicated) :-' , key_stat_list[1].find('div', {'class': 'apply-overflow-tooltip value-GgmpMpKr'}).getText())
    # print('Price to earnings Ratio (TTM):-' , key_stat_list[2].find('div', {'class': 'apply-overflow-tooltip value-GgmpMpKr'}).getText())
    # print('Basic EPS (TTM):-' , key_stat_list[3].find('div', {'class': 'apply-overflow-tooltip value-GgmpMpKr'}).getText())
    # print('Net income (FY):-' , key_stat_list[4].find('div', {'class': 'apply-overflow-tooltip value-GgmpMpKr'}).getText())
    # print('Revenue (FY):-' , key_stat_list[5].find('div', {'class': 'apply-overflow-tooltip value-GgmpMpKr'}).getText())
    # print('Shares float:-' , key_stat_list[6].find('div', {'class': 'apply-overflow-tooltip value-GgmpMpKr'}).getText())
    # print('Beta (1Y):-' , key_stat_list[7].find('div', {'class': 'apply-overflow-tooltip value-GgmpMpKr'}).getText())

    # print('/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////')
    
    # print(Stock_Name)
    # print(Stock_Price)

    return {
        'Stock_Name': Stock_Name ,
        'Stock_Price' : Stock_Price,
        'Market_Capitalization': Market_Capitalization ,
        'Dividend_yield_indicated' : Dividend_yield_indicated,
        'Price_to_earnings_Ratio_TTM': Price_to_earnings_Ratio_TTM,
        'Basic_EPS_TTM' : Basic_EPS_TTM ,
        'Net_income_FY' : Net_income_FY ,
        'Revenue_FY' : Revenue_FY ,
        'Shares_float' : Shares_float ,
        'Beta_1Y' : Beta_1Y 
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
            new_page = browser.new_page()
            new_page.goto(link)
            new_page.wait_for_load_state('networkidle')
            
            stock_data = stock_scrap(new_page)
            stock_details.append(stock_data)
            
            new_page.close()

        print(stock_details)


        

        
