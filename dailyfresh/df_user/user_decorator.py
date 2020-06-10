#coding=utf-8
from django.shortcuts import redirect
from django.http import HttpResponseRedirect

# 如果未登录则转到登录页面,注意参数传递
def login(func):
    def login_fun(request,*args,**kwargs):
        if 'user_id' in request.session:
            return func(request,*args,**kwargs)
        else:
            red = HttpResponseRedirect('/user/login/')
            # 记录原来的页面
            red.set_cookie('url',request.get_full_path())
            return red
    return login_fun