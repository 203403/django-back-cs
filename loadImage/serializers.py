from rest_framework import routers, serializers, viewsets

#Importancion de modelos
from loadImage.models import TablaImages

class TablaSerializerImg(serializers.ModelSerializer):
    class Meta:
        model = TablaImages
        fields = ("id", "name_img", "url_img", "format_img", "image")
