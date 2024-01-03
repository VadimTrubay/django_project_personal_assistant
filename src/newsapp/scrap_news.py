import requests
from bs4 import BeautifulSoup
import time
import random
delay = random.uniform(1, 4)

Data = []
def news_war():
    global Data
    url = "https://www.bbc.com/news/world-60525350"
    req = requests.get(url, headers={'User-Agent': 'V'})
    soup = BeautifulSoup(req.content, 'html.parser')
   
    result1 = soup.find_all(
        'a', class_="gs-c-promo-heading gs-o-faux-block-link__overlay-link gel-pica-bold nw-o-link-split__anchor", attrs={'class': 'href'})
    
    data = [{'href': f'https://www.bbc.com{link["href"]}', 'title': link.text} for link in result1]
    time.sleep(delay)
    
    Data = data[0:6]

   
    return Data
    
    
def news_business():
    global Data
    url = "https://www.bbc.com/news/business"
    req = requests.get(url, headers={'User-Agent': 'V'})
    soup = BeautifulSoup(req.content, 'html.parser')
   
    result = soup.find_all(
        'a', class_="gs-c-promo-heading gs-o-faux-block-link__overlay-link gel-pica-bold nw-o-link-split__anchor", attrs={'class': 'href'}) 
    data = [{'href': f'https://www.bbc.com{link["href"]}', 'title': link.text} for link in result]
    time.sleep(delay)
    Data = data[0:6]
  
    return Data


def news_since():
    global Data
    url = "https://www.bbc.com/news/science_and_environment"
    req = requests.get(url, headers={'User-Agent': 'V'})
    soup = BeautifulSoup(req.content, 'html.parser')
   
    result = soup.find_all(
        'a', class_="gs-c-promo-heading gs-o-faux-block-link__overlay-link gel-pica-bold nw-o-link-split__anchor", attrs={'class': 'href'}) 
    data = [{'href': f'https://www.bbc.com{link["href"]}', 'title': link.text} for link in result]
    time.sleep(delay)
    Data = data[0:6] 
 
    return Data


def news_sport():
    # global Data
    url = "https://www.bbc.com/sport"
    req = requests.get(url, headers={'User-Agent': 'V'})
    soup = BeautifulSoup(req.content, 'html.parser')
   
    # result = soup.find_all(
    #     'div', class_='ssrcss-2zuha1-NoTitlePadding eqfxz1e3', attrs={'class': 'href'}) 
    # data = [{'href': f'https://www.bbc.com{link["href"]}', 'title': link.text} for link in result]
    # time.sleep(delay)
    # Data = data[0:10]

    return Data
    



def parse_page(string:str):
    link = ''
    img_src = ''

    for i in Data:
        
        if i['title'] == string:
            link = i['href']
    

    url = link
    req = requests.get(url, headers={'User-Agent': 'V'})
    print(f"REQUEST:: : : : :  {req.text}")
    soup = BeautifulSoup(req.content, 'html.parser')
   
    result = soup.find('h1')
    time.sleep(delay)
    title = result.text

    
    img_tag = soup.find('img')

    if img_tag:
       
        img_src = img_tag.get('src')

    div_element = soup.find_all(
        'p', class_='ssrcss-1q0x1qg-Paragraph')
    
    text_list = [p_element.text for p_element in div_element]

    text = '\n'.join(text_list)
    text = text.replace('© 2023 BBC. The BBC is not responsible for the content of external sites. Read about our approach to external linking.', '')

    return title, text, img_src

news_sport()