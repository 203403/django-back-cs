from django.urls import path, re_path
from django.conf.urls import include

#Importacion de vistas
from loadImage.views import TablaListImg
from loadImage.views import TablaImagesDetail

urlpatterns = [
    re_path(r'^image/$', TablaListImg.as_view()),
    re_path(r'^image/(?P<pk>\d+)$', TablaImagesDetail.as_view()),
]