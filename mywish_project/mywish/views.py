from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import Post

import requests
# duration 시간으로 보이기
from isodate import parse_duration
from django.conf import settings

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