"""
URL configuration for movies_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from MyApp.views import home,user,subject,recommend,box_view,box_predict

urlpatterns = [
    # home界面
    path("home/",home.home_page),
    path("movie/list/",home.movie_list),
    path("greatmovie/list/",home.greatmovie_list),
    path("rating/list/",home.rating_list),
    path("rating/delete/",home.rating_delete),
    path("comment/list/",home.comment_list),
    path("comment/delete/",home.comment_delete),

    # 登录注册
    path("login/",user.login),
    path("logout/",user.logout),
    path("register/",user.register),
    path("image/code/",user.image_code),

    # 电影具体页面
    path("movie/subject/<int:nid>",subject.movie_subject),
    path("comment/add/",subject.comment_add),
    path("comment/edit/",subject.comment_edit),
    path("rating/add/",subject.rating_add),
    path("rating/detail/",subject.rating_detail),
    path("rating/edit/",subject.rating_edit),
    path("vote/add/",subject.vote_add),
    path("wordcloud/get/",subject.wordcloud_get),

    # 推荐界面
    path("recommend/home",recommend.recommend_home),
    path("recommend/list/",recommend.recommend_list),
    path("recommend/check/",recommend.recommend_check),

    # 票房数据分析
    path("box/view/home/",box_view.box_view_home),
    path("box/chart1/",box_view.chart_1),
    path("box/chart2/",box_view.chart_2),
    path("box/chart3/",box_view.chart_3),

    # 票房预测
    path('box/predict/',box_predict.box_predict),
    path('box/getinfo/',box_predict.box_getinfo),

]
