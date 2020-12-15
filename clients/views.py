from django.shortcuts import render,redirect
from clients.models import creator_profile,catagory,user_profile,followers,posts,likes
from django.contrib.auth.models import User
# Create your views here.

def dashboard(request):
    return render(request,'company_dashboard.html')

def post(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            image = request.POST['post_file']
            desc = request.POST['description']
            posts(user_id=request.user,post_file=image,post=desc).save()
            return redirect('company dashboard')
        else:
            return render(request,'post_upload.html')
    else:
        return redirect('login-Page')

def my_menu(request):
    return render(request,'my_menu.html')

def add(request):

    if request.method=="POST":
        user_id = request.user
        phone=request.POST['phone']
        name=request.POST['name']
        email=request.POST['email']
        address=request.POST['address']
        age=request.POST['date']
        phone_al = new_customer.objects.filter(user_id=user_id,phone=phone)
        if len(phone_al)==0:
            cust = new_customer(user_id=user_id,name=name,email=email,phone=phone,Address=address,age=age)
            cust.save()
            return redirect('all customer')
        else:
            return redirect('all customer')
    return render(request, 'add_customer.html')

def all_customer(request):
    if request.user.is_authenticated:
        user_id = request.user
        customers = new_customer.objects.filter(user_id=user_id)
        return render(request,'all_customer.html',{'context':customers})
    else:
        return redirect('login-page')
    # return render(request, 'all_customers.html')

def delete_customer(request,key_id):
    if request.user.is_authenticated:
        user_id=request.user
        customer=new_customer.objects.filter(user_id=user_id,id=key_id)
        customer.delete()
        return redirect('all customer')
    else:
        return redirect('login-page')



def profile(request,username):
    user_id=User.objects.get(username=username)
    user_by = request.user.id
    status_statu = check_user(username,user_by)

    context = {
        'profile':User.objects.get(id=user_id.id),
        # 'follow':creator_profile.objects.get(user_id=user_id),
        'catagory':catagory.objects.all(),
        'status':status_statu,
    }
    return render(request,'Profile.html',{'context':context})

def add_follow(request,username):
    if request.user.is_authenticated:
        user_id=User.objects.get(username=username)
        # follow = creator_profile.objects.get(user_id=user_id.id)
        followers(follower_id=user_id.id,followed_id=request.user.id).save()
        return redirect('/manage/'+username)
    else:
        return redirect('login-Page')

def del_follow(request,username):
    if request.user.is_authenticated:
        user_id=User.objects.get(username=username)
        # follow = creator_profile.objects.get(user_id=user_id.id)
        delf = followers.objects.get(follower_id=user_id.id,followed_id=request.user.id)
        delf.delete()
        return redirect('/manage/'+username)
    else:
        return redirect('login-Page')

def check_user(username,user_by):
    status=False
    user_id=User.objects.get(username=username).id
    user_id_by=user_by
    try:
        followers.objects.get(follower_id=user_id,followed_id=user_id_by)
        status=True
        return status
    except:
        return status


def like_post():
    # print(user_id)
    if request.user.is_authenticated:
        likes(post_id=post_id,user_who_liked=request.user.id)
        return redirect('infinite_post')

def unlike_post():
    pass

def infinite_post(request):
    if request.user.is_authenticated:
        t = followers.objects.filter(followed_id=request.user.id)
        list_of_followed=[i.follower_id for i in t]
        post = posts.objects.filter(user_id__in=list_of_followed).order_by('updated_at','created_at')
        return render(request,'posts.html',{'context':post})
    else:
        return redirect('login-Page')