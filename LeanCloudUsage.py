#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import leancloud
import Crawler
import urllib2,re
reload(sys)
sys.setdefaultencoding('utf8')
leancloud.init("app_id", "app_key")

Tangshi = leancloud.Object.extend('TangShi')
Songci = leancloud.Object.extend('Songci')


def doTangshiCrawler():
    content = urllib2.urlopen(Crawler.tangurl).read()
    #print content
    parser = Crawler.MyParser()
    parser.feed(content)
    print len(parser.linkList)
    print len(parser.linkDescList)

    linkStrsList = parser.linkDescList
    linkList = parser.linkList
    ind = 0
    savedCnt = 0
    failedCnt = 0
    #len(linkList)
    for ind in range(581,len(linkList)):
        item = linkList[ind]
        print Crawler.base_url+item
        guwenPage = urllib2.urlopen(Crawler.base_url+item).read()
        newParser = Crawler.MyParser()
        newParser.feed(guwenPage)
        guwenContNow =newParser.tangshiCont
        guwenContJuan = linkStrsList[ind][:6]
        #print linkStrsList[ind], guwenContJuan
        res = Crawler.tangshiContHandle(guwenContNow, guwenContJuan)
        for item in res:
            if not not item.strip():
                try:
                    tangshi = Tangshi()
                    tangshi.set('allStr', guwenContJuan + item)
                    #print item

                    tmps = re.split('「|」', item.replace('【','「').replace('】','」'))
                    s = tmps[:2]
                    tmpa = tmps[2].split(' ')
                    for tmp in tmpa:
                        if not tmp.strip():
                            tmpa.remove(tmp)

                    if len(tmpa[0]) <= 5 * 3:
                        s.append(tmpa[0])
                        s.append(''.join(tmpa[1:len(tmpa)]))
                    else:
                        s.append(''.join(tmpa))
                    # print 'len(tmpa):',len(tmpa)

                    # print 'len(s)',len(s)
                    for i in s:
                        if not i.strip():
                            s.remove(i)
                    if len(s) is 3:
                        s.insert(2, '佚名')
                        # print 'length 3'

                    tangshi.set('category', guwenContJuan + s[0].strip())
                    tangshi.set('name', s[1].strip())
                    tangshi.set('author', s[2].strip())
                    tangshi.set('content', s[3].strip())
                    tangshi.save()
                    savedCnt += 1
                except Exception, e:
                    failedCnt += 1
                    #if str(e).find('LeanCloudError: [137] A unique field was given a value that is already taken.') is -1:
                    print e
                    print item, 'saving failed'
        #ind += 1

    print 'Tangshi Crawler End'
    print 'Saved: ', savedCnt
    print 'Failed:', failedCnt


def doSongciCrawler():
    content = urllib2.urlopen(Crawler.songurl).read()
    #print content
    parser = Crawler.MyParser()
    parser.feed(content)
    print len(parser.linkList)
    print len(parser.linkDescList)

    linkDescList = parser.linkDescList
    linkList = parser.linkList
    #ind = 0
    savedCnt = 0
    failedCnt = 0
    #len(linkList)
    for ind in range(83,len(linkList)):
        item = linkList[ind]
        print Crawler.base_url+item
        guwenPage = urllib2.urlopen(Crawler.base_url+item).read()
        newParser = Crawler.MyParser()
        newParser.feed(guwenPage)
        guwenContNow =newParser.songciCont

        res = Crawler.songciContHandle(guwenContNow)
        for item in res:
            if len(item) > 0:
                try:
                    songci = Songci()
                    songci.set('allStr', ' '.join(item))
                    songci.set('category', linkDescList[ind].strip())
                    songci.set('name', item[0].strip())
                    songci.set('author', item[1].strip())
                    songci.set('content', item[2].strip())
                    songci.save()
                    savedCnt += 1
                except Exception, e:
                    failedCnt += 1
                    #if str(e).find('LeanCloudError: [137] A unique field was given a value that is already taken.') is -1:
                    print e
                    print ' '.join(item), 'saving failed'
        #ind += 1

    print 'Songci Crawler End'
    print 'Saved: ', savedCnt
    print 'Failed:', failedCnt


doTangshiCrawler()
#doSongciCrawler()