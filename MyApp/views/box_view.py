from django.shortcuts import render,HttpResponse
from MyApp import models
from MyApp.utils.pagination import Pagination
from MyApp.utils.encrypt import md5
from django.views.decorators.csrf import csrf_exempt
from django import forms
from django.http import JsonResponse
from MyApp.utils.bootstrap import BootStrapModelForm,BootStrapForm
import datetime
from collections import defaultdict
import pandas as pd
from decimal import Decimal

def actor_movie_box():
    data_obj = models.movie_box.objects.all()
    data = {}
    for item in data_obj:
        directors = item.director.split('/')
        actors = item.actors.split('/')
        for director in directors:
            if director not in data:
                data[director]={}
            for actor in actors:
                if actor not in data[director]:
                    data[director][actor] = [item.box,1]
                else:
                    data[director][actor][0] +=item.box
                    data[director][actor][1] += 1
    data_list = []
    for director,actors in data.items():
        for actor,box in actors.items():
            data_list.append((director,actor,box[0],box[1]))
    data_sorted = sorted(data_list,key=lambda x:-x[2])
    print(data_sorted)
    return data_sorted[:50]

def box_view_home(request):
    '''数据分析页面'''
    years = [i for i in range(2012,2024)]
    years.append('2012-2023')
    years.reverse()
    act_obj = models.movie_box.objects.all().values_list('actors',flat=True)
    act_obj = list(act_obj)
    actors = [actor for item in act_obj for actor in item.split('/')]
    actors = list(set(actors))
    context ={
        'years':years,
        'actors':actors,
        'table_4':actor_movie_box(),
    }
    return render(request,'box_view_home.html',context)
# 获取票房去重数据
def get_unique_box(data):
    unique_box = {}
    for item in data:
        movie_name = item.movie_name
        box  = item.box
        if movie_name not in unique_box:
            unique_box[movie_name] = box
        else:
            unique_box[movie_name] += box
    return unique_box

# 电影票房排行榜
def pic_1_1(text,year):
    if year == '2012-2023':
        data = models.movie_box.objects.all()
    else:
        year = int(year)
        data = models.movie_box.objects.filter(year=year)
    unique_box = get_unique_box(data)
    unique_box_sorted = sorted(unique_box.items(),key=lambda x:-x[1])
    unique_box_sorted = unique_box_sorted[:10]
    movie_names = [item[0] for item in unique_box_sorted]
    boxes = [item[1] for item in unique_box_sorted]
    legend = ["柱状图", "折线图"]
    series_list = [
        {
            "name": '柱状图',
            "type": 'bar',
            "data": boxes,
            'label':{
                'show':True,
                'position':'inside',
                "formatter": "{c}"+'万元',  # 自定义标签格式，使用 {b} 表示类目轴（X 轴）的数值
            },
        },
        {
            "name": '折线图',
            "type": 'line',
            'label':{
                'show':True,
                'position':'top',
                "formatter": "{b}",  # 自定义标签格式，使用 {b} 表示类目轴（X 轴）的数值
            },
            "data": boxes,
        }
    ]
    data = {
        'title':{
            'textAlign':"auto",
            'left':'center',
            'text':text,
        },
        'toolbox':{
            'show': True,
            'feature': {
                'mark': {'show': True},
                'dataView': {'show': True, 'readOnly': False},
                'restore': {'show': True},
                'saveAsImage': {'show': True}
            }
        },
        'tooltip':{
            'show': True,
            'feature': {
                'mark': {'show': True},
                'dataView': {'show': True, 'readOnly': False},
                'restore': {'show': True},
                'saveAsImage': {'show': True}
            }
        },
        'legend':{
            'data':legend,
            'bottom':0,
        },
        'xAxis':{
            'data':movie_names,
            'axisLabel':{
                'interval':1,
                'position':'top',
            },
        },
        'yAxis':{
            'axisLabel': { 
                'formatter': '{value} 万元', 
                'color': '#333',  
                'fontSize': 12,  
                'fontWeight': 'bold',
            },
        },
        'series':series_list,

    }
    result = {
        "status": True,
        "data": data,
    }
    return JsonResponse(result)

