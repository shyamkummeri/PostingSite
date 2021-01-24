from django.db import models

class UserRegister(models.Model):
    userId = models.AutoField(primary_key=True)
    userName = models.CharField(max_length=60)
    emailId = models.EmailField(unique=True)
    contactNumber = models.CharField(max_length=10,unique=True)
    password = models.CharField(max_length=50)

class PostContent(models.Model):
    postid = models.AutoField(primary_key=True)
    Useremail = models.EmailField()
    nameOfUser = models.CharField(max_length=50,default=True)
    content = models.TextField(max_length=1000)
    dateofpost = models.DateTimeField(auto_now_add=True)
    username = models.ForeignKey(UserRegister,on_delete=models.CASCADE)

class Comment(models.Model):
    commentid = models.AutoField(primary_key=True)
    userid = models.ForeignKey(UserRegister,on_delete=models.CASCADE)
    postid = models.ForeignKey(PostContent,on_delete=models.CASCADE)
    commentContent = models.TextField(max_length=1000)
    comment = models.TextField(max_length=1000)
    dateofcomment = models.DateTimeField(auto_now_add=True)

class UserLikes(models.Model):
    likesid = models.AutoField(primary_key=True)
    useridlikes = models.ManyToManyField(UserRegister,blank=True)
    postidlikes = models.ForeignKey(PostContent,on_delete=models.CASCADE)
    userid = models.IntegerField(default=True)
    like = models.BooleanField()









