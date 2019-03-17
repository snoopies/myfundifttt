#coding=utf-8
from bs4 import BeautifulSoup
#import requests
import io
import sys
import json
import urllib.request, urllib.parse, urllib.response, urllib.error
from flask import Flask
from flask import request
#from urllib import request
#from urllib import parse
from datetime import datetime
app = Flask(__name__)
    

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') 



#def http_post():
#    url='https://maker.ifttt.com/trigger/uuu/with/key/py1yJDLJz7zXczrGiBNZ-'
#    values ={ "value1" : "smith", "value2" : "join", "value3" : "123456" }

#    jdata = json.dumps(values)             # 对数据进行JSON格式化编码
#    req = urllib.request(url, jdata)       # 生成页面请求的完整数据
#    response = urllib.urlopen(req)       # 发送页面请求
#    print(response.read())
#    return response.read()                    # 获取服务器返回的页面信息


def http_post2(post_data):
    url = "https://maker.ifttt.com/trigger/uuu/with/key/py1yJDLJz7zXczrGiBNZ-"
    data = post_data
    params="?"
#    for key in data:
#        params = params + key + "=" + data[key] + "&"
#    print("Get方法参数："+params)
    headers = {
        #heard部分直接通过chrome部分request header部分
        'Accept':'application/json, text/plain, */*',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Connection':'keep-alive',
        #'Content-Length':'38', #get方式提交的数据长度，如果是post方式，转成get方式：【id=wdb&pwd=wdb】
        'Content-Type':'application/x-www-form-urlencoded',
        #'Referer':'http://10.1.2.151/',
        'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.23 Mobile Safari/537.36'
    }
    data = urllib.parse.urlencode(data).encode('utf-8')
    try:
        req = urllib.request.Request(url, headers=headers, data=data)  #POST方法
        #req = urllib.request.Request(url+params)  # GET方法
        page = urllib.request.urlopen(req).read()
        page = page.decode('utf-8')
        #    print(page)
    except error.HTTPError as error:    # HTTP错误
        print('HTTPError')
        print('ErrorCode: %s' % error.code)
    except error.URLError as error:     # URL错误
        print(error.reason)



def get_fund(fundcode):
    #使用requests抓取页面内容，并将响应赋值给page变量
    #html = requests.get('http://quotes.money.163.com//fund/jzzs_150165.html')
    #html = requests.get('http://quotes.money.163.com/fund/270014.html')
    req = """http://quotes.money.163.com/fund/{code}.html""".format(code=fundcode)  # GET方法
    try:
        #urllib2.urlopen(req)
        html = urllib.request.urlopen(req)
        #使用content属性获取页面的源页面
        #使用BeautifulSoap解析，吧内容传递到BeautifulSoap类
        soup = BeautifulSoup(html,'lxml',from_encoding='utf-8')
        data={}
        data["value1"] = fundcode
        data["value2"] = soup.body.select('div.fn_data_trend>div')[0].select('big')[0].next_element
        data["value3"] = soup.body.select('div.fn_data_trend>div')[0].select('big')[1].next_element
        return data
        #我是分隔符，下面就是select（）方法咯~
        #table = soup.find_all('table',class_='fn_cm_table')[0]
        #links = soup.select('body > div.fn_wrap > div.fn_data_title > div.fn_data_trend > div.fn_data_trend_total')
        #for link in links:
        #    print(link.get_text())
        #tab = table.find_all('tbody')[0]
        #print(tab)
        #for tr in table.find_all('tr'):
           #print(tr)
           #for td in tr.find_all('td'):
               #print(td.get_text())
    except error.HTTPError as error:    # HTTP错误
        print('HTTPError')
        print('ErrorCode: %s' % error.code)
    except error.URLError as error:     # URL错误
        print(error.reason)

    

@app.route('/')
def homepage():
    the_time = datetime.now().strftime("%A, %d %b %Y %l:%M %p")
    return """
    <h1>Hello heroku</h1>
    <p>It is currently {time}.</p>
    """.format(time=the_time)

#    for arg in request.args:
#        print(arg)
#    return """{time}""".format(time=request.args.get("fundscode"))

@app.route('/funds/')
def funds():
    if request.args.get("fundscode") == None:
        return "Error Request!"
    funds=request.args.get("fundscode").split(",")
    for fund in funds:
        data = get_fund(fund)
        http_post2(data)
#        http_post2({"value1":"smith","value2":"join","value3":"123456"})
    return "data"




if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
    
