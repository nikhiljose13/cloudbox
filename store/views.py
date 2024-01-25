from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import authentication,permissions
from rest_framework.decorators import action
from rest_framework import serializers

from store.serializers import Userserializers,ProductSerializers,BasketItemserializers,Basketserializers
from store.models import Product,BasketItem



# Create your views here.

class SignUpview(APIView):
    def   post(self,request,*args,**kwargs):
        serializers=Userserializers(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(data=serializers.data)
        else:
           return Response(data=serializers.errors) 
        

class ProductView(viewsets.ModelViewSet):
       serializer_class=ProductSerializers
       queryset=Product.objects.all()
       authentication_classes=[authentication.TokenAuthentication]
       permission_classes=[permissions.IsAuthenticatedOrReadOnly]

    # url:http://127.0.0.1:8000/api/products/{id}/add_to_basket/
       
       @action(methods=["post"],detail=True)
       def add_to_basket(self,request,*args,**kwargs):
           id=kwargs.get("pk")
           product_object=Product.objects.get(id=id)
           basket_object=request.user.cart

           basket_products=request.user.cart.cartitem.all().values_list("product",flat=True)
           print(basket_products)
           if int(id) in basket_products:
                Basket_Item_object=BasketItem.objects.get(basket=basket_object,product__id=id)
                Basket_Item_object.quantity=Basket_Item_object.quantity+int(request.data.get("quantity",1))
                Basket_Item_object.save()
                serializers=BasketItemserializers(Basket_Item_object)
                return Response(data=serializers.data)



           serializers=BasketItemserializers(data=request.data)
           if serializers.is_valid():
              serializers.save(basket=basket_object,product=product_object)
              return Response(data=serializers.data)
           else:
              return Response(data=serializers.errors) 
         
       def create(self, request, *args, **kwargs):
             raise serializers.ValidationError("permission denied")
       
       def update(self, request, *args, **kwargs):
             raise serializers.ValidationError("permission denied")
       
       def destroy(self, request, *args, **kwargs):
             raise serializers.ValidationError("permission denied")
       

class BasketView(viewsets.ViewSet):
     authentication_classes=[authentication.TokenAuthentication]
     permission_classes=[permissions.IsAuthenticated]

     def list(self, request, *args, **kwargs):
         qs= request.user.cart 
         serializers=Basketserializers(qs)
         return Response(serializers.data)
          
class BasketItemView(viewsets.ModelViewSet):
     serializer_class=BasketItemserializers
     queryset=BasketItem.objects.all()
     authentication_classes=[authentication.TokenAuthentication]
     permission_classes=[permissions.IsAuthenticated]


     def perform_update(self, serializer):
          user=self.request.user
          owner=self.get_object().basket.owner
          if user==owner :
           return super().perform_update(serializer)
          else :
               raise serializers.ValidationError("permission denied")
          
     def perform_destroy(self, instance):
          user=self.request.user
          owner=self.get_object().basket.owner
          if user==owner :
           return super().perform_destroy(instance)
          else :
               raise serializers.ValidationError("permission denied")
     
     def create(self, request, *args, **kwargs):
             raise serializers.ValidationError("permission denied")
     
     def list(self, request, *args, **kwargs):
             raise serializers.ValidationError("permission denied")
     
     