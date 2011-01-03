
import xbmc, xbmcgui, xbmcplugin, urllib2, urllib, re, string, sys, os, traceback, xbmcaddon

__plugin__ = "Trailer Addict"
__author__ = 'stacked <stacked.xbmc@gmail.com>'
__url__ = 'http://code.google.com/p/plugin/'
__date__ = '12-20-2010'
__version__ = '1.0.3'
#__settings__ = xbmcaddon.Addon(id='plugin.video.trailer.addict')

HEADER = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.1) Gecko/20090624 Firefox/3.5'
THUMBNAIL_PATH = os.path.join(os.getcwd().replace( ";", "" ),'resources','media')

def main():
	li3=xbmcgui.ListItem("Search",iconImage="DefaultVideo.png", thumbnailImage=os.path.join(THUMBNAIL_PATH, 'search_icon.png'))
	u3=sys.argv[0]+"?mode=0&name="+urllib.quote_plus('Search')
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u3,li3,True)
	li3=xbmcgui.ListItem("Film Database",iconImage="DefaultVideo.png", thumbnailImage=os.path.join(THUMBNAIL_PATH, 'media.png'))
	u3=sys.argv[0]+"?mode=4&name="+urllib.quote_plus('Film Database')
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u3,li3,True)
	li3=xbmcgui.ListItem("Coming Soon",iconImage="DefaultVideo.png", thumbnailImage=os.path.join(THUMBNAIL_PATH, 'media.png'))
	u3=sys.argv[0]+"?mode=6&name="+urllib.quote_plus('Coming Soon')+"&url="+urllib.quote_plus('http://www.traileraddict.com/comingsoon')+"&page="+str(page)
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u3,li3,True)
	#li3=xbmcgui.ListItem("Latest Trailers",iconImage="DefaultVideo.png", thumbnailImage=os.path.join(THUMBNAIL_PATH, 'media.png'))
	#u3=sys.argv[0]+"?mode=2&name="+urllib.quote_plus('Latest Trailers')+"&url="+urllib.quote_plus('http://www.traileraddict.com/trailers')+"&page="+str(page)
	#xbmcplugin.addDirectoryItem(int(sys.argv[1]),u3,li3,True)
	#li3=xbmcgui.ListItem("Latest Clips",iconImage="DefaultVideo.png", thumbnailImage=os.path.join(THUMBNAIL_PATH, 'media.png'))
	#u3=sys.argv[0]+"?mode=2&name="+urllib.quote_plus('Latest Clips')+"&url="+urllib.quote_plus('http://www.traileraddict.com/clips')+"&page="+str(page)
	#xbmcplugin.addDirectoryItem(int(sys.argv[1]),u3,li3,True)
	li3=xbmcgui.ListItem("Top 150 Films of the Week",iconImage="DefaultVideo.png", thumbnailImage=os.path.join(THUMBNAIL_PATH, 'media.png'))
	u3=sys.argv[0]+"?mode=5&name="+urllib.quote_plus('Top 150 Films of the Week')
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u3,li3,True)
	xbmcplugin.addSortMethod( handle = int(sys.argv[ 1 ]), sortMethod = xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory(int(sys.argv[1]))
	
def runKeyboard():
	searchStr = ''
	keyboard = xbmc.Keyboard(searchStr, "Search")
	keyboard.doModal()
	if (keyboard.isConfirmed() == False):
		return
	searchstring = keyboard.getText()
	newStr = searchstring.replace(' ','+')
	if len(newStr) == 0:
		return
	url='http://www.traileraddict.com/search.php?domains=www.traileraddict.com&sitesearch=www.traileraddict.com/tags&q=' + newStr + '&client=pub-8929492375389186&forid=1&channel=4779144239&ie=ISO-8859-1&oe=ISO-8859-1&safe=active&cof=GALT%3A%235A5A5A%3BGL%3A1%3BDIV%3A%23336699%3BVLC%3ACD0A11%3BAH%3Acenter%3BBGC%3AFFFFFF%3BLBGC%3AFFFFFF%3BALC%3ACD0A11%3BLC%3ACD0A11%3BT%3A000000%3BGFNT%3ACD0A11%3BGIMP%3ACD0A11%3BLH%3A50%3BLW%3A227%3BL%3Ahttp%3A%2F%2Fwww.traileraddict.com%2Fimages%2Fgoogle.png%3BS%3Ahttp%3A%2F%2Fwww.traileraddict.com%3BFORID%3A11&hl=en'
	#print url
	showList(url,newStr)

def showList(url, name):
	nexturl=url
	req=urllib2.Request(url+'&start='+str(page*10))
	req.add_header('User-Agent', HEADER)
	f=urllib2.urlopen(req)
	a=f.read()
	f.close()
	image=re.compile('<center>\r\n<div style="background:url\((.*?)\);" class="searchthumb">',re.DOTALL).findall(a)
	link_title=re.compile('</div><a href="/tags/(.*?)">(.*?)</a><br />').findall(a)
	#date=re.compile('<span style="font-size:7pt;">(.*?)</span><br /><br />').findall(a)
	#director=re.compile('<span style="color:#6D7D31;">Director:</span> (.*?)<br />').findall(a)
	#writer=re.compile('<span style="color:#6D7D31;">Writer:</span> (.*?)<br />').findall(a)
	#cast=re.compile('<span style="color:#6D7D31;">Condensed Cast:</span> (.*?)<br />').findall(a)
	if len(link_title) == 0:
		dialog = xbmcgui.Dialog()
		ok = dialog.ok('Trailer Addict', 'Your search - '+name+' - did not match any documents.\nMake sure all words are spelled correctly\nor try different keywords.')
		main()
		return
	item_count=0
	for url,title in link_title:
		url='http://www.traileraddict.com/tags/'+url
		imagex=image[item_count].replace('/pthumb.php?dir=','').replace('\r\n','')
		thumb='http://www.traileraddict.com'+imagex
		name = clean(title)
		item=xbmcgui.ListItem(name, iconImage=thumb, thumbnailImage=thumb)
		#year=re.compile('[0-9][0-9][0-9][0-9]').findall(date[item_count])
		#item.setInfo( type="Video", infoLabels={ "Title": clean(title), "Year": int(year[0]), "Director": director[item_count], "Writer": writer[item_count] } )
		u=sys.argv[0]+"?mode=2&name="+urllib.quote_plus(clean(title))+"&url="+urllib.quote_plus(url)
		xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,isFolder=True)
		item_count=item_count+1
	xbmcplugin.addSortMethod( handle = int(sys.argv[ 1 ]), sortMethod = xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def get_tags(url, name):
	#print url
	savename=name
	nexturl=url
	req=urllib2.Request(url+'/'+str(page+1))
	req.add_header('User-Agent', HEADER)
	f=urllib2.urlopen(req)
	a=f.read()
	f.close()
	link_thumb=re.compile('<a href="(.+?)"><img src="(.+?)" name="thumb').findall(a)
	thumbs=re.compile('img src="/psize\.php\?dir=(.+?)" style').findall(a)
	if len(thumbs) == 0:
		thumb="DefaultVideo.png"
	else:
		thumb='http://www.traileraddict.com/'+thumbs[0]
	#disc=re.compile('<em>(.+?)</em><br />').findall(a)
	#info=re.compile('</a><br />Runtime: (.+?) | Views:').findall(a)
	title=re.compile('<div class="abstract"><h2><a href="(.+?)">(.+?)</a></h2><br />', re.DOTALL).findall(a)
	index=re.compile('Page \((.+?)/(.+?)\)&nbsp;', re.DOTALL).findall(a)
	trailers=re.compile('<dl class="dropdown">(.+?)</dl>', re.DOTALL).findall(a)
	item_count=0
	if len(trailers) > 0:
		check1=re.compile('<a href="(.+?)"><img src="\/images\/usr\/arrow\.png" border="0" style="float:right;" \/>(.+?)</a>').findall(trailers[0])
		check2=re.compile('<a href="(.+?)"( style="(.*?)")?>(.+?)<br />').findall(trailers[0])
		#print check2
		if len(check1) > 0:
			url_title=check1
			for url,title in url_title:
				url='http://www.traileraddict.com'+url
				item=xbmcgui.ListItem(clean(title), iconImage=thumb, thumbnailImage=thumb)
				u=sys.argv[0]+"?mode=3&name="+urllib.quote_plus(savename+' ('+clean(title)+')')+"&url="+urllib.quote_plus(url)
				xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,isFolder=False)
			xbmcplugin.addSortMethod( handle = int(sys.argv[ 1 ]), sortMethod = xbmcplugin.SORT_METHOD_NONE )
			xbmcplugin.endOfDirectory(int(sys.argv[1]))
		elif len(check2) > 0:
			url_title=check2
			for url,trash,trash2,title in url_title:
				url='http://www.traileraddict.com'+url
				item=xbmcgui.ListItem(clean(title), iconImage=thumb, thumbnailImage=thumb)
				u=sys.argv[0]+"?mode=3&name="+urllib.quote_plus(savename+' ('+clean(title)+')')+"&url="+urllib.quote_plus(url)
				xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,isFolder=False)
			xbmcplugin.addSortMethod( handle = int(sys.argv[ 1 ]), sortMethod = xbmcplugin.SORT_METHOD_NONE )
			xbmcplugin.endOfDirectory(int(sys.argv[1]))
		else:
			dia = xbmcgui.Dialog()
			ok = dia.ok("No trailers found!", 'Please report this problem to stacked.xbmc@gmail.com')
	else:
		for url,thumb2 in link_thumb:
			if clean(title[item_count][1]).find('Trailer') > 0: 
				url='http://www.traileraddict.com'+url
				item=xbmcgui.ListItem(clean(title[item_count][1]), iconImage=thumb, thumbnailImage=thumb)
				u=sys.argv[0]+"?mode=3&name="+urllib.quote_plus(savename+' ('+clean(title[item_count][1])+')')+"&url="+urllib.quote_plus(url)
				xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,isFolder=False)
			item_count=item_count+1
		xbmcplugin.addSortMethod( handle = int(sys.argv[ 1 ]), sortMethod = xbmcplugin.SORT_METHOD_NONE )
		xbmcplugin.endOfDirectory(int(sys.argv[1]))

