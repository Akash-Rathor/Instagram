from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db import models

class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# class new_customer(TimeStampMixin):
#     user_id = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
#     name=models.CharField(max_length=100)
#     age=models.DateField()
#     Address = models.CharField(max_length=500)
#     phone = models.CharField(max_length=12)
#     email=models.EmailField(max_length=40)

#     def age_now(self):
#         import datetime
#         return int((datetime.date.today() - self.age).days / 365.25)

class creator_profile(TimeStampMixin):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    followers = models.IntegerField()
    following = models.IntegerField()
    image = models.ImageField()

class catagory(models.Model):
    cat_id = models.IntegerField()
    cat_name = models.CharField(max_length=100)

class user_profile(TimeStampMixin):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    following = models.IntegerField()
    image = models.ImageField()
    # selected_cataory = models.CharField(max_length=50,choices=catagory.cat_name)


class followers(TimeStampMixin):
    follower_id=models.IntegerField()
    followed_id=models.IntegerField()

class posts(TimeStampMixin):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    post_file=models.ImageField(upload_to='posts/%Y/%m/%d')
    post = models.CharField(max_length=500,null=True)
    username = models.CharField(max_length=500)
    like_count = models.IntegerField(default=0)

class likes(TimeStampMixin):
    post_id=models.ForeignKey(posts, on_delete=models.CASCADE,null=True)
    user_who_liked = models.IntegerField()
    # whose_liked = models.IntegerField()
