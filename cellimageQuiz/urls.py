"""cellimageQuiz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from dal import autocomplete
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from cellimageQuizApp.importdata import importData
from cellimageQuizApp.models import Image, Answer, Question
from cellimageQuizApp.views import index, sign_up, FilteredImagesListView, playquizz, information

urlpatterns = [
    path('admin/', admin.site.urls),
    path('data/', importData),
    path('', index, name='index'),
    path('sign_up/', sign_up),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('model_information/', information),
    path('exploreimages/', FilteredImagesListView.as_view()),
    path('quiz/<choiceCategory>/', playquizz),
    #path('quiz/microscopy', playquizz),
    #path('quiz/component', playquizz),
    url(  # Register the autocomplete view
          'images-autocomplete/$',
          autocomplete.Select2QuerySetView.as_view(model=Image),
          name='images-autocomplete',
    ),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
