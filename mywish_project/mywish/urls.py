from django.urls import path
from . import views

urlpatterns = [
    # 포스트 페이지
    path('post/', views.post_list, name='post_list'), #포스트 메인페이지 
    path('post/upload/', views.PostUploadView.as_view(), name='post_upload'), # 생성
    path('post/delete/<int:pk>/', views.PostDeleteView.as_view(), name='post_delete'), # 삭제
    path('post/update/<int:pk>/', views.PostUpdateView.as_view(), name='post_update'), # 수정
    path('post/detail/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'), #포스트 상세페이지(댓글)

    path('content/', views.youtube, name='youtube'), # 나는될놈 페이지
    path('my_wish/', views.my_wish, name='my_wish'), # 마이위시 페이지
    
    # 로그인
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("signup/", views.signup_view, name="signup"),

    # 로그인 후 마이페이지
    path('login/my_page/', views.mypage, name='mypage'), 

    path('', views.index, name='index'), # 메인
]