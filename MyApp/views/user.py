from django.shortcuts import render,HttpResponse,redirect
from MyApp import models
from MyApp.utils.form import RegisterForm,LoginForm
from MyApp.utils.code import check_code
from MyApp.utils.encrypt import md5

def register(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request,'register.html',{'form':form})
    form = RegisterForm(data=request.POST)
    if form.is_valid():
        user_input_code = form.cleaned_data.pop('code')
        code = request.session.get('image_code', "")
        if code.upper() != user_input_code.upper():
            form.add_error("code", "验证码错误")
            return render(request, 'register.html', {'form': form})
        user_obj = form.cleaned_data
        user_obj.pop('confirm_pwd')
        models.UserInfo.objects.create(**user_obj)
        return redirect("/home/")
    return render(request,'register.html',{'form':form})

def login(request):
    """ 登录 """
    if request.method == "GET":
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    form = LoginForm(data=request.POST)
    if form.is_valid():
        user_input_code = form.cleaned_data.pop('code')
        code = request.session.get('image_code', "")
        if code.upper() != user_input_code.upper():
            form.add_error("code", "验证码错误")
            return render(request, 'login.html', {'form': form})

        user_object = models.UserInfo.objects.filter(**form.cleaned_data).first()
        if not user_object:
            form.add_error("password", "用户名或密码错误")
            # form.add_error("username", "用户名或密码错误")
            return render(request, 'login.html', {'form': form})

        if not user_object.user_md5:
            user_object.user_md5 = md5(str(user_object.id))
            user_object.save()
        # 用户名和密码正确
        # 网站生成随机字符串; 写到用户浏览器的cookie中；在写入到session中；
        request.session["info"] = {'id': user_object.id, 'name': user_object.username}
        # session可以保存7天
        request.session.set_expiry(60 * 60 * 24 * 7)

        return redirect("/home/")

def logout(requset):
    requset.session.clear()
    return redirect("/home/")

from io import BytesIO

def image_code(request):
    img,code_string = check_code()

    request.session['image_code'] = code_string
    request.session.set_expiry(60)

    stream  = BytesIO()
    img.save(stream,'png')
    return HttpResponse(stream.getvalue())
        