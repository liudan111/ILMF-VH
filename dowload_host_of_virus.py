# -*- coding: UTF-8 -*-
import urllib2 
import re
from lxml import etree
from pyquery import PyQuery as pyq
from bs4 import BeautifulSoup

print "download task start..."

file = open("G:\\python\\phage\\dowland_file.txt")
saveFile = open("G:\\python\\phage\\target.txt", "a")
failFile = open("G:\\python\\phage\\fail.txt", "a")
saveFile.truncate() #清空文件内容
failFile.truncate() #清空文件内容

#0表示每行不换行 1表示换行
saveMode = 1 

#查询的Url
searchUrl = "https://www.ncbi.nlm.nih.gov/nuccore/?term=%s+16S+ribosomal+RNA"

#最终下载文件的Url
finalUrl = "https://www.ncbi.nlm.nih.gov/sviewer/viewer.fcgi?id=%s&db=nuccore&report=fasta&extrafeat=0&fmt_mask=0&maxplex=1&sendto=t&withmarkup=on&tool=portal&log$=seqview&maxdownloadsize=1000000"

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

#解析下载地址
def parse(name, page):
	doc = pyq(page)
	test = doc(".rprt:eq(0)").text()
	retryLimit = 1
	retryTimes = retryLimit
	if test is not None and test.strip() != '':
		retryLimit = len(doc(".rprt"))
		retryTimes = retryLimit
	# retryTimes = 20 #每页20条，最多遍历20次
	uid = 0
	while retryTimes > 0:
		try:
			print retryLimit - retryTimes
			title = doc(".rprt:eq(%s) .rslt:eq(0) .title" % str(retryLimit - retryTimes)).text()
			ref = doc(".rprt:eq(%s) .rslt:eq(0) .shortcuts .dblinks:eq(0)" % str(retryLimit - retryTimes)).attr("ref")
			supp = doc(".rprt:eq(%s) .rslt:eq(0) .supp" % str(retryLimit - retryTimes)).text()
			retryTimes = retryTimes - 1
			uid = 0
			if ref is None or ref.strip()=='':
				soup = BeautifulSoup(page, "lxml")
				uid = soup.select('meta[name="ncbi_uidlist"]')[0]['content']
			else:
				#not title.startswith(name)
				if title.lower().find(name.lower()) < 0:#不包含碱基名，过滤
					continue
				if title.find("16S ribosomal RNA") < 0:#不包含16S ribosomal RNA，过滤
					continue
				length = supp.split("bp")[0].rstrip().replace(",","")
				if int(length) < 800 or int(length) > 3000:#碱基长度不符合条件，过滤
					continue
				uid = re.match(r'.*ncbi_uid=(\d+)&.*', ref).group(1)
			if uid > 0:
				break;
		except Exception as e:
			print "error occupied..."
			uid = 0
			break

	# print uid
	if uid is None or uid == 0:
		print "parse fail, save to fail.txt..."
		failFile.write(name + "\n")#收集下载失败的序列名，手动操作
		return ""
	return finalUrl % uid

#追加到Txt文件
def appendToText(targetText):
	if targetText is None or targetText.strip()=='':
		print "error occupied..."
		return
	if saveMode == 1:
		text = targetText.split('\n', 1)
		header = text[0]
		content = text[1]
		content = re.sub(r'\s', "", content)
		targetText = header + "\n" + content
	# print targetText
	saveFile.write(targetText.strip('\n') + "\n")

#循环读取需要下载的文件名列表
while 1:
	lines = file.readlines(100000)
	if not lines:
		break
	for line in lines:
		name = line.strip('\n')
		print name
		url = searchUrl % urllib2.quote(name) 
		page = fetch(url)
		targetUrl = parse(name, page)
		if targetUrl is None or targetUrl.strip()=='':
			continue
		targetText = fetch(targetUrl)
		appendToText(targetText)

file.close()
saveFile.close()
failFile.close()

print "dowland complete!"


