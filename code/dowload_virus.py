# -*- coding: UTF-8 -*-
import urllib2 
import os
from lxml import etree
from pyquery import PyQuery as pyq
from bs4 import BeautifulSoup

downloadFile = open("G:\\python\\virus820_fail.txt", "r")
failFile = open("G:\\python\\virus820_fail.txt", "a")
#域名
domain = "https://www.ncbi.nlm.nih.gov"

#查询的Url‘
searchUrl = "https://www.ncbi.nlm.nih.gov/nuccore/%s"

#目标url
targetUrl = "https://www.ncbi.nlm.nih.gov/sviewer/viewer.fcgi?id=%s&db=nuccore&report=fasta&extrafeat=0&conwithfeat=on&retmode=html&withmarkup=on&tool=portal&log$=seqview&maxdownloadsize=1000000"

#抓取网页内容
def fetch(url):
	# print url
	data = ""
	while 1:
		try:
			request = urllib2.Request(url)
			response = urllib2.urlopen(request)
			data = response.read()
		except Exception as e:
			print "Retrying..."
			continue
		break
	return data

#解析网页内容
def parse(page):
    doc = pyq(page)
    content = doc(".dblinks[ref$=fasta]").attr['href']
    return content

#解析uid
def parseUid(page):
    soup = BeautifulSoup(page, "lxml")
    uid = soup.select('meta[name="ncbi_uidlist"]')[0]['content']
    return uid
    
#保存文件
def saveFile(filename, content):
    saveFile = open("G:\\python\\download_820virus\\" + filename, "w")
    saveFile.write(content)
    saveFile.close()
	
for name in downloadFile.readlines():
    try:
        firstUrl = searchUrl % name
        tempUrl = domain + parse(fetch(firstUrl))
        uid = parseUid(fetch(tempUrl))
        print(name)
        filename = name.strip('\n') + ".fasta"
        if os.path.exists(filename):
            print(filename + "文件已存在")
            continue
        saveFile(filename, fetch(targetUrl % uid))
    except Exception as e:
        failFile.write(name)#收集下载失败的序列名，手动操作
        print "parse fail, save to fail.txt..."
        continue
downloadFile.close()
print("completed")