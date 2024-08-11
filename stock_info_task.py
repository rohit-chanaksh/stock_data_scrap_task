from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup , NavigableString
import requests

url = 'https://in.tradingview.com/symbols/NSE-TCS/'

def remove_extra(itration):
    return list(filter(lambda x: type(x) != NavigableString, itration))

def TCS_info(TCS_page):
    print('Stock Name:-' ,TCS_page.find('h1', {'class': 'apply-overflow-tooltip title-HFnhSVZy'}).getText())
    print('Stock Price:-' ,TCS_page.find('span', {'class': 'last-JWoJqCpY js-symbol-last'}).find('span').getText())
    print('Market Capitalization :- ', TCS_page.find('div', {'data-container-name': 'key-stats-id'}).find('div', {'class': 'content-JhZ1X2FK'}).find('div', {'class': 'apply-overflow-tooltip value-GgmpMpKr'}).getText())
    key_stat_list = TCS_page.find('div', {'data-container-name': 'key-stats-id'}).find_all('div' , {'class': 'block-GgmpMpKr container-lQwbiR8R'} )
    # print(len(key_stat_list))
    print('Dividend yield (indicated) :-' , key_stat_list[1].find('div', {'class': 'apply-overflow-tooltip value-GgmpMpKr'}).getText())
    print('Price to earnings Ratio (TTM):-' , key_stat_list[2].find('div', {'class': 'apply-overflow-tooltip value-GgmpMpKr'}).getText())
    print('Basic EPS (TTM):-' , key_stat_list[3].find('div', {'class': 'apply-overflow-tooltip value-GgmpMpKr'}).getText())
    print('Net income (FY):-' , key_stat_list[4].find('div', {'class': 'apply-overflow-tooltip value-GgmpMpKr'}).getText())
    print('Revenue (FY):-' , key_stat_list[5].find('div', {'class': 'apply-overflow-tooltip value-GgmpMpKr'}).getText())
    print('Shares float:-' , key_stat_list[6].find('div', {'class': 'apply-overflow-tooltip value-GgmpMpKr'}).getText())
    print('Beta (1Y):-' , key_stat_list[7].find('div', {'class': 'apply-overflow-tooltip value-GgmpMpKr'}).getText())



if __name__ == '__main__':
    with sync_playwright() as p:
        browser = p.chromium.launch(headless= True)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_load_state('networkidle')
        page.evaluate('()=> window.scroll(1 ,document.body.scrollHeight)')
        page.screenshot(path='IT_stock.png', full_page=True)
        page_data = page.inner_html('body')
        bSoup = BeautifulSoup(page_data, 'html.parser')
        
        TCS_info(bSoup)

        # print(bSoup.find('div' , attrs={'class' : 'apply-overflow-tooltip value-GgmpMpKr'}))
        
        

        
