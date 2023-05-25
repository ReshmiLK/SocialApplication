from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count

# Create your models here.

class UserProfileModel(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    profile_pic=models.ImageField(upload_to="profiles",null=True,blank=True)
    bio=models.CharField(max_length=200)
    time_line_pic=models.ImageField(upload_to="timelineimages",null=True,blank=True)

    def __str__(self):
        return self.user.username
    

class PostModel(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    caption=models.CharField(max_length=260)
    image=models.ImageField(upload_to="images",null=True,blank=True)
    created_date=models.DateTimeField(auto_now_add=True)
    like=models.ManyToManyField(User,related_name="likes")

    @property
    def post_comment(self):
        return CommentModel.objects.filter(post=self).annotate(ccount=Count("clike")).order_by('-ccount')
    
    @property
    def like_count(self):
        return self.like.all().count()
    

class CommentModel(models.Model):
    post=models.ForeignKey(PostModel, on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    comment=models.CharField(max_length=200)
    created_date=models.DateTimeField(auto_now_add=True)
    clike=models.ManyToManyField(User,related_name="commentlikes")

    @property
    def clike_count(self):
        return self.clike.all().count()


