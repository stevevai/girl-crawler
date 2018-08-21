# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 18:00:38 2018

@author: WangShuai
"""
import requests
import os
import urllib
import http.cookiejar
from lxml import html
import random
import time
def get_page_urls(num):
    url_base = 'http://www.mmjpg.com/mm/'
    urls = []
    # 网站共有1300个页面
    rand_list = list(range(1, 1300))
    for i in random.sample(rand_list, num):
        url = url_base + str(i)
        print (url)
        urls.append(url)
    print ("###共"+str(len(urls))+"个无重复页面###\n")
    return urls

def get_image_title(url):
    response = requests.get(url).content
    selector = html.fromstring(response)
    image_title = selector.xpath("//h2/text()")[0]
    image_amount = selector.xpath("//div[@class='page']/a[last()-1]/text()")[0]
    return image_title, image_amount

def get_image_detail_website(url):
    image_title, image_amount = get_image_title(url)
    image_detail_websites = []
    for i in range(int(image_amount)):
        try:
            image_detail_link = '{}/{}'.format(url, i+1)
            response = requests.get(image_detail_link).content
            sel = html.fromstring(response)
            image_download_link = sel.xpath("//div[@class='content']/a/img/@src")[0]
            image_detail_websites.append(image_download_link)
        except Exception as err:
            continue       
    return image_detail_websites

def download_image(image_title, image_detail_websites, path_name=''):
    num = 1
    amount = len(image_detail_websites)
    for i in image_detail_websites:
        filename = '%s%s.jpg' % (image_title, num)
        print('正在下载图片：%s第%s/%s张，' % (image_title, num, amount))
        try:          
            headers={
                    'Referer':'http://www.mmjpg.com/'
                    }
            content = requests.get(i,headers=headers)
            
            ifile = open('./'+path_name+'/'+filename, 'wb')
            ifile.write(content.content)
            num += 1
        except Exception as err:
            print (err)
            print ('........ 图片下载失败 ........')
            continue    

if __name__ == '__main__':
    page_numbers = int(input('请输入需要爬取的套图数量：'))
for link in get_page_urls(page_numbers):
    try:
        path_name = get_image_title(link)[0]
        os.makedirs('./'+path_name)
        print ("#"*10+"正在解析网页： "+link+"#"*10)
        download_image(get_image_title(link)[0], get_image_detail_website(link), path_name)
        time.sleep(10)
    except Exception as err:
        print (err)
        print ("........ %s网页解析失败 ........") % link
        continue























