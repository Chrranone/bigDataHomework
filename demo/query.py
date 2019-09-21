import pymysql
import re

#db = pymysql.connect("localhost","root","ccrr123cc","bigdata" )

def querys(word,db):
    cursor = db.cursor()
    idList = []
    sql = "SELECT * FROM keywords"

    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            id = row[1]
            key = row[2]

            s = "(\D+)\s(\D+)\s(\D+)\s(\D+)\s(\D+)"
            key2 = re.match(s,key)
            #for i in range(5):
                #print(key2.group(i))
            if word in key :
                idList.append(id)
            elif key2.group(1) in word:
                idList.append(id)
            elif key2.group(2) in word:
                idList.append(id)
            elif key2.group(3) in word:
                idList.append(id)
            elif key2.group(4) in word:
                idList.append(id)
            elif key2.group(5) in word:
                idList.append(id)
            #print("id = %s ,key = %s" % (id,key))
    except:
        print("数据查询失败")
    return idList


def getcontent(idList,db):
    contentList = []
    content = []
    cursor = db.cursor()
    for i in idList:
        sql = "SELECT id,name,content FROM content WHERE id = %s" % (int(i))
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
            for row in result:
                content.append(row[0])
                content.append(row[1])
                #content.append(row[2])
        except:
            print('查询失败')
        contentList.append(content)
        content = []

    return contentList


def main(word):
    db = pymysql.connect("localhost","root","ccrr123cc","bigdata" )
    kword = word
    idList = querys(kword,db)
    #print(idList)
    #模糊检索结果列表
    contentList = getcontent(idList,db)
    #print(contentList)
    #print(len(contentList))

    db.close()
    return contentList