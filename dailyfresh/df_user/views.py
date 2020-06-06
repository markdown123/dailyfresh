#coding=utf-8
from django.shortcuts import render,redirect
from .models import UserInfo
from hashlib import sha1
from django.http import JsonResponse, HttpResponseRedirect

# 注册视图
def register(request):
    return render(request,'df_user/register.html')

def register_handle(request):
    # 接受用户输入
    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('pwd')
    upwd2 = post.get('cpwd')
    uemail = post.get('email')
    #再次验证密码
    if upwd!=upwd2:
        return redirect('/user/register/')
    #密码加密
    s1 = sha1()
    s1.update(upwd.encode('utf8'))
    upwd3=s1.hexdigest()

    #创建对象,将提交的数据存入数据库
    user = UserInfo()
    user.uname = uname
    user.upwd = upwd3
    user.uemail = uemail
    user.save()

    #注册成功，转到登录界面
    return redirect('/user/login/')

def register_exist(request):
    uname = request.GET.get('uname')
    count= UserInfo.objects.filter(uname=uname).count()
    print(count)
    return JsonResponse({'count':count})

def login(request):
    uname = request.COOKIES.get('uname','')
    context = {'title':'用户登录','error_name':0,'error_pwd':0,'uname':uname}
    return render(request,'df_user/login.html',context)

def login_handle(request):
    # 接受请求信息
    post = request.POST
    uname = post.get('username')
    upwd = post.get('pwd')
    jizhu= post.get('jizhu',0)
    # 根据用户名查询对象,user为[[],[]]
    users = UserInfo.objects.filter(uname=uname)
    print(uname)
    # 判断: 未查到用户名，返回错误；查到用户名，则判断密码是否正确，正确立即转到用户中心
    if len(users)==1:
        s1 = sha1()
        s1.update(upwd.encode('utf8'))
        if s1.hexdigest()==users[0].upwd:
            red = HttpResponseRedirect('/user/info/')
            # 记住用户名
            if jizhu!=0:
                red.set_cookie('uname',uname)
            else:
                red.set_cookie('uname','',max_age=1)
            request.session['user_id'] = users[0].id
            request.session['user_name']=uname
            return red
        else:
            context = {'title': '用户登录', 'error_name': 0, 'error_pwd': 1,
                       'uname': uname, 'upwd': upwd}
            return render(request, 'df_user/login.html', context)
    else:
        context = {'title': '用户登录', 'error_name': 1, 'error_pwd': 0,
                   'uname': uname,'upwd':upwd}
        return render(request,'df_user/login.html',context)

def info(request):
    user_email = UserInfo.objects.get(id=request.session['user_id']).uemail
    context= {'title':'用户中心',
              'user_email':user_email,
              'user_name':request.session['user_name']}
    return render(request,'df_user/user_center_info.html',context)

def order(request):
    context = {'title':'用户中心'}
    return render(request,'df_user/user_center_order.html',context)

def site(request):
    user = UserInfo.objects.get(id=request.session['user_id'])
    if request.method=='POST':
        post=request.POST
        user.ushou=post.get('ushou')
        user.uaddress = post.get('uaddress')
        user.uyoubian = post.get('uyoubian')
        user.phone = post.get('uphone')
        user.save()
    context={'title':'用户中心','user':user}
    return render(request,'df_user/user_center_site.html',context)


