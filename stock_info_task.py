from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup , NavigableString
import requests

url = 'https://in.tradingview.com/symbols/NSE-TCS/'

def remove_extra(itration):
    return list(filter(lambda x: type(x) != NavigableString, itration))

def TCS_info(TCS_page):
    print('Stock Name:-' ,TCS_page.find('h1', {'class': 'apply-overflow-tooltip title-HFnhSVZy'}).getText())
    print('Stock Price:-' ,TCS_page.find('span', {'class': 'last-JWoJqCpY js-symbol-last'}).find('span').getText())
    



if __name__ == '__main__':
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_load_state('networkidle')
        page.evaluate('()=> window.scroll(1 ,document.body.scrollHeight)')
        page.screenshot(path='IT_stock.png', full_page=True)
        page_data = page.inner_html('body')
        bSoup = BeautifulSoup(page_data, 'html.parser')
        
        TCS_info(bSoup)

        # print(bSoup.find('div' , attrs={'class' : 'apply-overflow-tooltip value-GgmpMpKr'}))
        
        

        
