from django.shortcuts import render
from django.shortcuts import render_to_response ,get_object_or_404,render,redirect
import pymysql
from . import query , check2,makedoc


def xinxi_list(request):
    db = pymysql.connect("localhost","root","ccrr123cc","bigdata" )
    cursor = db.cursor()
    sql = "select id,name from content"
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
    except:
        print("查询失败")
    re = list(result)
    nameList = []
    idList = []
    for row in result:
        nameList.append(row[1])
        idList.append(row[0])
    context = {}
    context['xinxis'] = result
    context['ids'] = idList

    #信息类型
    type_all = []

    type_one = []
    type_one.append(0)
    type_one.append('热词')
    type_all.append(type_one)
    type_one = []
    type_one.append(1)
    type_one.append('概念')
    type_all.append(type_one)
    type_one = []
    type_one.append(2)
    type_one.append('技术')
    type_all.append(type_one)
    type_one = []
    type_one.append(3)
    type_one.append('法律')
    type_all.append(type_one)

    context['type'] = type_all

    db.close()
    return render_to_response('xinxi_list.html',context)

def xinxi_type(request,id):
    context={}
    #读取主键值相同的类的内容
    db = pymysql.connect("localhost","root","ccrr123cc","bigdata" )
    cursor = db.cursor()
    sql = ""
    xinxi_id = int(id)
    if xinxi_id == 0:
        sql = "select id,name from content WHERE isHot = 1"
    if xinxi_id == 1:
        sql = "select id,name from content WHERE isConcept = 1"
    if xinxi_id == 2:
        sql = "select id,name from content WHERE isScience = 1"
    if xinxi_id == 3:
        sql = "select id,name from content WHERE isLaw = 1"
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
    except:
        print("查询失败")

    nameList = []
    idList = []
    for row in result:
        nameList.append(row[1])
        idList.append(row[0])
    context = {}
    context['xinxis'] = result
    context['ids'] = idList


    #类型列表
    #信息类型
    type_all = []

    type_one = []
    type_one.append(0)
    type_one.append('热词')
    type_all.append(type_one)
    type_one = []
    type_one.append(1)
    type_one.append('概念')
    type_all.append(type_one)
    type_one = []
    type_one.append(2)
    type_one.append('技术')
    type_all.append(type_one)
    type_one = []
    type_one.append(3)
    type_one.append('法律')
    type_all.append(type_one)

    context['type'] = type_all

    db.close()
    return render(request,'xinxi_type.html',context)



def xinxi_detail(request,id):
    db = pymysql.connect("localhost","root","ccrr123cc","bigdata" )
    cursor = db.cursor()
    sql = "select name,content from content where id ="+str(id)
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
    except:
        print("查询失败")
    context = {}
    context['xinxi'] = result
    return render_to_response('xinxi_detail.html',context)



def xinxi_query(request):
    context = {}
    guanjianzi = request.POST.get('guanjianzi')

    if guanjianzi != None:
        result = query.main(guanjianzi)
        context['xinxis'] = result
        return render(request, 'xinxi_query.html', context)

    return render(request,'xinxi_query.html')

def xinxi_check(request):
    context = {}
    guanjianzi = request.POST.get('guanjianzi')

    if guanjianzi != None:
        result = check2.main(guanjianzi)

        context['xinxi'] = result[-1]
        #print(context['xinxi'])
        context['name'] = result[-1][0]
        context['content'] = result[-1][1]
        context['num'] = result[-1][2]
        context['text'] = guanjianzi

        context['par'] = result[0:len(result)-1]
        print('********')
        print(context['par'])
        print('********')

        '''context['xinxi'] = result
        #print(context['xinxi'])
        context['name'] = result[0]
        context['content'] = result[1]
        context['num'] = result[2]
        context['text'] = guanjianzi'''
        makedoc.make(context)
        return render(request, 'xinxi_check.html', context)

    return render(request,'xinxi_check.html')

