from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

#Importaciones de modelos
from primerComponente.models import PrimerTabla

#Importaciones de serializadores
from primerComponente.serializers import PrimerTablaSerializer

#Importacion JSON
import json

# Create your views here.

class PrimerTablaList(APIView):
    def get(self, request, format=None):
        queryset = PrimerTabla.objects.all()
        serializer = PrimerTablaSerializer(queryset, many = True, context = {'request':request})
        responseOk = self.responseCustom(serializer.data, "success", status.HTTP_200_OK)
        return Response(responseOk)

    def post(self, request, format=None):
        serializer = PrimerTablaSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            datas = serializer.data
            responseOk = self.responseCustom(datas, "success", status.HTTP_201_CREATED)
            return Response(responseOk)
        responseOk = self.responseCustom(serializer.errors, "error", status.HTTP_400_BAD_REQUEST)
        return Response(responseOk)

    def responseCustom(self, data, respuesta, status):
        responseOk = {"messages": respuesta, "pay_load": data, "status": status}
        return responseOk


class PrimerTablaDetail(APIView):
    def get_object(self, pk):
        try:
            return PrimerTabla.objects.get(pk = pk)
        except PrimerTabla.DoesNotExist:
            return 0

    def get(self, request,pk, format=None):
        idResponse = self.get_object(pk)
        print(idResponse)
        if idResponse != 0:
            idResponse = PrimerTablaSerializer(idResponse)
            return Response(idResponse.data, status = status.HTTP_200_OK)
        return Response("No hay datos", status = status.HTTP_400_BAD_REQUEST)

    def put(self, request,pk, format=None):
        idResponse = self.get_object(pk)
        serializer = PrimerTablaSerializer(idResponse, data = request.data)
        if serializer.is_valid():
            serializer.save()
            datas = serializer.data
            return Response(datas, status = status.HTTP_201_CREATED)
        return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request,pk, format=None):
        idResponse = self.get_object(pk)
        if idResponse !="No existe":
            idResponse.delete()
            return Response("Datos eliminado", status = status.HTTP_201_CREATED)
        return Response("error",status = status.HTTP_400_BAD_REQUEST)