# 演员票房排行榜
def pic_1_2(text,year):
    if year == '2012-2023':
        data = models.movie_box.objects.all()
    else:
        year = int(year)
        data = models.movie_box.objects.filter(year=year)
    data_dict = {}
    for item in data:
        actors = item.actors.split('/')
        for actor in actors:
            if actor not in data_dict:
                data_dict[actor] = item.box
            else :
                data_dict[actor] += item.box
    data_sorted = sorted(list(data_dict.items()),key=lambda x:-x[1])
    data_sorted = data_sorted[:10]
    actors = [item[0] for item in data_sorted]
    boxes = [item[1] for item in data_sorted]
    legend = ["柱状图", "折线图"]
    series_list = [
        {
            "name": '柱状图',
            "type": 'bar',
            "data": boxes,
            'label':{
                'show':True,
                'position':'inside',
                "formatter": "{c}"+'万元',  # 自定义标签格式，使用 {b} 表示类目轴（X 轴）的数值
            },
        },
        {
            "name": '折线图',
            "type": 'line',
            'label':{
                'show':True,
                'position':'top',
                "formatter": "{b}",  # 自定义标签格式，使用 {b} 表示类目轴（X 轴）的数值
            },
            "data": boxes,
        }
    ]
    series_list = [
        {
            "name": '柱状图',
            "type": 'bar',
            "data": boxes,
            'label':{
                'show':True,
                'position':'inside',
                "formatter": "{c}"+'万元',  # 自定义标签格式，使用 {b} 表示类目轴（X 轴）的数值
            },
        },
        {
            "name": '折线图',
            "type": 'line',
            'label':{
                'show':True,
                'position':'top',
                "formatter": "{b}",  # 自定义标签格式，使用 {b} 表示类目轴（X 轴）的数值
            },
            "data": boxes,
        }
    ]
    data = {
        'title':{
            'textAlign':"auto",
            'left':'center',
            'text':text,
        },
        'tooltip':{},
        'toolbox':{
            'show': True,
            'feature': {
                'mark': {'show': True},
                'dataView': {'show': True, 'readOnly': False},
                'restore': {'show': True},
                'saveAsImage': {'show': True}
            }
        },
        'legend':{
            'data':legend,
            'bottom':0,
        },
        'xAxis':{
            'data':actors,
            'axisLabel':{
                'interval':1,
                'position':'top',
            },
        },
        'yAxis':{
            'axisLabel': { 
                'formatter': '{value} 万元', 
                'color': '#333',  
                'fontSize': 12,  
                'fontWeight': 'bold',
            },
        },
        'series':series_list,

    }
    result = {
        "status": True,
        "data": data,
    }
    return JsonResponse(result)     

# 各类型票房占比
def pic_1_3(text,year):
    if year == '2012-2023':
        data = models.movie_box.objects.all()
    else:
        year = int(year)
        data = models.movie_box.objects.filter(year=year)
    data_dict = {}
    for item in data:
        genre = item.main_genre
        if genre not in data_dict:
            data_dict[genre] = item.box
        else :
            data_dict[genre] += item.box
    data_sorted = sorted(list(data_dict.items()),key=lambda x:-x[1])
    genres = [item[0] for item in data_sorted]
    boxes = [item[1] for item in data_sorted]

    # 构建带有原始值的数据项
    data_items = [{'value': value, 'name': name} for value, name in zip(boxes,genres)]
    data = {
        'title':{
            'textAlign':"auto",
            'left':'left',
            'text':text,
        },
        'legend': {
            'left': 'left',  # 设置图例在左侧
            'top': 'middle',  # 设置图例在中间
            'orient': 'vertical',  # 设置图例竖直显示
        },
        'toolbox': {
            'show': True,
            'feature': {
                'mark': {'show': True},
                'dataView': {'show': True, 'readOnly': False},
                'restore': {'show': True},
                'saveAsImage': {'show': True}
            }
        },
        'tooltip': {  # 配置 tooltip
            'trigger': 'item',  # 触发类型为 item
            'formatter': '{a} <br/>{b} : {c}万元 ({d}%)',
        },
        'series': [
            {
                'name': '票房合计',
                'type': 'pie',
                'radius': [50, 250],
                'center': ['50%', '50%'],
                'roseType': 'area',
                'itemStyle': {
                    'borderRadius': 8
                },
                'data': data_items,
                # 转换为 float 类型以确保值是可序列化的
            }
        ]
    }
    result = {
        "status": True,
        "data": data,
    }
    return JsonResponse(result)
  
