"""
URL configuration for movienight project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from collector import urls as collector_urls
from movieDetail import urls as movieDetail_urls


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(collector_urls, namespace="collector")),
    path("movieDetail/", include(movieDetail_urls, namespace="movieDetail")),  # movieDetail 앱의 URL 추가
]
