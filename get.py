#coding=utf-8
from bs4 import BeautifulSoup
import requests
import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') 


#使用requests抓取页面内容，并将响应赋值给page变量
html = requests.get('https://www.qiushibaike.com/text/')
 
#使用content属性获取页面的源页面
#使用BeautifulSoap解析，吧内容传递到BeautifulSoap类
soup = BeautifulSoup(html.content,'lxml',from_encoding='utf-8')
#我是分隔符，下面就是select（）方法咯~
#print(soup)
links = soup.select('div > a > div >span')
#links = soup.find_all('div',class_='content')
for link in links:
    print(link.get_text())
