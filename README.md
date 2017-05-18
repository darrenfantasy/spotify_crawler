# Windows 里环境配置

## 1.安装Python环境

网址：https://www.python.org/downloads/release/python-2713/

下载Python 2.7.13版本的。

为计算机添加安装目录到环境变量，及测试Python安装是否成功。

按照此网址 http://www.cnblogs.com/windinsky/archive/2012/09/20/2695520.html

## 2.安装pip

详情见 http://www.tuicool.com/articles/eiM3Er3/   的pip安装即可

下载地址  https://pypi.python.org/pypi/pip#downloads

## 3.安装xlrd和xlwt

命令行里输入

pip install xlrd

pip install xlwt

详情见 http://blog.csdn.net/wangkai_123456/article/details/50457284

就上面两条命令就好，不需要看网页里的使用介绍了

**安装 xlutils**

命令： pip install xlutils

## 4.安装spotipy环境

pip install spotipy

## 5.运行脚本

先进入到你存放脚本的目录

cd 你的目录 

如 我存放脚本的目录是 Documents/study/python/spotify/

那么输入：  cd Documents/study/python/spotify/

然后输入 ls 即可看到当前目录有哪些文件。

如搜索周杰倫 ，输入以下命令：

os系统：

python search_from_spotify.py 周杰倫

windows系统：

search_from_spotify_for_windows.py 周杰倫

## 6.友情提示

如果搜索不到结果

如周杰伦是无结果的需改成周杰倫。因为代码中加了判断，歌手名必须和网站返回的结果名一致，否则不写入excel里。当然要想周杰伦有结果，把  if singer_name in artist_names:  这句判断条件去掉即可。