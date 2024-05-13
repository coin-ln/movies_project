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

def get_current_user_movies(currentUser_md5):
    rating_obj = models.ratings.objects.filter(user_md5=currentUser_md5)
    movies_list = []
    rating_list = []
    for item in rating_obj:
        movies_list.append(item.movie_id)
        rating_list.append(int(item.rating))
    print(movies_list)
    return movies_list,rating_list

def get_data(currentUser_md5):
    current_user_movies , current_user_movies_rating= get_current_user_movies(currentUser_md5)
    if len(current_user_movies) == 0:
        return None
    # 第一遍查询 查找潜在用户
    rating_obj = models.Douban_ratings.objects.filter(movie_id__in=current_user_movies).values_list('user_md5',flat=True)
    users = list(set(rating_obj))
    if not users:
        return None
    # 第二遍查询 查找潜在电影
    rating_obj = models.Douban_ratings.objects.filter(user_md5__in=users).values_list('movie_id',flat=True)
    movies = list(set(rating_obj))
    if not movies:
        return None
    
    users_data = {}     #二维,users_data['user']是一个字典，users_data['user']['movie']是用户对这部电影的评分，
                       #users_data['user']['mean']表示评分的平均值
    movie_user ={}     #movie_user['movie'] 表示对movie评分的人群
    rating_obj = models.Douban_ratings.objects.filter(user_md5__in=users)
    for item in rating_obj:
        user = item.user_md5
        movie = item.movie_id
        rating = item.rating
        if not user in users_data.keys():
            users_data[user]={}
        users_data[user][movie]=int(rating)

    current_user_data={}
    for i in range(len(current_user_movies)):
        current_user_data[current_user_movies[i]]=current_user_movies_rating[i]
    # 对user_data中清洗掉 电影集合为current_user_data的子集等到
    cleaned_users_data = {}
    for user,user_data in users_data.items():
        is_subset = set(user_data.keys()).issubset(set(current_user_data.keys()))
        if is_subset:
            continue
        cleaned_users_data[user]=user_data

    for user,user_data in cleaned_users_data.items():
        for movie in user_data.keys():
            if movie not in movie_user.keys():
                movie_user[movie]=[]
            movie_user[movie].append(user)
    # for user,user_data in cleaned_users_data.items():

    return cleaned_users_data,movie_user,current_user_data,movies,users

def get_PearsonSimilarity(rating_a,rating_b,mean_a,mean_b):
    dataA = np.array(rating_a)
    dataB = np.array(rating_b)
    sumData = np.dot((dataA - mean_a),(dataB - mean_b)) # 若列为向量则为 dataA.T * dataB)
    denom = np.linalg.norm(dataA - mean_a) * np.linalg.norm(dataB - mean_b)
    if denom == 0.0:
        return 0.0
    return sumData / denom

def get_neighbor(currentUser_md5,neighbors_num):
    users_data,movie_user,current_user_data,movies,users=get_data(currentUser_md5)
    neighbors = []
    for user,user_data in users_data.items():
        rating_a = []
        rating_b = []
        for movie in current_user_data.keys():
            if movie in user_data.keys():
                rating_a.append(current_user_data[movie])
                rating_b.append(user_data[movie])
        if len(rating_a) <= 1:
            continue
        similarity = get_PearsonSimilarity(rating_a,rating_b,np.mean(list(current_user_data.values())),np.mean(list(user_data.values())))
        similarity = float(similarity)
        neighbors.append([user,similarity,fabs(similarity)])
    neighbors.sort(key=lambda tup:-tup[2])
    neighbors=neighbors[:neighbors_num]
    user_similarity = {}
    for neighbor in neighbors:
        user_similarity[neighbor[0]]=neighbor[1]
    return neighbors,users_data,movie_user,current_user_data,user_similarity

def get_movie_list(neighbors,users_data,movie_user,current_user_data,user_similarity):
    current_user_mean = np.mean(list(current_user_data.values()))
    movie_rating = {}
    movie_list = []
    for item in neighbors:
        user = item[0]
        similarity = item[1]
        f_similarity = item[2]
        for movie,rating in users_data[user].items():
            if movie in current_user_data.keys():
                continue
            a = similarity * (rating - np.mean(list(users_data[user].values())))
            b = f_similarity
            if movie in movie_rating:
                movie_rating[movie][0] += a
                movie_rating[movie][1] += b
            else:
                movie_rating[movie] =[a,b]
    for movie,rating in movie_rating.items():
        if rating[1] == 0.0:
            continue
        movie_list.append([movie,current_user_mean+rating[0]/rating[1]])
    movie_list.sort(key=lambda tup:-tup[1])
    movie_list = [item[0] for item in movie_list]
    return movie_list

def recommend_list(request):
    currentUser_md5 = md5(str(request.session['info']['id']))
    neighbors,users_data,movie_user,current_user_data,user_similarity = get_neighbor(currentUser_md5,100)
    movies_num = 10
    # movie_list = ['2059225','1781924','1298468','1308858','1300678','1400935','1473562','1304100','1304811','1297102']
    movie_list = get_movie_list(neighbors,users_data,movie_user,current_user_data,user_similarity)
    # print(movie_list)
    order_conditions = [When(movie_id=pk, then=pos) for pos, pk in enumerate(movie_list)]
    queryset = models.Movies.objects.filter(movie_id__in=movie_list).order_by(Case(*order_conditions))
    queryset = queryset[:movies_num]
    if queryset:
        context = {
            'queryset':queryset,
        }
        return render(request,'recommend_list.html',context)
    user_md5 = md5(str(request.session['info']['id']))
    rating_obj = models.ratings.objects.filter(user_md5=user_md5).values_list('movie_id',flat=True)
    movie_list=list(rating_obj)
    movie_object = models.Movies.objects.exclude(movie_id__in=movie_list).order_by('?')[:10]
    context ={
        'queryset':movie_object,
        'error':'暂无推荐，请多对几部电影评分'
    }
    return render(request,'recommend_home.html',context)

def recommend_home(request):
    user_md5 = md5(str(request.session['info']['id']))
    rating_obj = models.ratings.objects.filter(user_md5=user_md5).values_list('movie_id',flat=True)
    movie_list=list(rating_obj)
    movie_object = models.Movies.objects.exclude(movie_id__in=movie_list).order_by('?')[:10]
    context ={
        'queryset':movie_object,
    }
    return render(request,'recommend_home.html',context)

@csrf_exempt
def recommend_check(request):
    user_md5 = md5(str(request.session['info']['id']))
    rating_obj = models.ratings.objects.filter(user_md5=user_md5)
    if rating_obj:
        return JsonResponse({'status':True})
    return JsonResponse({'status':False})
