from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets

from store.serializers import Userserializers,ProductSerializers
from store.models import Product

# Create your views here.

class SignUpview(APIView):
    def   post(self,requset,*args,**kwargs):
        serializers=Userserializers(data=requset.data)
        if serializers.is_valid():
            serializers.save()
            return Response(data=serializers.data)
        else:
           return Response(data=serializers.errors) 
        

class ProductView(viewsets.ModelViewSet):
       serializer_class=ProductSerializers
       queryset=Product.objects.all()