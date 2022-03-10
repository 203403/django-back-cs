from django.urls import path, re_path
from django.conf.urls import include

# Importacion de vistas
from Profile.views import LoadProfileImage
from Profile.views import ProfileUserData

urlpatterns = [
    re_path(r'^user/$', LoadProfileImage.as_view()),
    re_path(r'^user/(?P<pk>\d+)$', ProfileUserData.as_view()),
    re_path(r'^user-img/(?P<pk>\d+)$', LoadProfileImage.as_view()),
]
