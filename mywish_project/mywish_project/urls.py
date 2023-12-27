"""
URL configuration for mywish_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static # static을 서빙해줌.


urlpatterns = [
    
    path('', include('mywish.urls')),
    path('accounts/', include('mywish.urls')),
    path('admin/', admin.site.urls),
    
]
# media파일의 url설정 DEBUG모드일 때 - static기능을 사용한다.
# 서비스 배포시 방법1. 미디어 파일 서버를 별도로 두고 사용한다. 방법2.웹서버에서 별도로 서빙 성정을 한다. nginx나 아파치같은 거 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)