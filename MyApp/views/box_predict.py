from django.shortcuts import render,HttpResponse
from MyApp import models
from MyApp.utils.pagination import Pagination
from MyApp.utils.encrypt import md5
from django.views.decorators.csrf import csrf_exempt
from django import forms
from django.http import JsonResponse
from MyApp.utils.bootstrap import BootStrapModelForm,BootStrapForm
from math import sqrt,fabs
import numpy as np
from django.db.models import Case, When
from MyApp.utils.form import Movie_BoxModelForm
import pandas as pd
import pickle
import sklearn
import joblib

def box_predict(request):
    form = Movie_BoxModelForm()
    context={
        'form':form,
    }
    return render(request,'box_predict.html',context)

def get_predict(data,mods_name):
    data = pd.DataFrame(data)
    genres_list = ['主旋律', '亲情', '传记', '公路', '冒险', '剧情', '动作', '动画', '励志', '历史', '友情', '古装', '喜剧', '奇幻', '家庭', '怀旧', '恐怖', '悬疑', '惊悚', '战争', '抢险', '探案', '文艺', '歌舞', '灾难', '爱情', '犯罪', '玄幻', '真人秀', '神话', '科幻', '穿越', '竞技', '综艺大电影', '职场', '警匪', '运动', '青春']
    areas_list = ['中国', '加拿大', '印度', '德国', '新西兰', '日本', '法国', '美国', '英国']
    top_actors = ['刘昊然', '吴京', '张涵予', '张译', '朱亚文', '杜江', '欧豪', '沈腾', '王宝强', '黄渤']
    top_directors = ['乔·罗素', '宁浩', '安东尼·罗素', '张艺谋', '徐克', '徐峥', '林超贤', '郭帆', '陈凯歌', '陈思诚']
    for genre in genres_list:
        data['类型_'+genre] = data['作品类型'].apply(lambda x:1 if genre in x else 0)
    for area in areas_list:
        data['国家地区_'+area] = data['国家地区'].apply(lambda x:1 if area in x else 0)
    for actor in top_actors:
        data['演员_'+actor] = data['演员'].apply(lambda x:1 if actor in x else 0)
    for director in top_directors:
        data['导演_'+director] = data['导演'].apply(lambda x:1 if director in x else 0)
    drop_columns = ['电影名称','年份','国家地区','主类型','作品类型','导演','演员']
    data = data.drop(columns=drop_columns)
    for item in data.columns:
        data [item] = data[item].astype(float)
    mods = []
    mods_mse = []
    mods_pos = []
    mods_pos_mse = []
    for mod_name in mods_name:
        mods_pos.append(r'E:\graduate\movies_project\Models\box_predict\%s_model.pkl'%mod_name)
        mods_pos_mse.append(r'E:\graduate\movies_project\Models\box_predict\%s_model_mse.pkl'%mod_name)
    for mod_pos in mods_pos:
        with open(mod_pos,'rb') as f:
            mods.append(pickle.load(f))
    for mod_pos_mse in mods_pos_mse:
        mods_mse.append(joblib.load(mod_pos_mse))
    predict_results = [mod.predict(data) for mod in mods]
    results = [np.expm1(item[0]) for item in predict_results]
    return results,mods_mse

@csrf_exempt
def box_getinfo(request):
    form = Movie_BoxModelForm(data = request.POST)
    if form.is_valid():
        all_values = form.cleaned_data.values()
        all_values = list(all_values)
        data_in ={
            '电影名称':[all_values[0]],
            '年份':[all_values[1]],
            '国家地区':[all_values[2]],
            '主类型':[all_values[3]],
            '作品类型':[all_values[4]],
            '片长':[all_values[5]],
            '导演':[all_values[6]],
            '演员':[all_values[7]],
        }
        mods_name = ['ridge','lasso','DecisionTree','RandomForest','GradientBoosting']
        result ,mods_mse = get_predict(data_in,mods_name)
        return JsonResponse({'status':True,'mods_name':mods_name,'result':result,'mse':mods_mse})
    return JsonResponse({"status": False, 'error': form.errors})