def get_film(url, name):
	searchStr = ''
	keyboard = xbmc.Keyboard(searchStr, "Enter the film's starting letter or word, or release year:")
	keyboard.doModal()
	if (keyboard.isConfirmed() == False):
		return
	searchstring = keyboard.getText()
	newStr = searchstring.replace(' ','+')
	if len(newStr) == 0:
		return
	url='http://www.traileraddict.com/thefilms/'+newStr
	req=urllib2.Request(url)
	req.add_header('User-Agent', HEADER)
	f=urllib2.urlopen(req)
	a=f.read()
	f.close()
	link_title=re.compile('<img src="/images/arrow2.png" class="arrow"> <a href="(.+?)">(.+?)</a>').findall(a)
	#print link_title
	item_count=0
	for url,title in link_title:
		url='http://www.traileraddict.com/'+url
		name = clean(title)
		item=xbmcgui.ListItem(name)
		item.setInfo( type="Video", infoLabels={ "Title": name } )
		u=sys.argv[0]+"?mode=2&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)
		xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,isFolder=True)
		item_count=item_count+1
	xbmcplugin.addSortMethod( handle = int(sys.argv[ 1 ]), sortMethod = xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def coming_soon(url, name):
	req=urllib2.Request(url)
	req.add_header('User-Agent', HEADER)
	f=urllib2.urlopen(req)
	a=f.read()
	f.close()
	link_title=re.compile('<img src="/images/arrow2.png" class="arrow"> <a href="(.+?)">(.+?)</a>').findall(a)
	#print link_title
	item_count=0
	for url,title in link_title:
		url='http://www.traileraddict.com/'+url
		name = clean(title)
		item=xbmcgui.ListItem(name)
		item.setInfo( type="Video", infoLabels={ "Title": name } )
		u=sys.argv[0]+"?mode=2&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)
		xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,isFolder=True)
		item_count=item_count+1
	xbmcplugin.addSortMethod( handle = int(sys.argv[ 1 ]), sortMethod = xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def get_top(url, name):
	url='http://www.traileraddict.com/top150'
	req=urllib2.Request(url)
	req.add_header('User-Agent', HEADER)
	f=urllib2.urlopen(req)
	a=f.read()
	f.close()
	link_title=re.compile('<img src="/images/arrow2.png" class="arrow"> <a href="(.+?)">(.+?)</a> <span style="font-size:7pt;">(.+?)</span>').findall(a)
	#print link_title
	item_count=75
	for test in range(0,150):
		if item_count == 150:
			item_count = 0
		url=link_title[item_count][0]
		views=link_title[item_count][2]
		title=link_title[item_count][1]
		#print title
		url='http://www.traileraddict.com/'+url
		name = clean(title)+' '+views
		item=xbmcgui.ListItem(name)
		item.setInfo( type="Video", infoLabels={ "Title": clean(title) } )
		u=sys.argv[0]+"?mode=2&name="+urllib.quote_plus(clean(title))+"&url="+urllib.quote_plus(url)
		xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,isFolder=True)
		item_count=item_count+1
	xbmcplugin.addSortMethod( handle = int(sys.argv[ 1 ]), sortMethod = xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory(int(sys.argv[1]))
		
def get_trailer(url,name):
		req = urllib2.Request(url)
		req.add_header('User-Agent', HEADER)
		f=urllib2.urlopen(req)
		a=f.read()
		f.close()
		p=re.compile('<param name="movie" value="http://www.traileraddict.com/emb/(.+?)">')
		info=p.findall(a)
		if a.find('black-tab-hd.png') > 0:
			url='http://www.traileraddict.com/fvarhd.php?tid='+info[0]
		else:
			url='http://www.traileraddict.com/fvar.php?tid='+info[0]
		#print url
		req = urllib2.Request(url)
		req.add_header('User-Agent', HEADER)
		f=urllib2.urlopen(req)
		a=f.read()
		f.close()
		p=re.compile('fileurl=(.+?)&vidwidth')
		info=p.findall(a)
		z=re.compile('&image=(.+?)').findall(a)
		url=info[0]
		thumb=z[0]
		print url
		url=url.replace('%3A', ':').replace('%2F', '/').replace('%3F', '?').replace('%3D', '=').replace('%26', '&').replace('%2F', '//')
		#Gets redirect url, fixes problem in linux and osx
		req = urllib2.Request(url)
		req.add_header('User-Agent', HEADER)
		content=urllib2.urlopen(req)
		url=content.geturl()
		content.close()
		play_video(name,url)
			
def play_video(name,url):
	g_thumbnail = xbmc.getInfoImage( "ListItem.Thumb" )
	listitem=xbmcgui.ListItem(name ,iconImage="DefaultVideo.png", thumbnailImage=g_thumbnail)
	xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER).play(str(url), listitem)
	xbmc.sleep(200)
	
def clean(name):
	remove=[('&amp;','&'),('&quot;','"'),('<em>',''),('</em>',''),('&#39;','\'')]
	for trash, crap in remove:
		name=name.replace(trash,crap)
	return name
	
def clean_file(name):
    remove=[(':',' - '),('\"',''),('|',''),('>',''),('<',''),('?',''),('*','')]
    for old, new in remove:
        name=name.replace(old,new)
    return name

def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param

params=get_params()
mode=None
name=None
url=None
page=0
try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass
try:
        page=int(params["page"])
except:
        pass

if mode==None:
	main()
elif mode==0:
	runKeyboard()
elif mode==1:
	showList(url, name)
elif mode==2:
	get_tags(url, name)
elif mode==3:
	get_trailer(url, name)
elif mode==4:
	get_film(url, name)
elif mode==5:
	get_top(url, name)
elif mode==6:
	coming_soon(url,name)
