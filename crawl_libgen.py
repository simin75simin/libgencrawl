from datetime import datetime
import os
import pickle
from icecream import ic
import requests
from tqdm import tqdm
from lxml.html import fromstring
from urllib.request import urlretrieve

def timestr():
    now=datetime.now()
    date_time = now.strftime("%m-%d-%Y_%H:%M:%S")
    return date_time

def crawl(url,num=10,page=1):
    dirname='results_'+timestr()
    os.mkdir(dirname)
    os.chdir(dirname)
    resp=requests.get(url).content
    tree=fromstring(resp)
    bookpath=f'/html/body/table[3]//td[10]/a'
    booklinks=tree.xpath(bookpath)
    for booklink in tqdm(booklinks,desc=f'page {page}'):
        if num<=1:
            return
        downloadurl=booklink.values()[0]
        bookresp=requests.get(downloadurl).content
        tree=fromstring(bookresp)
        titlepath='/html/body/table/tr/td[2]/h1'
        dlpath='/html/body/table/tr/td[2]/div[1]/h2/a'
        title=tree.xpath(titlepath)[0].text_content()
        dllink=tree.xpath(dlpath)[0].values()[0]
        ext=dllink[dllink.rindex('.')+1:]
        filename=f'{title}.{ext}'
        urlretrieve(dllink,os.path.join('.',filename))
        num-=1
    nextpagepath='/html/body/table[2]/tr/td[2]/font/a'
    try:
        nextpagelink=tree.xpath(nextpagepath)[0].values()[0]
        crawl(nextpagelink,page+1,num)
    except:
        pass


if __name__=='__main__':
    url=input('please input url after search and press enter: ')
    num=input('please input the number of books you wanna crawl and press enter: ')
    num=int(num)
    crawl(url,num)
