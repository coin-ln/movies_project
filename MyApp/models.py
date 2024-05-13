from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
class Movies(models.Model):
    f1 = models.CharField(max_length=255, blank=True, null=True)
    movie_id = models.CharField(db_column='MOVIE_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=255, blank=True, null=True)  # Field name made lowercase.
    alias = models.CharField(db_column='ALIAS', max_length=255, blank=True, null=True)  # Field name made lowercase.
    actors = models.CharField(db_column='ACTORS', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cover = models.CharField(db_column='COVER', max_length=255, blank=True, null=True)  # Field name made lowercase.
    directors = models.CharField(db_column='DIRECTORS', max_length=255, blank=True, null=True)  # Field name made lowercase.
    douban_score = models.CharField(db_column='DOUBAN_SCORE', max_length=255, blank=True, null=True)  # Field name made lowercase.
    douban_votes = models.CharField(db_column='DOUBAN_VOTES', max_length=255, blank=True, null=True)  # Field name made lowercase.
    genres = models.CharField(db_column='GENRES', max_length=255, blank=True, null=True)  # Field name made lowercase.
    imdb_id = models.CharField(db_column='IMDB_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    languages = models.CharField(db_column='LANGUAGES', max_length=255, blank=True, null=True)  # Field name made lowercase.
    mins = models.CharField(db_column='MINS', max_length=255, blank=True, null=True)  # Field name made lowercase.
    official_site = models.CharField(db_column='OFFICIAL_SITE', max_length=255, blank=True, null=True)  # Field name made lowercase.
    regions = models.CharField(db_column='REGIONS', max_length=255, blank=True, null=True)  # Field name made lowercase.
    release_date = models.CharField(db_column='RELEASE_DATE', max_length=255, blank=True, null=True)  # Field name made lowercase.
    slug = models.CharField(db_column='SLUG', max_length=255, blank=True, null=True)  # Field name made lowercase.
    storyline = models.CharField(db_column='STORYLINE', max_length=8000, blank=True, null=True)  # Field name made lowercase.
    tags = models.CharField(db_column='TAGS', max_length=255, blank=True, null=True)  # Field name made lowercase.
    year = models.CharField(db_column='YEAR', max_length=255, blank=True, null=True)  # Field name made lowercase.
    actor_ids = models.CharField(db_column='ACTOR_IDS', max_length=255, blank=True, null=True)  # Field name made lowercase.
    director_ids = models.CharField(db_column='DIRECTOR_IDS', max_length=255, blank=True, null=True)  # Field name made lowercase.
    def __str__(self):
        return self.name

class UserInfo(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_md5 = models.CharField(db_column='user_md5', max_length=255, blank=True, null=True) 
    username = models.CharField(max_length=16, blank=True, null=True)
    password = models.CharField(max_length=64, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    e_mail = models.CharField(max_length=64, blank=True, null=True)
    gender_choices = (
        (1, "男"),
        (2, "女"),
    )
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices, default=1)
class Comments(models.Model):
    comment_id = models.CharField(db_column='comment_id', max_length=255, blank=True, null=True)  # Field name made lowercase.
    user_md5 = models.CharField(db_column='user_md5', max_length=255, blank=True, null=True)  # Field name made lowercase.
    movie_id = models.CharField(db_column='movie_id', max_length=255, blank=True, null=True)  # Field name made lowercase.
    # movie_id = models.ForeignKey(verbose_name='movie_id',to='Movies',to_field='movie_id',null=True, blank=True, on_delete=models.SET_NULL)
    content = models.CharField(db_column='content', max_length=8000, blank=True, null=True)  # Field name made lowercase.
    votes = models.IntegerField(db_column='',blank=True, null=True)
    comment_time = models.CharField(db_column='comment_time',max_length=255,blank=True,null=True)
    movie_name = models.CharField(db_column='movie_name', max_length=255, blank=True, null=True)  # Field name made lowercase.
   
class Douban_UserInfo(models.Model):
    user_md5 = models.CharField(db_column='user_md5', max_length=255, blank=True, null=True)  # Field name made lowercase.
    user_nickname = models.CharField(db_column='user_nickname', max_length=255, blank=True, null=True)  # Field name made lowercase.

class Douban_Comments(models.Model):
    comment_id = models.CharField(db_column='comment_id', max_length=255, blank=True, null=True)  # Field name made lowercase.
    user_md5 = models.CharField(db_column='user_md5', max_length=255, blank=True, null=True)  # Field name made lowercase.
    movie_id = models.CharField(db_column='movie_id', max_length=255, blank=True, null=True)  # Field name made lowercase.
    # movie_id = models.ForeignKey(verbose_name='movie_id',to='Movies',to_field='movie_id',null=True, blank=True, on_delete=models.SET_NULL)
    content = models.CharField(db_column='content', max_length=8000, blank=True, null=True)  # Field name made lowercase.
    votes = models.IntegerField(db_column='',blank=True, null=True)
    comment_time = models.CharField(db_column='comment_time',max_length=255,blank=True,null=True)
    rating = models.CharField(db_column='rating',max_length=255,blank=True,null=True)

class Douban_ratings(models.Model):
    rating_id = models.CharField(max_length=50,verbose_name='id',)
    user_md5 = models.CharField(db_column='user_md5', max_length=255, blank=True, null=True)
    movie_id = models.CharField(db_column='movie_id', max_length=255, blank=True, null=True)
    # movie_id = models.ForeignKey(verbose_name='movie_id',to='Movies',to_field='movie_id',null=True, blank=True, on_delete=models.SET_NULL)
    rating = models.CharField(db_column='rating',max_length=255,blank=True,null=True)
    rating_time = models.CharField(db_column='rating_time',max_length=255,blank=True,null=True)
    class Meta:
        db_table = 'Douban_ratings'
        verbose_name = '评分信息'
        verbose_name_plural = '评分信息'
class ratings(models.Model):
    user_md5 = models.CharField(db_column='user_md5', max_length=255, blank=True, null=True)
    movie_id = models.CharField(db_column='movie_id', max_length=255, blank=True, null=True)
    # movie_id = models.ForeignKey(verbose_name='movie_id',to='Movies',to_field='movie_id',null=True, blank=True, on_delete=models.SET_NULL)
    rating = models.CharField(db_column='rating',max_length=255,blank=True,null=True)
    rating_time = models.CharField(db_column='rating_time',max_length=255,blank=True,null=True)
    movie_name = models.CharField(db_column='movie_name', max_length=255, blank=True, null=True)  # Field name made lowercase.
    class Meta:
        db_table = 'ratings'
        verbose_name = '评分信息'
        verbose_name_plural = '评分信息'

class movie_box(models.Model):
    movie_name = models.CharField(verbose_name='电影名称',max_length=255)
    year = models.PositiveIntegerField(verbose_name='年份')
    box = models.DecimalField(verbose_name='票房',max_digits=10, decimal_places=2)
    area = models.CharField(verbose_name='国家地区',max_length=255)
    
    main_genre = models.CharField(verbose_name='主要类型',max_length=255)
    genre = models.CharField(verbose_name='类型',max_length=100)
    duration = models.PositiveIntegerField(verbose_name='片长')
    director = models.CharField(verbose_name='导演',max_length=100)
    actors = models.CharField(verbose_name='演员',max_length=255)  # 用逗号分隔的演员名字字符串
    class Meta:
        db_table = 'movie_box'
        verbose_name = '票房信息'
        verbose_name_plural = '票房信息'