def pic_1_4(text,year):
    if year == '2012-2023':
        data = models.movie_box.objects.all()
    else:
        year = int(year)
        data = models.movie_box.objects.filter(year=year)
    data_dict = {}
    for item in data:
        box = item.box
        area = item.area
        if area == '中国':
            if area not in data_dict:
                data_dict[area] = box
            else:
                data_dict[area] += box
        elif '中国' in area:
            if '中外合作' not in data_dict:
                data_dict['中外合作'] = box
            else:
                data_dict['中外合作'] += box
        else:
            area = '国外'
            if area not in data_dict:
                data_dict[area] = box
            else:
                data_dict[area] += box
    data_sorted = sorted(list(data_dict.items()),key=lambda x:-x[1])
    data_sorted = data_sorted[:10]
    areas = [item[0] for item in data_sorted]
    boxes = [item[1] for item in data_sorted]
    data_items = [{'value': value, 'name': name} for value, name in zip(boxes,areas)]
    data = {
        'title':{
            'textAlign':"auto",
            'left':'center',
            'text':text,
        },
        'legend': {
            'left': 'left',  # 设置图例在左侧
            'top': 'middle',  # 设置图例在中间
            'orient': 'vertical',  # 设置图例竖直显示
            'text':text,
        },
        'toolbox': {
            'show': True,
            'feature': {
                'mark': {'show': True},
                'dataView': {'show': True, 'readOnly': False},
                'restore': {'show': True},
                'saveAsImage': {'show': True}
            }
        },
        'tooltip': {  # 配置 tooltip
            'trigger': 'item',  # 触发类型为 item
            'formatter': '{a} <br/>{b} : {c}万元 ({d}%)',
        },
        'series': [
            {
                'name': '票房合计',
                'type': 'pie',
                'radius': ['40%', '70%'],
                'center': ['50%', '50%'],
                'itemStyle': {
                    'borderRadius': 8
                },
                'data': data_items,
                # 转换为 float 类型以确保值是可序列化的
            }
        ]
    }
    result = {
        "status": True,
        "data": data,
    }
    return JsonResponse(result)

@csrf_exempt
def chart_1(request):
    title_text = request.POST.get('title_text')
    year = request.POST.get('year')
    year = year[:-1]
    print(year)
    print(title_text)
    if title_text =='电影票房排行榜前十名':
        return pic_1_1(request.POST.get('year')+title_text,year)
    elif title_text =='演员票房排行榜前十名':
        return pic_1_2(request.POST.get('year')+title_text,year)
    elif title_text=='各类型票房占比':
        return pic_1_3(request.POST.get('year')+title_text,year)
    elif title_text == '各地区票房占比':
        return pic_1_4(request.POST.get('year')+title_text,year)
    else:
        result = {
            "status": False,
        }
        return JsonResponse(result)   

def pic_2_1(text):
    years = [year for year in range(2012,2024)]
    genres = models.movie_box.objects.all().values_list('main_genre',flat=True)
    genres = list(set(genres))
    genres = sorted(genres)
    data_dict = {genre:[] for genre in genres}
    for year in years:
        data = models.movie_box.objects.filter(year = year)
        data_temp = {}
        for item in data:
            genre = item.main_genre
            if genre not in data_temp:
                data_temp[genre] = item.box
            else :
                data_temp[genre] += item.box
        for genre in genres:
            if genre in data_temp:
                data_dict[genre].append(data_temp[genre])
            else:
                data_dict[genre].append(Decimal('0.00'))
    data = []
    for genre in genres:
        year_i = 2012
        for item in data_dict[genre]:
            data.append([str(year_i),item,genre])
            year_i +=1
    options = {
        'title':{
            'textAlign':"auto",
            'left':'left',
            'text':text,
        },
        'toolbox': {
            'show': True,
            'feature': {
                'mark': {'show': True},
                'dataView': {'show': True, 'readOnly': False},
                'restore': {'show': True},
                'saveAsImage': {'show': True}
            }
        },
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {
                "type": "line",
                "lineStyle": {
                    "color": "rgba(0,0,0,0.2)",
                    "width": 1,
                    "type": "solid"
                }
            },
            'show': True,
            'feature': {
                'mark': {'show': True},
                'dataView': {'show': True, 'readOnly': False},
                'restore': {'show': True},
                'saveAsImage': {'show': True}
            }
        },
        "legend": {
            "data": genres,
        },
        "singleAxis": {
            "top": 50,
            "bottom": 50,
            "axisTick": {},
            "axisLabel": {},
            "type": "time",
            "axisPointer": {
                "animation": True,
                "label": {
                    "show": True
                }
            },
            "splitLine": {
                "show": True,
                "lineStyle": {
                    "type": "dashed",
                    "opacity": 0.2
                }
            }
        },
        "series": [
            {
                "type": "themeRiver",
                "emphasis": {
                    "itemStyle": {
                        "shadowBlur": 20,
                        "shadowColor": "rgba(0, 0, 0, 0.8)"
                    }
                },
                "data": data,
            }
        ]
    }
    return JsonResponse({'status':True,'data':options})

