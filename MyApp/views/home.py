from django.shortcuts import render,HttpResponse
from MyApp import models
from MyApp.utils.pagination import Pagination
from MyApp.utils.encrypt import md5
from MyApp.utils.form import RatingForm,CommentForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def home_page(request):
    return render(request,'layout.html')

def movie_list(request):
    data_dict = {}
    search_data =request.GET.get('q','')
    if search_data:
        data_dict['name__contains'] = search_data
    queryset = models.Movies.objects.filter(**data_dict).order_by("?")
    page_object = Pagination(request,queryset)
    user_md5 = 0
    if 'info' in request.session:
        user_md5 = md5(str(request.session['info']['id']))
    for item in page_object.page_queryset:
        condition_current = {
            'user_md5':user_md5,
            'movie_id':item.movie_id,
        }
        rating_current = models.ratings.objects.filter(**condition_current)
        if rating_current:
            rating_current = int(rating_current.first().rating)
        else:
            rating_current = 0
        item.rating = [i for i in range(rating_current)]
    context = {
        'queryset':page_object.page_queryset,
        'page_string':page_object.html(),
    }
    return render(request,'movie_list.html',context)

def greatmovie_list(request):
    data_dict = {}
    search_data =request.GET.get('q','')
    if search_data:
        data_dict['name__contains'] = search_data
    queryset = models.Movies.objects.filter(**data_dict).order_by("-douban_score")
    page_object = Pagination(request,queryset)
    for item in page_object.page_queryset:
        condition_current = {
            'user_md5':md5(str(request.session['info']['id'])),
            'movie_id':item.movie_id,
        }
        rating_current = models.ratings.objects.filter(**condition_current)
        if rating_current:
            rating_current = int(rating_current.first().rating)
        else:
            rating_current = 0
        item.rating = [i for i in range(rating_current)]
    context = {
        'queryset':page_object.page_queryset,
        'page_string':page_object.html(),
    }
    return render(request,'movie_list.html',context)


def rating_list(request):
    user_md5 = md5(str(request.session['info']['id']))
    queryset = models.ratings.objects.filter(user_md5=user_md5)
    page_object = Pagination(request,queryset)
    context = {
        'queryset':page_object.page_queryset,
        'page_string':page_object.html(),
        'ratingform':RatingForm(),
    }
    return render(request,'rating_list.html',context)

@csrf_exempt
def rating_delete(request):
    movie_id = request.POST.get('movie_id')
    user_md5 = md5(str(request.session['info']['id']))
    models.ratings.objects.filter(movie_id=movie_id,user_md5=user_md5).delete()
    return JsonResponse({'status':True})

def comment_list(request):
    user_md5 = md5(str(request.session['info']['id']))
    queryset = models.Comments.objects.filter(user_md5=user_md5)
    page_object = Pagination(request,queryset)
    context = {
        'queryset':page_object.page_queryset,
        'page_string':page_object.html(),
        'commentform':CommentForm(),
    }
    return render(request,'comment_list.html',context)

@csrf_exempt
def comment_delete(request):
    comment_id = request.POST.get('comment_id')
    models.Comments.objects.filter(comment_id=comment_id).delete()
    return JsonResponse({'status':True})

