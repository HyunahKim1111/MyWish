from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, User
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.urls import reverse_lazy

import requests
# duration 시간으로 보이기
from isodate import parse_duration
from django.conf import settings

def login_view(request):
    if request.method == "POST":
        print(request.POST)
        # print로 뭐가 들어오는 지 볼 수 있어
        username = request.POST["username"] 
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            print("인증성공")
            auth_login(request ,user)
        else:
            print("인증실패")
    return render(request, "mywish/login.html")

def logout_view(request):
    logout(request)
    return redirect('index')
# redirect로 로그아웃 리턴해주기

# 회원가입
def signup_view(request):

    if request.method == "POST":
        print(1, request.POST) # request.POST에 뭐가 들어있는지 print로 확인해보자
        print(2, request.FILES)
        profile_img = request.FILES['profile_img'] 
        username = request.POST["username"]
        password = request.POST["password"]
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        email = request.POST["email"]

        user = User.objects.create_user(username, email, password)
        user.last_name = lastname
        user.first_name = firstname
        user.profile_img = profile_img
        user.save()

        return redirect("login") # 로그인창으로 보내기

    return render(request, "mywish/signup.html")


#포스트 메인페이지(함수뷰)
def post_list(request):
    posts = Post.objects.all()
    return render(request, 'mywish/post_list.html', {'posts':posts})

class PostUploadView(CreateView):
    model = Post
    fields = ['head_image', 'content'] # 작성자는 로그인하면 저절로! 작성시간은 auto_now가 있어서 자동으로 된다.
    template_name = 'mywish/post_upload.html'

# 로그인을 했다는 전제로 업로드를 하는것임.
    def form_valid(self, form): # 저장 전에 데이터가 올바른지 처리해줌. 올바르면 저장하겠다.
        form.instance.author_id = self.request.user.id
        if form.is_valid():
            # 데이터가 올바르다면 저장을 하겠다.
            form.instance.save() # form안에는 Post모델에 있는 instance가 존재한다. 그래서 Post모델의 instance를 저장한거야.
            return redirect('post_list')
        else:
            return self.render_to_response({'form':form})
        
class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')
    template_name = 'mywish/post_delete.html'

class PostUpdateView(UpdateView):
    model = Post
    fields = ['head_image', 'content']
    template_name = 'mywish/post_update.html'

#포스트 상세페이지
class PostDetailView(DetailView):
    model = Post
    fields = ['head_image', 'content']
    template_name = 'mywish/post_detail.html'


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