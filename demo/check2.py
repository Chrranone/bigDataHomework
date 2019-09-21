from gensim import corpora,models,similarities
import jieba
import pymysql
import re

#db = pymysql.connect("localhost","root","ccrr123cc","bigdata" )

def getContent(db):
    contentList = []
    content = []
    cursor = db.cursor()
    sql = "SELECT id,content FROM content"
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            content.append(row[0])
            content.append(row[1])
            contentList.append(content)
            content = []
    except:
        print('查询失败')
    return contentList

def check(content,db):
    contentList = getContent(db)
    #print(type(contentList[0][1]))
    all_list = []
    for row in contentList:
        all_list.append(row[1])

    cut_list = []
    for doc in all_list:
        doc_list = [word for word in jieba.cut(doc)]
        cut_list.append(doc_list)

    #print(cut_list)

    cut_content = [word for word in jieba.cut(content)]

    dictionary = corpora.Dictionary(cut_list)

    dictionary.keys()
    #dictionary.token2id
    corpus = [dictionary.doc2bow(doc) for doc in cut_list]
    cut_content_vrc = dictionary.doc2bow(cut_content)

    tfidf = models.TfidfModel(corpus)
    #tfidf[cut_content_vrc]
    index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=len(dictionary.keys()))
    sim = index[tfidf[cut_content_vrc]]
    #result = list(sim)
    result = list(map(float,sim))
    return result
    #print(type(result[1]))

def getContent_id(id,db):
    cursor = db.cursor()
    id = id + 1
    sql = 'SELECT name,content FROM content where id = ' + str(id)
    try:
        cursor.execute(sql)
        result = cursor.fetchone()
        #print(result)
        result2 = []
        result2.append(result[0])
        result2.append(result[1])
        return result2
        #print(result[0])
        #print(result[1])
    except:
        print("查询失败")

def check2(content,text):
    print(text)

    pattern = r';|!|。|；|'
    doc = text
    #pattern = r',|/|;|\[|\]|\?|\{|\}|\~|!|@|#|\$|%|\^|&|-|=|\_|，|。|；|‘|’|【|】|·|！| |…|'
    text_all = re.split(pattern,text)
    print(text_all)

    cut_list = []
    for doc in text_all:
        doc_list = [word for word in jieba.cut(doc)]
        cut_list.append(doc_list)

    #print(cut_list)

    cut_content = [word for word in jieba.cut(content)]

    dictionary = corpora.Dictionary(cut_list)

    dictionary.keys()
    #dictionary.token2id
    corpus = [dictionary.doc2bow(doc) for doc in cut_list]
    cut_content_vrc = dictionary.doc2bow(cut_content)

    tfidf = models.TfidfModel(corpus)
    #tfidf[cut_content_vrc]
    index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=len(dictionary.keys()))
    sim = index[tfidf[cut_content_vrc]]
    #result = list(sim)
    result = list(map(float,sim))
    print(result)
    result2 = []
    for i in range(len(result)):
        a = []
        if result[i] > 0.2 :
            a.append(result[i])
            a.append(text_all[i])
            result2.append(a)

    print(result2)
    return result2

def main(word):
    #word待查文章
    db = pymysql.connect("localhost","root","ccrr123cc","bigdata" )
    content = word
    result = check(content,db)
    result2 = getContent_id(int(result.index(max(result))),db)
    result2.append(max(result))
    #print(content)

    result3 = check2(content,result2[1])
    result3.append(result2)


    #最相似的文章 名称+内容+相似度
    #print(result2)
    db.close()
    return result3

