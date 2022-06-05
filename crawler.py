from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.common.exceptions import InvalidArgumentException
from bs4 import BeautifulSoup
#imports
import pandas as pd
from datetime import datetime

driver = webdriver.Chrome(ChromeDriverManager().install())

def extract_tags():
    """"""
    try:
        driver.get('https://blog.dauphin.com/')
        sleep(5)
            
    except InvalidArgumentException:
        print('Invalid URL')
        exit()

    src = driver.page_source
    soup = BeautifulSoup(src,'lxml')
    wrapper = soup.find('main',{'class':'body-container-wrapper'})
    tags = wrapper.find_all('a',{'class':'blog-tags__link'})

    links=[]
    for tag in tags:
        links.append(tag['href'])

    return(links)

def extract_information():
    """"""
    article_titles=[]
    article_resume =[]
    article_tags=[]
    article_links=[]
    article_dates=[]
    
    try:
        for link in extract_tags()[1:]:
            driver.get(link)
            sleep(2)
            
            src = driver.page_source
            soup = BeautifulSoup(src,'lxml')
            wrapper = soup.find('main',{'class':'body-container-wrapper'})
            titles = wrapper.find_all('a',{'class':None}) #titles
            resume = wrapper.find_all('p',{'class':None}) #Resumen
            
            for i in range(len(titles)):
                tag = link.split('/')[-1].replace('-', ' ')
                article_tags.append(tag) #tags
            dates = wrapper.find_all('span',{'class':'blog-index__post-date'}) #dates
            
            for (title, date, resume_) in zip(titles, dates, resume):
                article_titles.append(title.get_text())
                article_links.append(title['href'])
                date_ = date.get_text().strip()
                date_obj = datetime.strptime(date_, '%b %d, %Y')
                date_formmatted = date_obj.strftime('%Y-%m-%d')
                article_dates.append(date_formmatted)
                article_resume.append(resume_.get_text())
            
    except InvalidArgumentException:
        print('Invalid URL')
        exit()
        
    driver.close()  
    return(article_dates, article_titles, article_resume, article_tags, article_links)

info = extract_information()

info_data = {
    "id_": [i for i in range(len(info[1]))],
    "Date": info[0],
    "Title": info[1],
    "Resume": info[2],
    "Tag": info[3],
    "Link": info[4],
}

df = pd.DataFrame(info_data)
df.to_csv('valores.csv', index=False)

