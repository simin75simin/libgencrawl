import os
import pickle
from icecream import ic
import requests
from tqdm import tqdm
from lxml.html import fromstring
from urllib.request import urlretrieve

def crawl(url,page=1):
    os.chdir('results')
    resp=requests.get(url).content
    tree=fromstring(resp)
    bookpath=f'/html/body/table[3]//td[10]/a'
    booklinks=tree.xpath(bookpath)
    for booklink in tqdm(booklinks,desc=f'page {page}'):
        downloadurl=booklink.values()[0]
        bookresp=requests.get(downloadurl).content
        tree=fromstring(bookresp)
        titlepath='/html/body/table/tr/td[2]/h1'
        dlpath='/html/body/table/tr/td[2]/div[1]/h2/a'
        title=tree.xpath(titlepath)[0].text_content()
        dllink=tree.xpath(dlpath)[0].values()[0]
        ext=dllink[dllink.rindex('.')+1:]
        filename=f'{title}.{ext}'
        #ic(title,filename,dllink)
        urlretrieve(dllink,os.path.join('.',filename))
    nextpagepath='/html/body/table[2]/tr/td[2]/font/a'
    #ic(tree.xpath(nextpagepath)[0].values()[0])
    try:
        nextpagelink=tree.xpath(nextpagepath)[0].values()[0]
        crawl(nextpagelink,page+1)
    except:
        pass


if __name__=='__main__':
    url=input('please input url after search and press enter: ')
    crawl(url)
