from django.urls import path, re_path
from django.conf.urls import include

# Importacion de vistas
from Profile.views import LoadProfile
from Profile.views import LoadProfileDetail

urlpatterns = [
    re_path(r'^user/$', LoadProfile.as_view()),
    re_path(r'^user/(?P<pk>\d+)$', LoadProfileDetail.as_view()),

]
