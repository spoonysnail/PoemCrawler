
#coding=utf-8
import urllib2,re
import HTMLParser
from sgmllib import SGMLParser

base_url = "http://www.gushiwen.org"
tangurl = 'http://www.gushiwen.org/gushi/quantang.aspx'
songurl = 'http://www.gushiwen.org/gushi/quansong.aspx'

class MyParser(SGMLParser):
    def __init__(self):
        SGMLParser.__init__(self)
        self.is_linkDiv = False
        self.is_link = False

        self.is_img = False
        #self.guwendivcont = []

        # 全唐诗/全宋词 链接 列表
        self.linkList = []
        # 全唐诗/全宋词 链接对应描述 列表
        self.linkDescList = []

        self.is_contDiv = False
        self.is_tangshiBr = False

        self.is_songciP = False

        self.tangshiCont = []
        self.songciCont = []
        self.singleSongciCont = ''

    def start_div(self, attrs):
        for k,v in attrs:
            # 找到 全唐诗/全宋词 各链接 所在div
            if str(k).strip() == 'class' and str(v).strip() == 'guwencont2':
                #print 'gewendiv '
                self.is_linkDiv = True
                return

            # 找到 唐诗/宋词 内容 所在div
            if str(k).strip() == 'class' and str(v).strip() == 'authorShow':
                #print 'gewendiv '
                self.is_contDiv = True
                return

    def end_div(self):
        self.is_linkDiv = False

    def start_br(self, attrs):
        if self.is_contDiv is True:
            self.is_tangshiBr = True

    def end_br(self):
        self.is_tangshiBr = False

    def start_p(self, attrs):
        if self.is_contDiv is True:
            self.is_songciP = True

    def end_p(self):
        self.is_songciP = False

    def start_a(self, attrs):
        for k,v in attrs:
            # 找到 全唐诗/全宋词 所有链接。
            if self.is_linkDiv is True and str(k).strip() == 'href':
                self.is_link = True
                self.linkList.append(str(v).strip())
                return
            if self.is_songciP is True and str(k).strip() == 'title':
                self.singleSongciCont += str(v).strip()

    def end_a(self):
        self.is_link = False

    def start_img(self, attrs):
        for k,v in attrs:
            # 找到 全唐诗/全宋词 所有链接。
            if self.is_songciP is True and str(k).strip() == 'title':
                self.singleSongciCont += str(v).strip()

    def end_img(self):
        self.is_img = False

    def handle_data(self, text):
        if self.is_link is True:
            if not not str(text).strip():
                self.linkDescList.append(str(text).strip())
        if self.is_tangshiBr is True:
            if not not str(text).strip():
                #print "handledata:" ,str(text)
                self.tangshiCont.append(str(text).replace('　', '')+' ')

        if self.is_songciP is True:
            if not not str(text).strip():
                self.singleSongciCont += (str(text).replace('　', ''))
                #self.songciCont.append(str(text).replace('　', '')+' ')

        if self.is_songciP is False:
            if not not str(self.singleSongciCont).strip():
                self.songciCont.append(self.singleSongciCont.strip().replace('　', '') + ' ')
                # if len(str(self.singleSongciCont).strip()) < 100:
                #     print len(self.singleSongciCont.strip()), self.singleSongciCont.strip()
                # if self.singleSongciCont.find('（') > -1:
                #     print len(self.singleSongciCont.strip()), self.singleSongciCont.strip()
                # if len(self.singleSongciCont.split('（')[0]) < 30 and len(self.singleSongciCont) < 120:
                #     print len(self.singleSongciCont.split('（')[0]),len(self.singleSongciCont.strip()), self.singleSongciCont.strip()
                self.singleSongciCont = ''



# def contHandle(cont):
#     if cont.find('，') > -1 or cont.find('。') > -1:
#         #print "contHandle: ",cont.strip().replace('　', '').replace(' ','')
#         return cont.strip().replace('　', '').replace(' ','')+' '
#     return cont+' '


def tangshiContHandle(tangshiContList, tangshiContTitle):
    #tangshiSplitList = []
    realSlitStr = tangshiContTitle
    print tangshiContTitle
    if int(tangshiContTitle[3:7]) < 100:
        realSlitStr = '卷' + str(int(tangshiContTitle[4:7]))
    print 'realSlitStr: ',realSlitStr
    tangshiSplitList = ' '.join(tangshiContList).split(realSlitStr)

    return tangshiSplitList


def songciContHandle(songciContList):
    # tangshiSplitList = []
    res = []
    # if len(songciContList) % 2 is not 1:
    #     print '按非正常顺序排列'
    #     return []

    # for i in range(0, len(songciContList)/2):
    #     # [宋词名， 内容， 作者]
    #     songciTmp = [songciContList[2*i + 1],  songciContList[2*i + 2].replace('  ',''), songciContList[0].replace(' ','')]
    #     res.append(songciTmp)

    songciTmp = []
    songciTitleTmp = ''
    songciContTmp = ''
    for i in range(1, len(songciContList)):
        # [宋词名， 作者， 内容]

        if len(songciContList[i].split('（')[0]) < 30 and len(songciContList[i]) < 120:
            songciTitleTmp = songciContList[i].replace(' ','')
            if len(songciTmp) is not 0:
                songciTmp.append(songciContTmp)
                res.append(songciTmp)
            songciTmp = []
            songciContTmp = ''
        elif not not songciTitleTmp.strip() and songciContList[i].find('●') > -1 :
            songciTitleTmp += str(songciContList[i]).split(' ')[0]
            songciTmp.append(songciTitleTmp)
            songciTmp.append(songciContList[0].replace(' ', ''))
            songciContTmp += str(songciContList[i]).split(' ')[1]
        else:
            if not not songciTitleTmp.strip():
                songciTmp.append(songciTitleTmp)
                songciTmp.append(songciContList[0].replace(' ',''))
            songciTitleTmp = ''
            songciContTmp += songciContList[i].replace(' ','')

    songciTmp.append(songciContTmp)
    res.append(songciTmp)


    return res




# content = urllib2.urlopen(songurl).read()
# #print content
# parser = MyParser()
# parser.feed(content)
# print len(parser.linkList)
# print len(parser.linkDescList)
#
# tmp = '/wen_2013.aspx'
#
# guwenPage = urllib2.urlopen(base_url+tmp).read()
# parser.feed(guwenPage)
# #print guwenPage
# i = 0
# # for item in (parser.songciCont):
# #      print item
# for item in songciContHandle(parser.songciCont):
#     print item[0], item[1], item[2]

# res = tangshiContHandle(parser, '卷101')
# for item in res:
#     print 'item',item
#     if not not item.strip():
#         tmps = re.split('「|」', item)
#         s = tmps[:2]
#         tmpa = tmps[2].split(' ')
#         for tmp in tmpa:
#             if not tmp.strip():
#                 tmpa.remove(tmp)
#         #print 'len(tmpa[0])',len('佚名')
#         if len(tmpa[0]) <= 4*3:
#             s.append(tmpa[0])
#             s.append(''.join(tmpa[1:len(tmpa)]))
#         else:
#             s.append(''.join(tmpa))
#         #print 'len(tmpa):',len(tmpa)
#
#         #print 'len(s)',len(s)
#         for i in s:
#             if not i.strip():
#                 s.remove(i)
#         if len(s) is 3:
#             s.insert(2, '佚名')
#             #print 'length 3'
#
#         for i in s:
#             print i
# # for item in parser.linkList:
# #     print base_url+item
# #     guwenCont = urllib2.urlopen(myurl+item).read()
# #     print guwenCont
# #     print item
#
