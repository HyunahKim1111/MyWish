from django.urls import path
from . import views

urlpatterns = [
    # 포스트 페이지
    path('post/', views.post_list, name='post_list'), #포스트 메인페이지 
    path('post/upload/', views.PostUploadView.as_view(), name='post_upload'), # 생성
    path('post/delete/<int:pk>/', views.PostDeleteView.as_view(), name='post_delete'), # 삭제
    path('post/update/<int:pk>/', views.PostUpdateView.as_view(), name='post_update'), # 수정
    path('post/detail/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'), #포스트 상세페이지
    path('post/detail/<int:pk>/new_comment/', views.new_comment, name='new_comment'),

    path('content/', views.youtube, name='youtube'), # 나는될놈 페이지
    path('mywish/', views.MyWishListView.as_view(), name='my_wish'), # 마이위시 페이지
    path('mywish/<int:pk>/likes/', views.likes, name='likes'), # 좋아요
    path('mywish/<int:pk>/checked/', views.checked_wish, name='checked_wish'), # 체크박스 위시
    path('submit-wishes/', views.SubmitWishesView.as_view(), name='submit_wishes'),  # 이 URL을 추가해주세요.
    path('mypage/', views.mypage_view, name='mypage_view'),
    
    
    # 로그인
    path("accounts/login/", views.login_view, name="login"),
    path("accounts/logout/", views.logout_view, name="logout"),
    path("accounts/signup/", views.signup_view, name="signup"),
    path('accounts/login/todolist/', views.todo_index, name='todo_list'), # 로그인 후 마이페이지(todo_list)
    path('accounts/login/todolist/add/', views.addTodo, name='add'), 
    path('accounts/login/todolist/complete/<todo_id>/', views.completeTodo, name='complete'),
    path('accounts/login/todolist/deletecomplete/', views.deleteCompleted, name='deletecomplete'),
    path('accounts/login/todolist/deleteall/', views.deleteAll, name='deleteall'),
    
    # 로그인 후 마이페이지
    path('accounts/login/my_page/', views.mypage_view, name='mypage'), 
    

    path('', views.index, name='index'), # 메인
]