def pic_2_2(text):
    years = [year for year in range(2012,2024)]
    data_dict = {
        '中国':[],
        '中外合作':[],
        '国外':[],
    }
    areas = ['中国','中外合作','国外']
    for year in years:
        data = models.movie_box.objects.filter(year = year)
        data_temp = {}
        for item in data:
            area = item.area
            if area != '中国':
                if '中国' in area:
                    area = '中外合作'
                else:
                    area = '国外'
            if area not in data_temp:
                data_temp[area] = item.box
            else :
                data_temp[area] += item.box
        for area in areas:
            if area in data_temp:
                data_dict[area].append(data_temp[area])
            else:
                data_dict[area].append(Decimal('0.00'))
    data = []
    for area in areas:
        year_i = 2012
        for item in data_dict[area]:
            data.append([str(year_i),item,area])
            year_i +=1
    options = {
        'title':{
            'textAlign':"auto",
            'left':'left',
            'text':text,
        },
        'toolbox': {
            'show': True,
            'feature': {
                'mark': {'show': True},
                'dataView': {'show': True, 'readOnly': False},
                'restore': {'show': True},
                'saveAsImage': {'show': True}
            }
        },
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {
                "type": "line",
                "lineStyle": {
                    "color": "rgba(0,0,0,0.2)",
                    "width": 1,
                    "type": "solid"
                }
            },
            'show': True,
            'feature': {
                'mark': {'show': True},
                'dataView': {'show': True, 'readOnly': False},
                'restore': {'show': True},
                'saveAsImage': {'show': True}
            }
        },
        "legend": {
            "data": areas,
        },
        "singleAxis": {
            "top": 50,
            "bottom": 50,
            "axisTick": {},
            "axisLabel": {},
            "type": "time",
            "axisPointer": {
                "animation": True,
                "label": {
                    "show": True
                }
            },
            "splitLine": {
                "show": True,
                "lineStyle": {
                    "type": "dashed",
                    "opacity": 0.2
                }
            }
        },
        "series": [
            {
                "type": "themeRiver",
                "emphasis": {
                    "itemStyle": {
                        "shadowBlur": 20,
                        "shadowColor": "rgba(0, 0, 0, 0.8)"
                    }
                },
                "data": data,
            }
        ]
    }
    return JsonResponse({'status':True,'data':options})

@csrf_exempt
def chart_2(request):
    title_text = request.POST.get('title_text')
    print(title_text)
    if title_text =='各类型票房变化河流图':
        return pic_2_1(title_text)
    elif title_text =='各地区票房变化河流图':
        return pic_2_2(title_text)
    else:
        result = {
            "status": False,
        }
        return JsonResponse(result)   

def pic_3_1(actor):
    act_obj = models.movie_box.objects.filter(actors__contains=actor).order_by('-box')
    if act_obj:
        movies = []
        for item in act_obj:
            movie_name = item.movie_name
            box = item.box
            movies.append((movie_name,box))
            print(movie_name)
        nodes = [{"name": movie[0], 'label': {'show': True, 'position': 'inside'}} for movie in movies]  # 电影作为节点
        nodes.append({'name':actor, 'label': {'show': True, 'position': 'inside'}})
        links = [{
            "source": actor, 
            "target": movie[0],
            "value": movie[1],
            }
            for movie in movies]  # 演员和电影之间的关系作为边
        # 生成 options

        # 生成 options
        options = {
            'title': {
                'textAlign': "auto",
                'left': 'left',
                'text': f"{actor}代表作及其票房",
            },
            'tooltip': {
                'trigger': 'item',
                'formatter': '{b}: {c}票房'
            },
            'series': [{
                'type': 'graph',
                'layout': 'force',
                'symbolSize': 40,
                'roam': True,
                'edgeSymbol': ['circle', 'arrow'],
                'edgeSymbolSize': [4, 10],
                'edgeLabel': {
                    'show': True,
                    'formatter': '{c}万元'
                },
                'draggable': True,
                'data': nodes,
                'links': links,
                'emphasis': {
                    'focus': 'adjacency',
                    'label': {
                        'position': 'right',
                        'show': True
                    }
                },
                'force': {
                    'repulsion': 1000,  # 增大节点之间的斥力
                    'gravity': 0.1,      # 增加中心引力
                    'edgeLength': 150    # 增加边的长度
                },
                'label': {
                    'show': True,        # 显示节点的名称
                    'position': 'inside' # 节点名称显示在节点中心
                },
            }]
        }


        return JsonResponse({'status':True,'data':options})
    else:
        result = {
            "status": False,
        }
        return JsonResponse(result) 
@csrf_exempt
def chart_3(request):
    actor = request.POST.get('actor')
    print(actor)
    return pic_3_1(actor)