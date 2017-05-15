# /usr/bin/python
# encoding:utf-8
import spotipy
import json
import xlrd
import xlwt
import os
import sys
from xlutils.copy import copy
reload(sys)
sys.setdefaultencoding('utf8')

def add_content(data_sheet,song,singer,album,nrows):
	row = [song,singer,album]
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
    row0 = ['歌曲名','歌手', '专辑名']      
    #生成第一行和第二行  
    for i in range(len(row0)):  
        data_sheet.write(0, i, row0[i], set_style('Times New Roman', 220, True))   
      
    #保存文件  
    workbook.save('demo.xls')  

if __name__ == '__main__':
	key = ''
	for x in xrange(len(sys.argv)):
		if len(sys.argv)==3:
			key = sys.argv[2]
		elif len(sys.argv)==4:
			key = sys.argv[2]+' '+sys.argv[3]
		else :
			print '如果是中文歌手 -----如搜索周杰伦，请输入如下：'
			print '歌手 周杰伦'
			print '---------------------------------------------------'
			print '如果是外文歌手 -----如搜索Justin Bieber，请输入如下：'
			print '歌手 Justin Bieber'
			sys.exit(0)
	if os.path.exists("demo.xls") == False:
		write_excel()
	rb = xlrd.open_workbook('demo.xls')
	mydemo_sheet  = rb.sheet_by_name('mydemo')
	rows = mydemo_sheet.nrows
	wb = copy(rb)
	sheet = wb.get_sheet(0)
	sp = spotipy.Spotify()
	if sys.argv[1] == '歌手':
		results = sp.search(q=key,limit=50,type='album')
		print json.dumps(results,ensure_ascii = False)
		if len(sys.argv)==4:
			singer_name = key
		else :
			singer_name = results['albums']['items'][0]['artists'][0]['name']
		album_list = []
		for i, t in enumerate(results['albums']['items']):
			if t['album_type']=='album':
				print ' ', i, t['name']
				album_name = t['name']
				album_list.append(album_name)
		for x in xrange(len(album_list)):
			results = sp.search(q=album_list[x],limit=50,type='track')
			for i, t in enumerate(results['tracks']['items']):
				print ' ', i, t['name']
				artist_names = t['artists'][0]['name']
				name_size = len(t['artists'])
				if name_size>1:
					for y in range(1,name_size):
						artist_names = artist_names+","+t["artists"][y]['name']
				print "artist_names:"+artist_names
				print "singer_name:"+singer_name
				if singer_name in artist_names:
					add_content(sheet,t['name'],artist_names,t['album']['name'],rows)
					rows = rows+1
		wb.save('demo.xls')
	else :
		results = sp.search(q=key,limit=50,type='track')
		print results
		for i, t in enumerate(results['tracks']['items']):
				print ' ', i, t['name']
				artist_names = t['artists'][0]['name']
				name_size = len(t['artists'])
				if name_size>1:
					for y in range(1,name_size):
						artist_names = artist_names+","+t["artists"][y]['name']
				add_content(sheet,t['name'],artist_names,t['album']['name'],rows)
				rows = rows+1
		wb.save('demo.xls')