#!/usr/bin/env python3
# @File:ReturnFunction.py
# @Date:2018/09/01
# Author:Cat.1
import copy
from project.Library import Error
from project.Module import ReturnStatus
from project.Module import RetDataModule


class songList(object):
    """部分请求参数说明
    
    Data是你请求音乐平台得到的json，但是需要自主解包成list后传入，songName，artistsName，idName是对应的键值，即key

    """
    def __init__(self, Data: list, songdir: str, artistsdir: str, iddir: str) -> list:
        self.Data       = Data
        self.songdir    = songdir
        self.artistsdir = artistsdir
        self.iddir      = iddir


    def buidingSongList(self):
        self.songList = []
        tmpSongMod    = copy.deepcopy(RetDataModule.mod_search_song)
        assert(eval("self.Data[0]" + self.songdir), 'PARAMS Error!')
        self.count = 0
        for item in self.Data:
            tmpSongMod['music_name'] = eval("item" + self.songdir)
            tmpSongMod['artists']    = eval("item" + self.artistsdir)
            tmpSongMod['id']         = eval("item" + self.iddir)
            self.songList.append(copy.deepcopy(tmpSongMod))
            self.count += 1
        return 0


    def CountSong(self):
        return self.count

    def ReturnList(self):
        return self.songList

    def ClearSongList(self):
        self.songList = []
        return self.songList



class RetDateModuleFunc(object):



    def __init__(self):
        self.re_dict = None


    def RetDateModSearch(self, now_page: int, next_page: int, before_page: int, songList: list, 
                         totalnum: int, code=200, status='Success') -> dict:
        """部分返回参数说明
        
        code -> 请求状态码，参阅ReturnStatus, status -> 详细状态，以str方式提供, now_page -> 当前用户请求的页码，用于翻页, 
        songList -> 一种特定的list，主要用来返回规定的歌曲候选列表, totalnum -> 返回的总歌曲数量
        """

        self.re_dict                     = copy.deepcopy(RetDataModule.mod_search)
        self.re_dict['code']             = code
        self.re_dict['status']           = status
        self.re_dict['now_page']         = now_page
        self.re_dict['next_page']        = next_page
        self.re_dict['before_page']      = before_page
        self.re_dict['song']['list']     = songList.ReturnList()
        self.re_dict['song']['totalnum'] = songList.count

        return self.re_dict


    def RetDateModSong(self, play_url: str, music_id: str, music_name: str, artists: str, image_url: str, 
                       lyric: str, comment: list, tlyric='None',  code=200, status='Success') -> dict:
        """部分返回参数说明
        
        code -> 请求状态码，参阅ReturnStatus, status -> 详细状态，以str方式提供, 
        play_url -> 音乐地址, music_id -> 音乐唯一识别码, lyric -> 歌词信息, tlyric -> 翻译歌词信息
        """
        assert(isinstance(comment, list), 'comment type is list ?')

        self.re_dict              = copy.deepcopy(RetDataModule.mod_song)
        self.re_dict['code']      = code
        self.re_dict['status']    = status
        self.re_dict['play_url']  = play_url
        self.re_dict['music_id']  = music_id
        self.re_dict['lyric']     = lyric
        self.re_dict['tlyric']    = tlyric
        self.re_dict['artists']   = artists
        self.re_dict['image_url'] = image_url
        self.re_dict['comment']   = comment

        return self.re_dict


    def RetDateModCdlist(self, dissname: str, nickname: str, info: str, dissid: str, image_url: str, 
                         songList: songList, totalnum: int, curnum: int, code=200, status="Success") -> dict:

        assert(len(songList.count)    == totalnum, "songList.totalnum != totalnum")
        assert(type(code)                == int, "code type is int ?")

        self.re_dict                     = copy.deepcopy(RetDataModule.mod_cdlist)
        self.re_dict['info']             = info
        self.re_dict['dissid']           = dissid
        self.re_dict['dissname']         = dissname
        self.re_dict['nickname']         = nickname
        self.re_dict['image_url']        = image_url
        self.re_dict['song']['list']     = songList.ReturnList()
        self.re_dict['song']['totalnum'] = songList.count
        self.re_dict['song']['curnum']   = curnum
        self.re_dict['code']             = code
        self.re_dict['status']           = status

        return self.re_dict

    def RetDateModHotItem(self, item_id: str, item_name: str, item_desc: str, code=200, status='Success') -> dict:
        assert(type(code)         == int, "code type is int ?")        
        self.re_dict              = copy.deepcopy(RetDataModule.mod_hot_item)
        self.re_dict['item_id']   = item_id
        self.re_dict['item_name'] = item_name
        self.re_dict['item_desc'] = item_desc
        self.re_dict['status']    = status
        self.re_dict['code']      = code

        return self.re_dict

    def RetDateModHotItemList(self, ItemList: list, totalitem: int, code=200, status='Success') -> dict:
        assert(type(code)         == int, "code type is int ?")        
        assert(len(ItemList)      == totalnum, "ItemList.totalnum != totalnum")
        self.re_dict              = copy.deepcopy(RetDataModule.mod_hot_item_list)
        self.re_dict['totalitem'] = totalitem
        self.re_dict[itemlist]    = ItemList
        self.re_dict['code']      = code
        self.re_dict['status']    = status

