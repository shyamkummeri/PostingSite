from django.contrib import messages
from django.shortcuts import render,redirect
from app.forms import UserRegisterForm
from app.models import UserRegister,PostContent,Comment,UserLikes
from datetime import datetime

def mainPage(request):
    user = request.session.get('user',None)
    if user:
        ur = UserRegister.objects.get(userName=user)
        d = datetime.now()
        post_display = PostContent.objects.all()
        post_list = [x for x in post_display]
        return render(request, 'mainPageLogin.html',{'username':user,'userid':ur.userId,'userEmail':ur.emailId,'dateofpost':d,'post_list':post_list})
    else:
        post_display = PostContent.objects.all()
        post_list = [x for x in post_display]
        return render(request,'mainPage.html',{'post_list':post_list})


def registerForm(request):
    return render(request,'registerForm.html',{'RegForm':UserRegisterForm})


def registerCheck(request):
    uf = UserRegisterForm(request.POST)
    if uf.is_valid():
        uf.save()
        messages.success(request,'Successfully Registered')
        return redirect('registerForm')
    else:
        messages.error(request,uf.errors)
        return render(request,'registerForm.html',{'RegForm':uf})


def loginForm(request):
    return render(request,'loginForm.html')


def loginCheck(request):
    email = request.POST.get('t1')
    pwd = request.POST.get('t2')
    try:
        ur = UserRegister.objects.get(emailId=email, password=pwd)
        request.session['user']=ur.userName
        d = datetime.now()
        post_display = PostContent.objects.all()
        post_list = [x for x in post_display]
        return render(request,'mainPageLogin.html',{'username':ur.userName,'userid':ur.userId,'userEmail':ur.emailId,'dateofpost':d,'post_list':post_list})
    except UserRegister.DoesNotExist:
        messages.error(request,"User details Not matched")
        return redirect('loginForm')

def postmainlogin(request):
    msg = request.POST.get("message")
    email = request.POST.get("email")
    name = request.POST.get("u_name")
    idUser = request.POST.get("u_id")
    date = request.POST.get("date")
    user = request.session.get('user',None)
    if user:
        PostContent(content=msg, Useremail=email,username_id=idUser,nameOfUser=name,dateofpost=date).save()
        d = datetime.now()
        post_display = PostContent.objects.all()
        post_list = [x for x in post_display]
        likdata = UserLikes.objects.all()
        return render(request, 'mainPageLogin.html', {'username': user,'userid':idUser,'userEmail': email,'dateofpost': d,'post_list':post_list,'likdata':likdata})
    else:
        post_display = PostContent.objects.all()
        post_list = [x for x in post_display]
        return render(request, 'mainPage.html',{'post_list':post_list})


def logOut(request):
    del_user = request.session.pop('user',None)
    if del_user:
        return redirect('main')
    else:
        return redirect('main')


def postCommentId(request,pk):
    if pk:
        glob_p_no = pk
    else:
        glob_p_no = request.GET.get("pno")
    user = request.session.get('user',None)
    if user:
        ur = UserRegister.objects.get(userName=user)
        d = datetime.now()
        comments=Comment.objects.filter(postid_id=glob_p_no).values("comment",'dateofcomment','userid','commentid')
        for uid in comments:
            global udata
            udata = uid['userid']
        comentBy = UserRegister.objects.filter(userId=udata).values('userName')
        post_content = PostContent.objects.filter(postid=glob_p_no).values('content')
        return render(request,'Commentpage.html',{"post_content":post_content,'username':ur.userName,'userid':ur.userId,'postid':glob_p_no,"comments":comments,"comentBy":comentBy})
    else:
        post_display = PostContent.objects.all()
        post_list = [x for x in post_display]
        return render(request,'mainPage.html',{'post_list':post_list})


def commentSubmit(request):
    user_comment = request.POST.get("comment")
    post_id = request.POST.get("pno")
    user = request.session.get('user', None)
    if user:
        ur = UserRegister.objects.get(userName=user)
        pc = PostContent.objects.get(postid=post_id)
        c = datetime.now()
        Comment(userid_id=ur.userId,postid_id=post_id,commentContent=pc.content,comment=user_comment,dateofcomment=c).save()
        return postCommentId(request,post_id)
    else:
        return redirect('loginForm')

def likeclickcount(request,postid):
    user = request.session.get('user',None)
    if user:
        ur = UserRegister.objects.get(userName=user)
        d = datetime.now()
        post_display = PostContent.objects.all()
        post_list = [x for x in post_display]
        likesid = UserLikes.objects.values('postidlikes_id')
        # print(postid)
        l=[]
        for i in likesid:
            if i['postidlikes_id'] not in l:
                l.append(i['postidlikes_id'])
        count = UserLikes.objects.filter(postidlikes_id=postid,like=True).count()
        return render(request, 'mainPageLogin.html',{'username':user,'userid':ur.userId,'userEmail':ur.emailId,'dateofpost':d,'post_list':post_list,'likecount':count,'likesid':l})
    else:
        post_display = PostContent.objects.all()
        post_list = [x for x in post_display]
        return render(request,'mainPage.html',{'post_list':post_list})

def likeclick(request):
    plid = request.GET.get("postlikeid")
    ulid = request.GET.get("userlikeid")
    user = request.session.get('user', None)
    if user:
        ur = UserRegister.objects.get(userName=user)
        alreadylike = UserLikes.objects.filter(userid=ur.userId,postidlikes_id=plid,like=True)
        alreadynotlike = UserLikes.objects.filter(userid=ur.userId,postidlikes_id=plid,like=False)
        if alreadylike:
            UserLikes.objects.filter(userid=ur.userId,postidlikes_id=plid).update(like=False)
        elif alreadynotlike:
            UserLikes.objects.filter(userid=ur.userId, postidlikes_id=plid).update(like=True)
        else:
            lk = UserLikes(postidlikes_id=plid, like=True, userid=ur.userId)
            lk.save()
            lk.useridlikes.set(ulid)
        return likeclickcount(request,plid)
    else:
        return redirect('loginForm')

