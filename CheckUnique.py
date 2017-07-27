#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import leancloud
import xlrd

reload(sys)
sys.setdefaultencoding('utf8')
leancloud.init('app_id', 'app_key', 'master_ley')
# 如果需要使用 master key 权限访问 LeanCLoud 服务，请将这里设置为 True
leancloud.use_master_key(True)



def checkClass(className, attrName):
    uniqueObjIdList = []
    uniqueContList = []

    Obj = leancloud.Object.extend(className)
    query = leancloud.Query(Obj)

    query.ascending('createdAt')

    query.limit(1000)

    query_list = query.find()
    print len(query_list)
    cnt = len(query_list)
    size = 1000
    repeatedDataCnt = 0
    while(cnt>0):

        for obj in query_list:
            cont = obj.get(attrName)
            objId = obj.get('objectId')
            if cont not in uniqueContList:
                uniqueObjIdList.append(objId)
                uniqueContList.append(cont)
            else:
                existId = uniqueObjIdList[uniqueContList.index(cont)]
                # 已存在数据ID，重复ID，重复内容
                print 'repeated:', existId, objId, cont
                repeatedDataCnt += 1

        query = leancloud.Query(Obj)
        query.ascending('createdAt')

        query.skip(size)
        size += 1000
        query.limit(1000)
        query_list = query.find()
        print len(query_list)
        cnt = len(query_list)

    print 'check end!'


def handleRepeatation(className, repeatationInfo):
    Obj = leancloud.Object.extend(className)

    workbook = xlrd.open_workbook(repeatationInfo, encoding_override='utf-8')
    booksheet = workbook.sheet_by_name(workbook.sheet_names()[0])
    print 'handle begin'
    for row in range(booksheet.nrows):
        existedId = getCellVal(booksheet.cell(row, 0))
        repeatedId = getCellVal(booksheet.cell(row, 1))
        query = leancloud.Query(className)
        #print existedId,repeatedId

        # 这里填入需要查询的 objectId
        try:
            existObj = query.get(existedId)
            existObjAttr = [existObj.get('author'), existObj.get('name'), existObj.get('content')]
            repeatedObj = query.get(repeatedId)
            repeatedObjAttr = [repeatedObj.get('author'), repeatedObj.get('name'), repeatedObj.get('content')]

            print repeatedObj.get('author'),existObj.get('author')
            if repeatedObj.get('author') == '佚名' and existObj.get('author') is not '佚名':
                # acl = leancloud.ACL()
                # acl.set_public_read_access(True)
                # acl.set_write_access(user.)  # 这里设置某个 user 的写权限
                #
                # # 将 ACL 实例赋予 Post 对象
                # repeatedObj.set_acl(acl)
                # repeatedObj.save()
                repeatedObj.destroy()
                print 'Delete', 'repeatedObj: ', ' '.join(repeatedObjAttr)
                continue

            if existObj.get('author') == '佚名' and repeatedObj.get('author') is not '佚名':
                existObj.destroy()
                print 'Delete', 'existObj: ', ' '.join(existObjAttr)

        except Exception,e:
            print e


def getAttr(Object, attr_name):
    if Object.get(attr_name) == None:
        return ''
    return Object.get(attr_name)


def getCellVal(cell):
    val = cell.value
    val.encode('utf8')
    return str(val).strip()
checkClass('Tangshi','content')
#handleRepeatation('Tangshi', '/users/gejiali/Documents/Game/Poem/RepeatedTangshi.xlsx')
