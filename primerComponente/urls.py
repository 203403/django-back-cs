from django.urls import path, re_path
from django.conf.urls import include

#Importacion de vistas
from primerComponente.views import PrimerTablaList
from primerComponente.views import PrimerTablaDetail

urlpatterns = [
    re_path(r'^lista/$', PrimerTablaList.as_view()),
    re_path(r'^lista/(?P<pk>\d+)$', PrimerTablaDetail.as_view()),
]