from django.shortcuts import render,redirect
from clients.models import creator_profile,catagory,user_profile,followers,posts,likes
from django.contrib.auth.models import User
# Create your views here.

def dashboard(request):
    return render(request,'company_dashboard.html')

def post(request):
    if request.user.is_authenticated:
        if request.method=="POST" and request.FILES: 
            image = request.FILES['post_file']
            desc = request.POST['description']
            posts(user_id=request.user,post_file=image,post=desc,username=request.user.username).save()
            return redirect('/manage/'+request.user.username)
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
    posts1 = posts.objects.filter(user_id=user_id.id)
    # print(user_id.id)
    if len(posts1)==0:
        catch=False
    else:
        catch=True

    if request.user.id!=user_id.id:
        itsme = False
    else:
        itsme=True
        
    context = {
        'profile':User.objects.get(id=user_id.id),
        'posts':posts1,
        # 'catagory':catagory.objects.all(),
        'status':status_statu,
        'itsme':itsme,
        'posts_exists':catch,
    }
    return render(request,'Profile.html',{'context':context})

def add_follow(request,username):
    if request.user.is_authenticated:
        user_id=User.objects.get(username=username)
        # follow = creator_profile.objects.get(user_id=user_id.id)
        followers(followed_to_id=user_id.id,followed_by_id=request.user.id).save()
        return redirect('/manage/'+username)
    else:
        return redirect('login-Page')

def del_follow(request,username):
    if request.user.is_authenticated:
        user_id=User.objects.get(username=username)
        # follow = creator_profile.objects.get(user_id=user_id.id)
        delf = followers.objects.get(followed_to_id=user_id.id,followed_by_id=request.user.id)
        delf.delete()
        return redirect('/manage/'+username)
    else:
        return redirect('login-Page')

def check_user(username,user_by):
    status=False
    user_id=User.objects.get(username=username).id
    user_id_by=user_by
    try:
        followers.objects.get(followed_to_id=user_id,followed_by_id=user_id_by)
        status=True
        return status
    except:
        return status


def like_post(request,posts_id):
    if request.user.is_authenticated:
        likes(post_id_id=posts_id,user_who_liked=request.user.id).save()
        check_like(posts_id,"add")
        return redirect('infinite_post')

def unlike_post(request,posts_id):
    if request.user.is_authenticated:
        obj = likes.objects.get(post_id_id=posts_id,user_who_liked=request.user.id).delete()
        check_like(posts_id,"sub")
        return redirect('infinite_post')

def infinite_post(request):
    if request.user.is_authenticated:
        t = followers.objects.filter(followed_by_id=request.user.id)
        list_of_followed=[i.followed_to_id for i in t]
        post = posts.objects.filter(user_id__in=list_of_followed).order_by('-updated_at','created_at')
        liked = [i.post_id.id for i in likes.objects.filter(user_who_liked=request.user.id)]
        me = User.objects.get(id=request.user.id)
        context = {
            'myself':me,
            'post':post,
            'liked':liked,
            # 'username':username,
        }

        return render(request,'posts.html',{'context':context})
    else:
        return redirect('login-Page')

def check_liked_or_not(posts_id,user_id_1,user_id):
    status=False
    try:
        likes.objects.get(post_id_id=posts_id,user_who_liked=user_id_1,whose_liked=user_id)
        status = True
        return status
    except:
        return status


def check_like(post_id,val):
    like = posts.objects.get(id=post_id)
    if val=="add":
        like.like_count+=1
        like.save()
    if val=="sub":
        like.like_count-=1
        like.save()
    

def followers_page(request,username):
    page = "following"
    if request.user.is_authenticated:
        usernames_id = User.objects.get(username=username)
        follower = followers.objects.filter(followed_to_id=usernames_id.id)

        follower_username = []
        for i in follower:
            follower_username.append(User.objects.get(id=i.followed_by_id).username)

        status = check_if_thats_me(username,request.user)
        print(status)
        context={

            'follower':follower_username,
            'myself':username,
            'status':status,
            'page':page,
        }
    return render(request,'followers.html',{'context':context})

def remove_follower(request,username1,username):
    if request.user.is_authenticated:
        # user = request.user
        user_to_remove=User.objects.get(username=username).id
        user = User.objects.get(username=username1).id
        print(user,user_to_remove)
        followers.objects.get(followed_to_id=user,followed_by_id=user_to_remove).delete()
        return redirect('/manage/'+username1)




def check_if_thats_me(username,usern1):
    if str(username)==str(usern1):
        return True
    else:
        return False

def following_page(request,username):
    page = "following"
    if request.user.is_authenticated:
        usernames_id = User.objects.get(username=username)
        follower = followers.objects.filter(followed_by_id=usernames_id.id)

        follower_username = []
        for i in follower:
            follower_username.append(User.objects.get(id=i.followed_to_id).username)

        status = check_if_thats_me(username,request.user)
        print(status)
        context={

            'follower':follower_username,
            'myself':username,
            'status':status,
            'page':page,
        }

    return render(request,'followers.html',{'context':context})