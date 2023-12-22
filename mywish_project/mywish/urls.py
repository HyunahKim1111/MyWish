from django.urls import path
from . import views

urlpatterns = [
    path('login/my_page/', views.mypage, name='mypage'), # 로그인 후 마이페이지
    #path('login/', views.login), # 로그인 페이지
    path('post/<int:pk>/', views.PostDetail.as_view(), name='post_single'), #포스트상세페이지 CBV방식
    path('post/', views.PostList.as_view(),name='post'), #포스트 메인페이지 CBV방식
    path('content/', views.youtube, name='youtube'), # 나는될놈 페이지
    path('my_wish/', views.my_wish, name='my_wish'), # 마이위시 페이지
    path('', views.index, name='index'), # 메인

    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("signup/", views.signup_view, name="signup"),
]