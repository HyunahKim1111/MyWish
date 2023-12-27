from django.contrib import admin
from .models import Post, User, Mywish

admin.site.register(Post)
admin.site.register(User)
admin.site.register(Mywish) # model에 만든 class 등록하기

