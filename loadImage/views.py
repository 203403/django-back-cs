from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from asyncio import exceptions
import os.path

#Importaciones de modelos
from loadImage.models import TablaImages

#Importaciones de serializadores
from loadImage.serializers import TablaSerializerImg

#Importacion JSON
import json

# Create your views here.

    
class TablaListImg(APIView):
    
    def get(self, request, format=None):
        queryset = TablaImages.objects.all()
        serializer = TablaSerializerImg(queryset, many = True, context = {'request':request})
        responseOk = self.responseCustom(serializer.data, "success", status.HTTP_200_OK)
        return Response(responseOk)

    def post(self, request, format=None):
        if 'image' not in request.data:
                raise exceptions.ParseError("Ningun archivo seleccionado") 
        file = request.data['image']
        nombre, formato = os.path.splitext(file.name)
        urlFinal = ''.join(nombre+formato)
        urlFinal = 'http://localhost:8000/assets/img/' + urlFinal
        request.data['name_img'] = nombre
        request.data['format_img'] = formato
        request.data['url_img'] = urlFinal
        serializer = TablaSerializerImg(data=request.data)   
        if serializer.is_valid():
            validated_data = serializer.validated_data
            image = TablaImages(**validated_data)
            image.save()
            serializeResponse = TablaSerializerImg(image)
            data = serializeResponse.data
            responseOk = self.responseCustom(data, "success", status.HTTP_201_CREATED)
            return Response(responseOk)
        responseOk = self.responseCustom(serializer.errors, "error", status.HTTP_400_BAD_REQUEST)
        return Response(responseOk)

    def responseCustom(self, data, respuesta, status):
        responseOk = {"messages": respuesta, "pay_load": data, "status": status}
        return responseOk

class TablaImagesDetail(APIView):
    def get_object(self, pk):
        try:
            return TablaImages.objects.get(pk = pk)
        except TablaImages.DoesNotExist:
            return 0

    def get(self, request,pk, format=None):
        idResponse = self.get_object(pk)
        if idResponse != 0:
            idResponse = TablaSerializerImg(idResponse)
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
        urlFinal = 'http://localhost:8000/assets/img/' + urlFinal
        request.data['name_img'] = nombre
        request.data['format_img'] = formato
        request.data['url_img'] = urlFinal
        serializer = TablaSerializerImg(idResponse, data = request.data)
        if serializer.is_valid():
            serializer.save()
            datas = serializer.data
            responseOk = self.responseCustom(datas, "success", status.HTTP_201_CREATED)
            return Response(responseOk)
        responseOk = self.responseCustom(serializer.errors, "error", status.HTTP_400_BAD_REQUEST)
        return Response(responseOk)

    def delete(self, request, pk):
        idResponse = self.get_object(pk)
        if idResponse != 0:
            idResponse.image.delete()
            idResponse.delete()
            responseOk = self.responseCustom("Datos eliminados", "success", status.HTTP_201_CREATED)
            return Response(responseOk)
        responseOk = self.responseCustom("no hay datos", "error", status.HTTP_400_BAD_REQUEST)
        return Response(responseOk)
    
    def responseCustom(self, data, respuesta, status):
        responseOk = {"messages": respuesta, "pay_load": data, "status": status}
        return responseOk