from django.urls import path, re_path
from django.conf.urls import include

 
from Registro.views import UserAPI

urlpatterns = [
    re_path(r'^create/$', UserAPI.as_view()),    
]