"""
URL configuration for Music project.

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
from django.urls import path
from django.contrib.auth import views as auth_views
from home.views import home, register, mimicking_page, tune_page, frontend, recommendation, listen2gether, piano, guitar, violien, login_page 
from django.conf.urls.static import static
from django.conf import settings 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', frontend , name='frontend'), 
    # path('', recommendation),
    path('register/', register, name='register'), 
    path('login/', login_page, name='login_page'), 
    path('frontend/', frontend),
    path('logout/', auth_views.LogoutView.as_view(next_page='login_page'), name='logout'),
    path('recommendation/', recommendation, name='recommendation'),
    path('mimicking_page/', mimicking_page, name='mimicking_page'),
    path('tune_page/', tune_page, name='tune_page'),
    path('listen2gether/', listen2gether, name='listen2gether'),
    path('piano/', piano, name='piano'),
    path('guitar/', guitar, name='guitar'),
    path('violen/', violien, name='violien'),  

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
