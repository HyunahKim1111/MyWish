from django.urls import path
from . import views

urlpatterns = [
    path('login/my_page/', views.mypage, name='mypage'), # 로그인 후 마이페이지
    path('post/<int:pk>/', views.PostDetail.as_view(), name='post_single'), #포스트상세페이지 CBV방식
    path('post/', views.PostList.as_view(),name='post'), #포스트 메인페이지 CBV방식
    path('content/', views.youtube, name='youtube'), # 나는될놈 페이지

    # 마이위시
    path('mywish/', views.MywishListView.as_view(), name='list'), 
    path('mywish/add/', views.MywishCreateView.as_view(), name='add'),
    path('mywish/detail/<int:pk>/', views.MywishDetailView.as_view(), name='detail'),
    path('mywish/update/<int:pk>/', views.MywishUpdateView.as_view(), name='update'),
    path('mywish/delete/<int:pk>/', views.MywishDeleteView.as_view(), name='delete'),

    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("signup/", views.signup_view, name="signup"),

    path('', views.index, name='index'), # 메인
]