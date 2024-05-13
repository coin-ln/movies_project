from django.shortcuts import render,HttpResponse
from MyApp import models
from MyApp.utils.pagination import Pagination
from MyApp.utils.encrypt import md5
from django.views.decorators.csrf import csrf_exempt
from django import forms
from django.http import JsonResponse
from MyApp.utils.bootstrap import BootStrapModelForm,BootStrapForm
import datetime
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import jieba

from MyApp.utils.form import CommentForm,RatingForm


def get_username(user_md5):
    instance = models.Douban_UserInfo.objects.filter(user_md5=user_md5).first()
    if instance:
        return str(instance.user_nickname)
    return "匿名用户"

def movie_subject(request,nid):
    if request.method == 'GET':
        instance = models.Movies.objects.filter(movie_id = nid).first()
        queryset = models.Douban_Comments.objects.filter(movie_id = nid).order_by("-votes")
        # queryset = models.Douban_Comments.objects.filter(movie_id = nid)[:1]
        page_object = Pagination(request,queryset)
        for item in page_object.page_queryset:
            item.user_nickname = get_username(item.user_md5)
        queryset_inner = models.Comments.objects.filter(movie_id = nid).order_by("-comment_time")
        for item in queryset_inner:
            item.user_nickname = models.UserInfo.objects.filter(user_md5=item.user_md5).first().username
        
        rating_self = models.ratings.objects.filter(movie_id=nid,user_md5=md5(str(request.session['info']['id'])))
        if rating_self:
            rating_self = rating_self.first().rating
            rating_self = int(rating_self)
        else:
            rating_self = 0
        context = {
            'instance':instance,
            'queryset':page_object.page_queryset,
            'page_string':page_object.html(),
            'queryset_inner':queryset_inner,
            'commentform':CommentForm(),
            'ratingform':RatingForm(), 
            'rating_self':rating_self,
            'stars':range(rating_self),
        }
        return render(request,'movie_subject.html',context)
    

@csrf_exempt
def comment_add(request):
    form = CommentForm(data=request.POST)
    print(form)
    if form.is_valid():
        local_time = datetime.datetime.now()
        comment_obj = form.cleaned_data
        comment_obj['user_md5'] = md5(str(request.session['info']['id']))
        comment_obj['comment_time'] = local_time.strftime("%Y-%m-%d %H:%M:%S")
        comment_obj['votes'] = 0
        comment_obj['movie_name'] = models.Movies.objects.filter(movie_id=comment_obj['movie_id']).first().name
        comment_obj['comment_id'] = 'l'+str(request.session['info']['id']) + str(local_time.month)+str(local_time.day)+str(local_time.hour)+str(local_time.minute)+str(local_time.second)
        print(comment_obj)
        models.Comments.objects.create(**comment_obj)
        return JsonResponse({'status':True})
    print("NO")
    return HttpResponse("失败了")

@csrf_exempt
def comment_edit(request):
    comment_id = request.POST.get('comment_id')
    comment = request.POST.get('comment')
    comment_obj = models.Comments.objects.filter(comment_id=comment_id).first()
    comment_obj.content = comment
    comment_obj.save()
    return JsonResponse({'status':True})

@csrf_exempt
def rating_add(request):
    form = RatingForm(data=request.POST)
    if form.is_valid():
        rating_obj = form.cleaned_data
        rating_obj['user_md5'] = md5(str(request.session['info']['id']))
        rating_obj['rating_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        rating_obj['movie_name'] = models.Movies.objects.filter(movie_id=rating_obj['movie_id']).first().name
        models.ratings.objects.create(**rating_obj)
        return JsonResponse({'status':True})
    print("NO")
    return HttpResponse("失败了")

@csrf_exempt
def rating_detail(request):
    movie_id = request.POST.get('movie_id')
    user_md5 = md5(str(request.session['info']['id']))
    rating = models.ratings.objects.filter(user_md5=user_md5,movie_id=movie_id).first().rating
    return JsonResponse({'status':True,'data':rating})

@csrf_exempt
def rating_edit(request):
    movie_id = request.POST.get('movie_id')
    rating = request.POST.get('rating')
    user_md5 = md5(str(request.session['info']['id']))
    rating_obj = models.ratings.objects.filter(user_md5=user_md5,movie_id=movie_id).first()
    rating_obj.rating = rating
    rating_obj.save()
    return JsonResponse({'status':True})

@csrf_exempt
def vote_add(request):
    print(request.POST)
    comment_id = request.POST.get('comment_id')
    comment_obj = models.Comments.objects.filter(comment_id=comment_id)
    if comment_obj:
        comment_obj = comment_obj.first()
        comment_obj.votes += 1
        comment_obj.save()
    else:
        comment_obj = models.Douban_Comments.objects.filter(comment_id=comment_id)
        if comment_obj:
            comment_obj = comment_obj.first()
            comment_obj.votes += 1
            comment_obj.save()
        else:    
            return JsonResponse({'status':False,'error':'评论不存在'})
    return JsonResponse({'status':True})


def get_wordcloud(movie_id):
    comment_obj = models.Douban_Comments.objects.filter(movie_id=movie_id).order_by('-votes')
    comment_obj =comment_obj[:100]
    comment_list = list(comment_obj.values_list('content',flat=True))
    comment = ' '.join(comment_list)
    # 创建词云对象
    font_path = r'E:\graduate\movies_project\MyApp\static\fonts\simsun.ttc'
    wordcloud = WordCloud(width=800, height=400, background_color='white',font_path=font_path).generate(comment)
    output_path = 'E:\graduate\movies_project\MyApp\static\img\%s.png'%movie_id
    wordcloud.to_file(output_path)
    src = '/static/img/%s.png'%movie_id
    return src

@csrf_exempt
def wordcloud_get(request):
    movie_id = request.POST.get('movie_id')
    src = get_wordcloud(movie_id)
    img = "<img src='%s' alt='图片未加载成功'>"%src
    return JsonResponse({'status':True,'img':img})