#! /usr/bin/python
# -*- coding: utf-8 -*-

import threading
import requests
import sys
import time

# 
FolderList = list()
FileList = list()
FolderResult = list()
FileResult = list()
FolderThread = list()
Folder2Thread = list()
FileThread = list()

headers = { "Accept":"text/html,application/xhtml+xml,application/xml;",
            "Accept-Encoding":"gzip",
            "Accept-Language":"zh-CN,zh;q=0.8",
            "Referer":"http://www.example.com/",
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"
            }

screenLock = threading.Semaphore(value=1)

# 高亮显示结果
class ColorPrinter:
    @staticmethod
    def print_red_text(content):
        print "\033[1;31;40m %s \033[0m" % (content),
    @staticmethod
    def print_green_text(content):
        print "\033[1;32;40m %s \033[0m" % (content),
    @staticmethod
    def print_blue_text(content):
	    print "\033[1;34;40m \033"

# 多线程

class myThread(threading.Thread):
	url = ''
	def __init__(self, url, timeout, flag):
		threading.Thread.__init__(self)
		self.url = url
		self.timeout = timeout
		self.flag = flag
	def run(self):
		detect(self.url, self.timeout, self.flag)

def urlInit(url):
    if(not url.startswith("http://")) and (not url.startswith("https://")):
        url = "http://" + url
    if not url.endswith("/"):
    	url = url + '/'
    return url

def stdformat():
	print "Usage: "
	print "       python %s [URL] [ThreadNumbers] [Timeout]" % (sys.argv[0])

def detect(url, timeout, flag):
    response = requests.head(url, headers = headers,timeout = timeout)
    status = response.status_code
    print url
    screenLock.acquire()
    if status == 200:
        ColorPrinter.print_green_text("[ " + str(status) + " ]")
        print "Found : " + url
        if flag == 1:
            FolderResult.append(url)
        else:
        	FileResult.append(url)
    elif status == 404 or status == 405:
        pass#ColorPrinter.print_red()
    else:
        pass
        #ColorPrinter.print_blue_text("[ " + str(status) + " ]")

    screenLock.release()

def scan(tmplist = []):
	for i in tmplist:
		time.sleep(0.1)
		i.start()
	for j in tmplist:
		j.join()

def main():

	# 初始化程序

    if len(sys.argv) == 4:
        pass
    elif len(sys.argv) == 2 and sys.argv[1] == '-h':
        stdformat()
        exit(1)
    else:
        print "parameter error!"
        print "----------------------------------"
        stdformat()
        exit(1)

    # 参数赋值，处理

    targetUrl = urlInit(sys.argv[1])
    threadNumber = int(sys.argv[2])
    timeout = float(sys.argv[3])

    print "Part 1: ......"
        
    # 读目录信息
    Folder = open('folder.txt', 'r')
 
    # 处理目录，将其转为列表，然后再将其转为线程，存储到列表，接着启动线程。
    for tmp in Folder:
    	tmp = tmp.replace('\n', '')
    	tmp = tmp.replace('\r', '')
        FolderList.append(tmp)

    for i in FolderList:
     	thread1 = myThread(targetUrl + i, timeout, 1)
        FolderThread.append(thread1)
    scan(FolderThread)

    # 扫描二级目录
    
    for i in FolderResult:
        for j in FolderList:
            thread2 = myThread(i + j, timeout, 1)
            Folder2Thread.append(thread2)
    scan(Folder2Thread)

    File = open('file.txt', 'r')
    # 将文件对象转为列表
    for tmp in File:
    	tmp = tmp.replace('\n', '')
    	tmp = tmp.replace('\r', '')
        FileList.append(tmp)
    # 等待线程结束

    print "Part 2:......"
    
    # 根目录文件
    FolderResult.insert(0, targetUrl)
    
    for i in FolderResult:
        global FileThread
        for j in FileList:
            threads2 =  myThread(i + j, timeout, 0)
            FileThread.append(threads2)
        scan(FileThread)
        FileThread = []

if __name__ == "__main__":
	main()











