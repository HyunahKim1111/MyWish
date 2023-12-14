from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post

#포스트 메인페이지
class PostList(ListView):
    model = Post
    ordering = '-pk'

#포스트 상세페이지
class PostDetail(DetailView):
    model = Post

# 나는될놈 페이지
def content(request):
    return render(request,'mywish/content.html')

# 마이위시 페이지
def my_wish(request):
    return render(request, 'mywish/my_wish.html')

# 메인페이지
def index(request):
    return render(request, 'mywish/index.html')

# 로그인 페이지
def login(request):
    return render(request, 'mywish/login.html')

# 로그인 후 마이페이지
def mypage(request):
    return render(request, 'mywish/mypage.html')