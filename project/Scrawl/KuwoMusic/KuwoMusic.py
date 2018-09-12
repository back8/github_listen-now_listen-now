# -*- coding: utf-8 -*-
# __date__ 2018/7/29
# __file__ KuwoMusic
# __author__ Msc


import simplejson
from Module import ReturnStatus
from Module import RetDataModule
from Module import ReturnFunction
from lxml import etree
import requests
import copy
import json

class KuwoMusic(object):
    '''
        酷我音乐
    '''
    
    global null
    null=''
    re_dict = copy.deepcopy(RetDataModule.mod_search)
    def __init__(self):
        self.baseurl    = "http://search.kuwo.cn/r.s?all=%s&ft=music&itemset=web_2018&client=kt&pn=%s&rn=10&rformat=json&encoding=utf8"
        self.searchurl  = "http://m.kuwo.cn/newh5/singles/songinfoandlrc?musicId=%s"
        self.palyurl    = "http://antiserver.kuwo.cn/anti.s?type=convert_url&rid=%s&format=aac|mp3&response=url"
        self.commenturl = "http://comment.kuwo.cn/com.s?type=get_comment&uid=0&prod=newWeb&digest=15&sid=%s&page=1&rows=10&f=web"
        self.songlisturl = "http://yinyue.kuwo.cn/yy/cinfo_%s.htm"
        self.session = requests.session()
        self.headers    = {
                    #"Content-Length": '11818',
                    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
                    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
                    }


    def Search_List(self, keyword, page=1):

        re_dict = copy.deepcopy(RetDataModule.mod_search)

        try:
            page -= 1
            resp = eval(self.session.get(url=self.baseurl%(keyword, page), headers=self.headers).text)

        except simplejson.errors.JSONDecodeError:
            code   = ReturnStatus.ERROR_SEVER
            status = "ReturnStatus.ERROR_SEVER"
            
        if resp["HIT"] != 0 :
            songList               = ReturnFunction.songList(Data=resp["abslist"], songdir="[\"SONGNAME\"]",artistsdir="[\"ARTIST\"]",iddir="[\"MUSICRID\"][6:]", page=page)
            songList.buidingSongList()
            re_dict_class          = ReturnFunction.RetDataModuleFunc()
            now_page               = page + 1
            before_page, next_page = page , page +2
            totalnum               = songList.count
            re_dict                = re_dict_class.RetDataModSearch(now_page, next_page, before_page, songList, totalnum, code=ReturnStatus.SUCCESS, status='Success')
            
            return re_dict



    def Search_details(self, music_id):

        try:
            resp = eval(self.session.get(url=self.searchurl%(music_id),headers=self.headers).text)
        except simplejson.errors.JSONDecodeError:
            code   = ReturnStatus.ERROR_SEVER
            status = "ReturnStatus.ERROR_SEVER"
            return 0
        else:
            code   = ReturnStatus.SUCCESS
            status = "ReturnStatus.SUCCESS"

            try:
                resp = resp["data"]
                lyric = str(resp['lrclist'])
                thelist = ['0','1','2','3','4','5','6','7','8','9']
                while lyric[-5:-4]  in thelist:
                        lyric = str(resp['lrclist'])
                lyric = lyric.replace("[{'time': '","[").replace("', 'lineLyric': '","]").replace("'}, {'time': '","\n[")[:-3]

                re_dict_class = ReturnFunction.RetDataModuleFunc()
                re_dict       = re_dict_class.RetDataModSong(self.get_play_url(music_id), resp["songinfo"]["id"], resp["songinfo"]['songName'], 
                    resp["songinfo"]['artist'], resp["songinfo"]['pic'], lyric, self.get_comment(music_id), tlyric='None', 
                    code=code, status=status)
            
            except:re_dict["code"] = ReturnStatus.DATA_ERROR
        return re_dict


    def get_play_url(self,music_id):
        re_dict  = copy.deepcopy(RetDataModule.mod_song)

        play_url = "http://antiserver.kuwo.cn/anti.s?type=convert_url&rid={0}&format=aac|mp3&response=url".format(music_id)
        return play_url


    def get_comment(self,music_id):
        resp    = eval(self.session.get(url=self.commenturl%(music_id),headers=self.headers).text)
        comment = resp["rows"]
        return comment

    def get_songlist(self,list_id,page=1):
        try:
            resp = self.session.get(url=self.songlisturl%(list_id), headers=self.headers)
            resp = etree.HTML(resp.content)

        except simplejson.errors.JSONDecodeError:
            code   = ReturnStatus.ERROR_SEVER
            status = "ReturnStatus.ERROR_SEVER"
            return 0
        
        else:
            try:
                global re_dict
                re_dict = {}
                code = ReturnStatus.SUCCESS
                status = "ReturnStatus.SUCCESS"
                re_dict_class = ReturnFunction.RetDataModuleFunc()  

                songdir = resp.xpath('//li [@class="clearfix"]/p [@class="m_name"]/a/@title')
                artistsdir = resp.xpath('//p [@class="s_name"]/a/@title')
                iddir = resp.xpath('//input/@ mid') 

                dissname = str(resp.xpath('//div [@class="s_img"]/a/@title'))[2:-2]
                dissid = list_id
                info = str(resp.xpath('//*[@id="intro"]/text()'))[33:-2]
                image1 = str(resp.xpath('//div [@id="bdshare"]/@data')).find("pic")
                image2 = str(resp.xpath('//div [@id="bdshare"]/@data')).find("jpg")
                image = str(resp.xpath('//div [@id="bdshare"]/@data'))[image1+6:image2+3]
                total = str(resp.xpath('//*[@id="content"]/div/div[2]/div[4]/form/div[1]/p[2]/text()'))[3:-4]   

                
                list1 = []
                keys = ['music_name','id','artists']
                for i in range(int(total)):
                    values = [songdir[i],iddir[i],artistsdir[i]]
                    dict1 = dict(zip(keys,values))
                    list1.append(dict1) 
    

                re_dict = {'nickname':'', 'code':code, 'status':status, 'dissid':dissid, 'info':info, 'dissname':dissname, 'image': image, 'song':{'totalnum':total, 'curnum':total, 'list':list1}} 

            except:
                code = ReturnStatus.DATA_ERROR
                status = "ReturnStatus.DATA_ERROR"
                return ReturnStatus.DATA_ERROR
            else:
                re_dict['code']   = ReturnStatus.SUCCESS

        return re_dict



if __name__=="__main__":

    test = KuwoMusic()

    rest.Search_List("青花瓷",1)

