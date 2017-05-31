# /usr/bin/python
# encoding:utf-8
import json
import xlrd
import xlwt
import os
import sys
import time
import requests
from xlutils.copy import copy
reload(sys)
sys.setdefaultencoding('utf8')

def add_content(data_sheet,song,singer,album,track_number,nrows):
	row = [song,singer,album,track_number]
	for i in range(len(row)):  
		data_sheet.write(nrows, i, row[i], set_style('Times New Roman', 220, True))

def set_style(name, height, bold = False):  
    style = xlwt.XFStyle()   #初始化样式  
    font = xlwt.Font()       #为样式创建字体  
    font.name = name  
    font.bold = bold  
    font.color_index = 4  
    font.height = height  
    style.font = font  
    return style 


def write_excel():
	#创建工作簿  
    workbook = xlwt.Workbook(encoding='utf-8')    
    #创建sheet  
    data_sheet = workbook.add_sheet('mydemo')  
    row0 = ['歌曲名','歌手', '专辑名','在专辑中的顺序']      
    #生成第一行和第二行  
    for i in range(len(row0)):  
        data_sheet.write(0, i, row0[i], set_style('Times New Roman', 220, True))   
      
    #保存文件  
    workbook.save('demo.xls')  

def read_txt():
    keywordsList = []
    f = open("test.txt")
    lines = f.readlines()
    for x in xrange(len(lines)):
        # print lines[x].strip('\n')
        keywordsList.append(lines[x].strip('\n'))
    f.close()
    return keywordsList

headers = {#User-Agent需要根据每个人的电脑来修改
		'Host': 'api.spotify.com',
		'Accept': 'application/json',
		'Content-Type': 'application/json',
		'Accept-Encoding': 'gzip, deflate, compress',
		'Authorization': 'Bearer BQDcH3s5D3RigGLlA97e6lVgY0728bw6iVtMF_pPi9DCC8vUxzLIAgGgorPLCEejhCiZ5vMrivLrNc1n0ls-mCgfi2KzPqX7c_LBIn8fKTVQV3qGZ1wW0XXxVLoJ_PV3--UgfqbY0c136HYP8cSmpZ-qjiaG20MNTlGswA_hPzZL58kuDhS2lBkxxMexppR9ZyjwiRmKsWTptU86ZRt-j2uHyGZVBM8HisNFQRoz6wSUOm_tXAaOIHZAAf3AUxBp',
		'User-Agent': 'Spotify API Console v0.1'
        }

if __name__ == '__main__':
	keywords = read_txt()
	for z in xrange(len(keywords)):
		key = keywords[z]
		print key
		if os.path.exists("demo.xls") == False:
			write_excel()
		rb = xlrd.open_workbook('demo.xls')
		mydemo_sheet  = rb.sheet_by_name('mydemo')
		rows = mydemo_sheet.nrows
		wb = copy(rb)
		sheet = wb.get_sheet(0)
		myparams = {"q":key,"limit":50,"type":'album'}
		response = requests.get("https://api.spotify.com/v1/search?",headers=headers,params = myparams)
		results = response.json()
		singer_name = str(key)
		album_list = []
		for i, t in enumerate(results['albums']['items']):
			album_name = t['name']
			album_list.append(album_name)
		for x in xrange(len(album_list)):
			data_list = []
			track_key = album_list[x]+" "+key
			mparams = {"q":track_key,"limit":50,"type":'track'}
			response = requests.get("https://api.spotify.com/v1/search?",headers=headers,params = mparams)
			results = response.json()
			for i, t in enumerate(results['tracks']['items']):
				artist_name = t['artists'][0]['name']
				name_size = len(t['artists'])
				if name_size>1:
					for y in range(1,name_size):
						artist_name = artist_name+","+t["artists"][y]['name']
				artist_names = str(artist_name)
				singer_names = singer_name.replace("\r","")
				print t['name']
				print artist_names
				print singer_names
				print "-------------------"
				if singer_names in artist_names and album_list[x]==t['album']['name']:
					dict = {'name':t['name'],'track_number':t['track_number'],'album_name':t['album']['name'],'singer_name':artist_name}
					data_list.append(dict)
			data_list.sort(key=lambda obj:obj.get('track_number'),reverse=False)
			print "size:"+str(len(data_list))
			for x in xrange(len(data_list)):
				print data_list[x]['name'],data_list[x]['track_number']
				print "rows"+str(rows)
				add_content(sheet,data_list[x]['name'],data_list[x]["singer_name"],data_list[x]['album_name'],data_list[x]['track_number'],rows)
				rows = rows+1
			print "---------------------------------------------"
		wb.save('demo.xls')
		print("--------------------save success-------------------")
		# time.sleep(3)