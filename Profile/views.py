from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated

# Importacion Models
from django.contrib.auth.models import User
from Profile.models import ProfileTable

# Importacion Serializers
from Profile.serializers import ProfileSerializer

import os.path
import json

# Create your views here.


class LoadProfile(APIView):

    def get_object(self, pk):
        try:
            return User.objects.get(id=pk)
        except User.DoesNotExist:
            return 0

    def put(self, request):
        if 'url_img' not in request.data:
            raise exceptions.ParseError("Ningun archivo seleccionado")
        file = request.data['url_img']
        userId = request.data['user_id']
        user = self.get_objectUser(userId)
        if(user != 0):
            serializer = ProfileSerializer(data=request.data)
            if serializer.is_valid():
                validated_data = serializer.validated_data
                profile = Profile(**validated_data)
                profile.save()
                serializerResponse = ProfileSerializer(profile)
                return Response(serializerResponse.data, status.HTTP_200_OK)
        return Response("error", status = status.HTTP_400_BAD_REQUEST)


class LoadProfileDetail(APIView):

    def get_object(self, pk):
        try:
            return ProfileTable.objects.get(pk=pk)
        except ProfileTable.DoesNotExist:
            return 0

    def get(self, request, pk, format=None):
        idResponse = self.get_object(pk)
        if idResponse != 0:
            idResponse = ProfileSerializer(idResponse)
            print(idResponse.data)
            user = User.objects.filter(id=pk).values()
            responseOk = self.responseCustom(idResponse.data, user, "success", status.HTTP_200_OK)
            return Response(responseOk)
        return Response("Error: No hay datos", status = status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        idResponse = self.get_object(pk)
        if 'image' not in request.data:
            raise exceptions.ParseError("Ningun archivo seleccionado")
        file = request.data['image']
        nombre, formato = os.path.splitext(file.name)
        urlFinal = ''.join(nombre+formato)
        urlFinal = 'http://localhost:8000/assets/img_profile/' + urlFinal
        request.data['url_img'] = urlFinal
        serializer = ProfileSerializer(idResponse, data=request.data)
        if serializer.is_valid():
            serializer.save()
            datas = serializer.data
            responseOk = self.responseCustom(idResponse.data, user, "success", status.HTTP_200_OK)
            return Response(responseOk)
        return Response("error", status = status.HTTP_400_BAD_REQUEST)

    def responseCustom(self, data, user, respuesta, status):
        data = self.responseUser(data, user)
        responseOk = {"messages": respuesta,
                      "pay_load": data, "status": status}
        responsOk = json.dumps(responseOk)
        return responseOk

    def responseUser(self, data, user):
        response = {
            "user": data.get('user'),
            "url_img": data.get('url_img'),
            "username": user[0]['username'],
            "first_name": user[0]['first_name'],
            "last_name": user[0]['last_name'],
            "email": user[0]['email'],
        }
        return response
