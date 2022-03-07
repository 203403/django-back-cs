from rest_framework import routers, serializers, viewsets
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

#Importancion de modelos
from Profile.models import ProfileTable

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileTable
        fields = ('username', 'email', 'first_name', 'last_name','user_id', 'url_img')
