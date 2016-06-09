import csv
import requests
from urllib.request import urlopen
from urllib.error import *
import re

from bs4 import BeautifulSoup
#异常处理
def getTitle(url):
    try:
        html = urlopen(url)
    except URLError as e:
        print(e)
        return None
    except HTTPError as f:
        print(f)
        return None
    try:
        bsObj = BeautifulSoup(html.read(), "html.parser")
        title = bsObj.body.h1
    except AttributeError as e:
        print(e)
        return None
    if title == None:
        print("No Title Found")
    else:
        return title

def getName(url):
    bsObj = BeautifulSoup(urlopen(url), "html.parser")
    namelist = bsObj.findAll("span", {"class":"green"})
    for name in namelist:
        print(name.get_text())

def getGiftName(url):
    bsObj = BeautifulSoup(urlopen(url), "html.parser")
    nameList = bsObj.find("table",{"id":"giftList"}).tr.next_siblings
    for name in nameList:
        if name.find('td') != -1:
            print(name.find('td').get_text().strip())

#regular expression
def getImg(url):
    bsObj = BeautifulSoup(urlopen(url), "html.parser")
    images = bsObj.findAll("img",{"src" : re.compile(r"\.\.\/img\/gifts\/img.*\.jpg")})
    for image in images:
        print(image["src"])

def getIPs(url):
    global ips, urls
    print(url)
    urls.add(url)
    try :
        html = urlopen(url)
    except URLError as e:
        print(e)
        return None
    except HTTPError as f:
        print(f)
        return None
    print("Open url")
    bsObj = BeautifulSoup(html,"html.parser")
    print("Parsed")
    history = urlopen("https://en.wikipedia.org"+bsObj.find('li', {'id':'ca-history'}).find('a').attrs['href'])
    print("Open History")
    bsObj2 = BeautifulSoup(history,"html.parser")
    print("parse history")
    ipAddr = bsObj2.findAll("a", text = re.compile(r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])'))
    print("Ips found")
    print("Ips:")
    for ip in ipAddr:
        out = ip.get_text()
        if out not in ips:
            print(out)
        ips.add(out)

    links = bsObj.find('div', {'id':'content'}).findAll("a", {"href": re.compile(r"^(/wiki/)((?!:).)*$")})
    print("links found")
    for link in links:
        title = link['href']
        url = "https://en.wikipedia.org" + title
        if url not in urls:
            print(title)
            getIPs(url)

#
# def findToken(bsObj) :
#     token = bsObj.find('meta', {'name': "csrf-token"}).attrs['content']
#     return token
#
#
# session = requests.session()
#
# login = session.get('http://thecourseforum.com/users/sign_in')
#
# loginB = BeautifulSoup(login.text, 'html.parser')
#
# token = findToken(loginB)
#
#
# postdata = {
#     'utf8':'%E2%9C%93',
#     'authenticity_token' : token,
#     'user[email]':'ys7va@virginia.edu',
#     'user[password]':'Junjun702881',
#     'commit':'Login',
#     'user[remember_me]': '0'
# }
#
# header = {
#     "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:35.0) Gecko/20100101 Firefox/35.0 ",
#     "Accept-Encoding" : "gzip, deflate"
# }
#
# r = session.post('http://thecourseforum.com/users/sign_in', data = postdata, headers = header)
#
# browsePage = session.get('http://thecourseforum.com')
#
# browseB = BeautifulSoup(browsePage.text, 'html.parser')
#
# links = browseB.find_all('a', {'href' : re.compile(r"^(\/departments\/)")})
#
# csvFile = open("../data/CourseLinks.csv", 'w+')
#
# writer = csv.writer(csvFile)
#
# writer.writerow(('Course Title', 'Course Link'))
# for link in links:
#     department = session.get("http://thecourseforum.com" + link.attrs['href'])
#     departmentB = BeautifulSoup(department.text, "html.parser")
#     courseLinks = departmentB.find_all('a', {'href' : re.compile(r"^(\/courses\/)")})
#     for course in courseLinks:
#         child1 = course.div
#         title = child1.text
#         url = "http://thecourseforum.com" + course.attrs['href']
#         writer.writerow((title, url))
#     print('department1 finished')
#
# csvFile.close()

