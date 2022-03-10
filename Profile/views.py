from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import exceptions

# Importacion Models
from django.contrib.auth.models import User
from Profile.models import ProfileTable

# Importacion Serializers
from Profile.serializers import ProfileSerializer

import os.path
import json

# Create your views here.


class CreateNewProfile(APIView):
    def post(self, request):
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            profileInitial = ProfileTable(**validated_data)
            profileInitial.save()
            serializerResponse = ProfileSerializer(profileInitial)
            return Response("success", status=status.HTTP_200_OK)
        return Response("Error: No es puede procesar la solicitud", status=status.HTTP_400_BAD_REQUEST)


class LoadProfileImage(APIView):

    def get_object(self, pk):
        try:
            return ProfileTable.objects.get(pk=pk)
        except ProfileTable.DoesNotExist:
            return 0

    def put(self, request, pk, format=None):
        idResponse = self.get_object(pk)
        if 'url_img' not in request.data:
            raise exceptions.ParseError("Ningun archivo seleccionado")
        file = request.data['url_img']
        urlFinal = ''.join(file.name)
        urlFinal = 'http://localhost:8000/assets/img_profile/' + urlFinal
        request.data['url_img'] = urlFinal
        if(idResponse != 0) :
            serializer = ProfileSerializer(idResponse)
            idResponse.url_img = file
            idResponse.save()
            return Response("success", status =status.HTTP_200_OK)
        return Response("Error: No es puede procesar la solicitud", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        profileImg = self.get_object(pk)
        if profileImg != 0:
            profileImg.url_img.delete()
            return Response("La imagen fue eliminada", status=status.HTTP_204_NO_CONTENT)
        return Response("Error al buscar la imagen", status=status.HTTP_400_BAD_REQUEST)

    def responseCustom(self, data, respuesta, status):
        responseOk = {"messages": respuesta,
                      "pay_load": data, "status": status}
        responsOk = json.dumps(responseOk)
        return responseOk


class ProfileUserData(APIView):

    def get_object(self, pk):
        try:
            return ProfileTable.objects.get(pk=pk)
        except ProfileTable.DoesNotExist:
            return 0

    def get(self, request, pk, format=None):
        idResponse = self.get_object(pk)
        if idResponse != 0:
            idResponse = ProfileSerializer(idResponse)
            user = User.objects.filter(id=pk).values()
            responseOk = self.responseCustom(
                idResponse.data, user, "success", status.HTTP_200_OK)
            return Response(responseOk)
        return Response("Error: No hay datos", status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        data = request.data
        if data is not None:
            user = User.objects.filter(pk=pk)
            user.update(username=data.get('username'))
            user.update(first_name=data.get('first_name'))
            user.update(last_name=data.get('last_name'))
            user.update(email=data.get('email'))
            return Response("Actualizcion exitosa", status.HTTP_200_OK)
        return Response("Error inesperado", status=status.HTTP_400_BAD_REQUEST)

    def responseCustom(self, data, user, respuesta, status):
        data = self.responseUser(data, user)
        responseOk = {"messages": respuesta,
                      "pay_load": data, "status": status}
        responsOk = json.dumps(responseOk)
        return responseOk

    def responseUser(self, data, usuario):
        response = {
            "user": data.get('user'),
            "url_img": data.get('url_img'),
            "username": usuario[0]['username'],
            "first_name": usuario[0]['first_name'],
            "last_name": usuario[0]['last_name'],
            "email": usuario[0]['email'],
        }
        return response
