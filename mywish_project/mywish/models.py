from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.urls import reverse
from django.conf import settings


# 할일 목록 리스트
class Todo(models.Model):
    text = models.CharField(max_length=40)
    complete = models.BooleanField(default=False)

    def __str__(self):
        return self.text


#로그인
class User(AbstractUser): 
    profile_img = models.ImageField(null=True, blank=True)


#포스트 메인,상세 페이지 모델
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='user_photos')
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    time = models.DateField(auto_now=True)

    head_image = models.ImageField(upload_to='mywish/images/%Y/%m/%d/', blank=True)
    file_upload = models.FileField(upload_to='mywish/files/%Y/%m/%d/', blank=True)

    class Meta:
        ordering = ['-updated_at']

    # 관리자페이지에서 글을 문자로 뿌려주는 역할
    def __str__(self):
        return self.author.username + " " + self.created_at.strftime("%Y-%m-%d %H:%M:%S")
    
    
    #메인페이지에서 제목을 클릭하면 상세페이지로 넘어가는 url
    def get_absolute_url(self):
        return reverse('post_detail', args=[self.id])
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author}::{self.content}'
    
    def get_absolute_url(self):
        return f'{self.post.get_absolute_url()}#comment-{self.pk}'
    
    
# user
# -> Post.objects.filter(user=user)
#  -> user.post_set.all() 
# 마이위시 페이지
class MyWish(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True) # related_name='my_post_set', 
    wish_list = models.CharField(max_length=50)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_wish', blank=True) # related_name='like_post_set',
    checked_wish = models.BooleanField(default=False)


    class Meta:
        verbose_name = 'mywish'
        verbose_name_plural = 'mywishes'

#인스턴스를 출력했을 때 만드는 내용
    def __str__(self):
        return "위시목록: " + self.wish_list
    
    # from django.urls import reverse 추가!
    def get_absolute_url(self):
        return reverse('my_wish', args=[str(self.id)]) # args=[(self.id)] 이렇게 들어가도 상관 없어
    

