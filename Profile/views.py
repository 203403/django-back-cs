from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated

#Importacion Models
from django.contrib.auth.models import User
from Profile.models import ProfileTable

#Importacion Serializers
from Profile.serializers import ProfileSerializer

import os.path
import json

# Create your views here.
class LoadProfile(APIView):
   
    def get(self, request, format=None):
        queryset = ProfileTable.objects.all()
        serializer = ProfileSerializer(queryset, many = True, context = {'request':request})
        responseOk = self.responseCustom(serializer.data, "success", status.HTTP_200_OK)
        return Response(responseOk)

    
    def post(self, request):
        if 'image' not in request.data:
            raise exceptions.ParseError("Ningun archivo seleccionado") 
        file = request.data['image']
        nombre, formato = os.path.splitext(file.name)
        urlFinal = ''.join(nombre+formato)
        urlFinal = 'http://localhost:8000/assets/img_profile/' + urlFinal
        request.data['url_img'] = urlFinal
        serializer = ProfileSerializer(data=request.data)   
        if serializer.is_valid():
            validated_data = serializer.validated_data
            userProfile = ProfileTable(**validated_data)
            userProfile.save()
            serializeResponse = ProfileSerializer(userProfile)
            responseOk = self.responseCustom(serializeResponse, "success", status.HTTP_201_CREATED)
            return Response(responseOk)
        responseOk = self.responseCustom(serializeResponse.errors, "error", status.HTTP_400_BAD_REQUEST)
        return Response(responseOk)
    
    def responseCustom(self, data, respuesta, status):
        responseOk = {"messages": respuesta,
                    "pay_load": data, "status": status}
        responsOk = json.dumps(responseOk)
        return responseOk


class LoadProfileDetail(APIView):
    
    def get_object(self, pk):
        try:
            return ProfileTable.objects.get(user_id = pk)
        except ProfileTable.DoesNotExist:
            return 0

    def get(self, request,pk, format=None):
        idResponse = self.get_object(pk)
        if idResponse != 0:
            idResponse = ProfileSerializer(idResponse)
            responseOk = self.responseCustom(idResponse.data, "success", status.HTTP_200_OK)
            return Response(responseOk)
        responseOk = self.responseCustom("No hay datos", "error", status.HTTP_400_BAD_REQUEST)
        return Response(responseOk)

    def put(self, request,pk, format=None):
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
            responseOk = self.responseCustom(datas, "success", status.HTTP_201_CREATED)
            return Response(responseOk)
        responseOk = self.responseCustom(serializer.errors, "error", status.HTTP_400_BAD_REQUEST)
        return Response(responseOk)

    def responseCustom(self, data, respuesta, status):
        responseOk = {"messages": respuesta,
                      "pay_load": data, "status": status}
        responsOk = json.dumps(responseOk)
        return responseOk
