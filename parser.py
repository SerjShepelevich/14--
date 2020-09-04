from bs4 import BeautifulSoup
import requests
import re
import pprint
import pandas as pd

URL = 'https://www.drom.ru/reviews/toyota/prius/5kopeek/'

def num_elements(soup,type_, name_):
    reviews = soup.find_all(type_, class_= name_)
    if len(reviews) > 0:
        return reviews
    else:
        return 0

def text_data(danniie_):
    if danniie_ != 0:
        return danniie_[0].text
    else:
        return ''

def grab_rev_from_page(page_URL):
    page = requests.get(page_URL)
    soup = BeautifulSoup(page.text, 'html.parser')
    # получаем список отзывов на странице
    list_rev = num_elements(soup,'div', "b-media-cont b-media-cont_reviews")
    rev_on_page = []
    plus_rev = []
    minus_rev = []
    comment_rev = []
    mod_desc = []
    for l in list_rev:
        reg = re.compile('[^a-zA-Z0-9,.а-яА-Я ]')
        model_describe_text = text_data(num_elements(l, 'div', 'b-media-cont'))
        model_describe_text = re.sub(' +', ' ', reg.sub('', model_describe_text))
        mod_desc.append(model_describe_text)
        plus_rev.append(text_data(num_elements(l, 'div', 'b-media-cont b-ico b-ico_type_plus-green b-ico_positioned_left')))
        minus_rev.append(text_data(num_elements(l, 'div', 'b-media-cont b-ico b-ico_type_minus-red b-ico_positioned_left')))
        comment_rev.append(text_data(num_elements(l, 'div', 'b-media-cont b-ico b-ico_type_repair b-ico_positioned_left')))
    rev_on_page.append([mod_desc, plus_rev, minus_rev, comment_rev])
    return rev_on_page

def list_pages(URL):
    page = requests.get(URL)
    soup = BeautifulSoup(page.text, 'html.parser')
    list_pages = []
    list_pages.append(URL)
    num_pages = num_elements(soup,'div', "b-pagination__items")
    for i in range(1,len(num_pages[0])):
        list_pages.append(num_pages[0].contents[i].attrs['href'])
    #pprint.pprint(list_pages)
    return list_pages

def grab_rev_mashins(first_page_URL):
    common_list = []
    list_of_pages = list_pages(first_page_URL)
    for URL in list_of_pages:
        common_list.append(grab_rev_from_page(URL))
    desc = []
    plus_rev = []
    minus_rev = []
    comment_rev = []
    for rec in common_list:
        desc.extend(rec[0][0])
        plus_rev.extend(rec[0][1])
        minus_rev.extend(rec[0][2])
        comment_rev.extend(rec[0][3])
    common_dict = {}
    common_dict.update({'desc':desc,
                        'plus_rev':plus_rev,
                        'minus_rev':minus_rev,
                        'comment_rev':comment_rev})
    return common_dict


df = pd.DataFrame(data=grab_rev_mashins(URL))
df.to_csv('df_1.csv')

