from keys import chromedriver_path
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()
options.headless = True

def get_games():
    """Returns an output string of today's NBA games with details and box score hyperlinks from nba.com"""
    output = "*Today's NBA Games*:\n"
    driver = webdriver.Chrome(chromedriver_path, chrome_options=options)  
    driver.get('https://www.nba.com/games')
    cookies_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[3]/div[3]/div/div/div[2]/div/div/button')))
    cookies_button.click()
    div = driver.find_elements_by_xpath('//a[@class="flex-1 px-2 pt-5 h-full block hover:no-underline relative text-sm pt-5 pb-4 mb-1 px-2"]')
    for i in div:
        text = (i.get_attribute('innerText'))
        box_score_url = i.get_attribute('href')
        processing = text.split()
        print(processing)
        if len(processing) == 10: #Game is live
            output += "[{} vs {}]({}): {}-{} ({})\n".format(processing[0],processing[-2],box_score_url,processing[2],processing[-3],processing[4])
        if len(processing) == 7: #Game is over
            output += "[{} vs {}]({}): {}-{} ({})\n".format(processing[0],processing[-2],box_score_url,processing[2],processing[-3],processing[3])
        if len(processing) == 6: #Game has not started
            output += "[{} vs {}]({}): {}\n".format(processing[0],processing[-2],box_score_url, processing[2])
    print(output)
    driver.close()
    return output

def get_news():
    base_url = 'https://basketball.realgm.com'
    news = 'https://basketball.realgm.com/nba/news'
    page = requests.get(news)
    soup = BeautifulSoup(page.content, 'html.parser')
    articles = soup.find_all('a',attrs={'class':'article-title'},href=True, limit=10)
    output = ''
    for article in articles:
        output += '[{}]({})\n\n'.format(article.text, base_url+article['href'])
    output += '[{}]({})'.format('Click Here for More NBA News',base_url)
    print(output)
    return output