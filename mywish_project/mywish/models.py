from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.urls import reverse

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
    

