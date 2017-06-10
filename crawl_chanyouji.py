#!/usr/bin/python
#-*- encoding:utf-8-*-
#
# python 3.5
# 爬取 蝉游记 chanyouji.com 的文章
# 
# 依赖 BeautifulSoup, requests, python3
# 
# python2.7 安装方式：
# python -m pip install beautifulsoup4
# python -m pip install requests 
#

from bs4 import BeautifulSoup
import requests
import MySQLdb
import random
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


# URL = "http://chanyouji.com/trips/559868"

headers = {
	"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
}


def main():
	# 创建数据库的连接
	conn= MySQLdb.connect(
	        host='localhost',
	        port = 3306,
	        user='root',
	        passwd='123456',
	        db ='food',
	        charset ='utf8'
	        )

	# 通过获取到的数据库连接conn下的cursor()方法来创建游标
	cur = conn.cursor()
	#获得表中有多少条数据
	cur.execute("select tripurl from senery")
	
	#获取所有结果       
	results = cur.fetchall()  
	result = list(results)  
	for rt in result:

		URL = rt[0]
		# print URL
		r = requests.get(URL,headers=headers)
		soup = BeautifulSoup(r.text,"html.parser")
		# print(soup.title.string)

		# date = soup.select(".note.day")[0].get_text()
		# print "\nDate:" + date

		# review = soup.select("#trip-comments")[0].get_text()
		# print "\nCommentNumber:" + review 

		notetext = soup.find_all(class_="note text")
		# print "\n=== Article:====" 

		read = random.randint(10,99)
		# print read

		art = ""
		for text in notetext:

			art = text.get_text()
			# print art 
			break

		sql = "update senery set article = '" + str(art) + "', readnum = " + str(read) + " where tripUrl = '" + str(URL) + "'"
		# sql = "update senery set readnum = " + str(read) + " where tripUrl = '" + str(URL) + "'"
		print sql
		cur.execute(sql)
		# 提交事物，向数据库插入一条数据时必须要有这个方法
		conn.commit()

	# 关闭数据库连接
	conn.close()

if __name__ == '__main__':
	main()