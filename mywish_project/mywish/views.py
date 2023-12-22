from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import Post, User
from django.contrib.auth import authenticate, login, logout

import requests
# duration 시간으로 보이기
from isodate import parse_duration
from django.conf import settings

# 로그인
def login_view(request):
    if request.method == "POST":
        # print로 뭐가 들어오는 지 볼 수 있어
        username = request.POST["username"] 
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            print("인증성공")
            login(request, user)
        else:
            print("인증실패")
    return render(request, "mywish/login.html")

def logout_view(request):
    logout(request)
    return redirect("mywish:login")
# redirect로 로그아웃 리턴해주기
# "user(app_name = "user"):login" 로그아웃이 끝나면 로그인페이지로 돌려주겠다

# 회원가입
def signup_view(request):

    if request.method == "POST":
        print(1, request.POST) # request.POST에 뭐가 들어있는지 print로 확인해보자
        profile_img = request.FILES['profile_img'] # model에 사진 넣을 공간을 만들어주자!
        username = request.POST["username"]
        password = request.POST["password"]
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        email = request.POST["email"]
        student_id = request.POST["student_id"]

        user = User.objects.create_user(username, email, password)
        user.last_name = lastname
        user.first_name = firstname
        user.student_id = student_id
        user.profile_img = profile_img
        user.save()

        return redirect("mywish:login") # 로그인 해보세요

    return render(request, "mywish/signup.html")

#포스트 메인페이지
class PostList(ListView):
    model = Post
    ordering = '-pk'

#포스트 상세페이지
class PostDetail(DetailView):
    model = Post

# 나는될놈 페이지
# def content(request):
#     return render(request,'mywish/content.html')

#유투브 영상 뿌리기
def youtube(request):
    videos = []
    if request.method == 'POST':
        search_url = 'https://www.googleapis.com/youtube/v3/search'
        video_url = 'https://www.googleapis.com/youtube/v3/videos'
        
        search_params = {
            'part': 'snippet',
            'q': request.POST['search'], # 원하는 검색어
            'maxResults':9,
            'key': settings.YOUTUBE_DATA_API_KEY,
            'type' : 'video'
        }

        r = requests.get(search_url, params=search_params)
        results = r.json()['items']

        video_ids = []
        for result in results:
            video_ids.append(result['id']['videoId'])

        if request.POST['submit'] == 'lucky':
            return redirect(f'https://www.youtube.com/watch?v={ video_ids[0] }')

        video_params = {
            'key': settings.YOUTUBE_DATA_API_KEY,
            'part': 'snippet, contentDetails',
            'id' : ','.join(video_ids), # vidoe_id마다 ','로 연결시키기
            'maxResults':9

        }
        r = requests.get(video_url, params=video_params)
        results = r.json()['items']


        for result in results:
            video_data = {
                'title' : result['snippet']['title'],
                'id' : result['id'],
                'url' : f'https://www.youtube.com/watch?v={ result["id"] }',
                'duration' : int(parse_duration(result['contentDetails']['duration']).total_seconds() // 60),
                'thumbnail' : result['snippet']['thumbnails']['high']['url']
            }
            videos.append(video_data)

    context = {
        'videos' : videos
    }
        
    return render(request, 'mywish/youtube.html', context)

# youtube API가져오기 https://developers.google.com/youtube/v3/docs/search/list

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