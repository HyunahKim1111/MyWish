from typing import Any
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, User, MyWish, Todo
from .forms import TodoForm, CommentForm, MyWishForm
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic.base import View # 좋아요 기능 구현
from django.http import HttpResponseForbidden, JsonResponse
from django.http import HttpResponseRedirect

import requests
# duration 시간으로 보이기
from isodate import parse_duration
from django.conf import settings

# 로그인 후 마이페이지(todo_list)
def todo_index(request):
    todo_list = Todo.objects.order_by('id')

    form = TodoForm()
    context = {'todo_list' : todo_list, 'form' : form}

    return render(request, 'mywish/todolist.html', context)

@require_POST
def addTodo(request):
    form = TodoForm(request.POST)

    if form.is_valid():
        new_todo = Todo(text=request.POST['text'])
        new_todo.save()

    return redirect('todo_list')

def completeTodo(request, todo_id):
    todo = Todo.objects.get(pk=todo_id)
    todo.complete = True
    todo.save()

    return redirect('todo_list')

def deleteCompleted(request):
    Todo.objects.filter(complete__exact=True).delete()

    return redirect('todo_list')

def deleteAll(request):
    Todo.objects.all().delete()

    return redirect('todo_list')

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
            return redirect('todo_list')# 마이페이지로 리디렉션
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
    
    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data()
        context['comment_form'] = CommentForm
        return context
    
# 댓글기능 
def new_comment(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=pk)

        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                return redirect(comment.get_absolute_url())
            # comment_form이 유효하지 않은 경우, 다시 해당 포스트로 리디렉션
            return redirect(post.get_absolute_url())
        else:
            return redirect(post.get_absolute_url())
    else:
        raise PermissionDenied
    


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
class MyWishListView(ListView):
    model = MyWish
    template_name = 'mywish/my_wish.html'

def checked_wish(request):
    if request.method == 'POST':
        # 전송된 체크박스 데이터 확인
        checked_wish_items = request.POST.getlist('checked_wish')
        
        # checked_wish_items를 활용하여 원하는 처리 수행
        
        # 예시: 선택된 위시를 확인하고 처리하는 코드
        for wish_id in checked_wish_items:
            # wish_id를 이용하여 해당 위시 객체 가져오기
            wish_item = MyWish.objects.get(id=wish_id)
            # 원하는 처리 수행
            wish_item.checked_wish = True
            wish_item.save()

        return HttpResponseRedirect('/success/')  # 성공적으로 처리되었을 때의 리디렉션 URL
    else:
        form = MyWishForm()
        # 다른 로직 수행 혹은 특정 페이지 렌더링
        return render(request, 'my_wish.html', {'form': form})


class CheckedWishView(View):
    def checked_wish(self, request, pk):
        if request.user.is_authenticated:
            checked_wish_ids = request.POST.getlist('wishes') # 체크된 위시 목록을 가져옴
            # 현재 로그인한 사용자의 MyWish 객체 가져오기
            user_wish = MyWish.objects.filter(user=request.user)
            # 해당 MyWish 객체의 checked_wish 필드 업데이트
            for wish in user_wish:
                if str(wish.id) in checked_wish_ids:
                    wish.checked_wish = True
                else:
                    wish.checked_wish = False
                wish.save()
            return reverse('mypage')
        else:
            return HttpResponseForbidden("로그인이 필요합니다.")
        
class SubmitWishesView(View):
    def post(self, request):
        if request.user.is_authenticated:
            selected_wishes = request.POST.getlist('wishes')  # 선택된 위시 목록을 가져옵니다.
            
            # 현재 로그인한 사용자의 MyWish 객체 가져오기
            user_wishes = MyWish.objects.filter(user=request.user)
            # 선택된 위시에 해당하는 객체들을 가져와 checked_wish를 True로 설정
            for wish in user_wishes:
                if str(wish.id) in selected_wishes:
                    wish.checked_wish = True
                    wish.save()
                else:
                    wish.checked_wish = False
                    wish.save()

            return JsonResponse({'message': '위시가 성공적으로 저장되었습니다.'})
        else:
            return JsonResponse({'error': '로그인이 필요합니다.'}, status=401)   

def likes(request, pk):
    if request.user.is_authenticated:
        mywish = get_object_or_404(MyWish, pk=pk)

        if mywish.like_users.filter(pk=request.user.pk).exists():
            mywish.like_users.remove(request.user)
        else:
            mywish.like_users.add(request.user)
        return redirect('my_wish')
    return redirect('login')

# 체크된 위시를 mypage로 전달하기
def mypage_view(request):
    if request.user.is_authenticated:
        checked_wishes = MyWish.objects.filter(user=request.user, checked_wish=True)
        # 필터링된 checked_wish가 True인 MyWish 객체들을 가져옴
        return render(request, 'mywish/mypage.html', {'checked_wishes':checked_wishes})
    else:
        return render(request, 'login.html') # 인증되지 않은 사용자의 경우 다른 처리를 할 수 있음

# def mypage(request):
#     return render(request, 'mywish/mypage.html')

# 메인페이지
def index(request):
    return render(request, 'mywish/index.html')
