from rest_framework  import serializers
from django.contrib.auth.models import User

from store.models import Product,BasketItem,Basket

class Userserializers(serializers.ModelSerializer):
    class Meta:
         model=User
         fields=["id","username","email","password"]
         read_only_fields=["id"]
    def create(self, validated_data):
         return User.objects.create_user(**validated_data)
    
class ProductSerializers(serializers.ModelSerializer):
     category=serializers.StringRelatedField()
     class Meta:
       model=Product
       fields="__all__"

class BasketItemserializers(serializers.ModelSerializer):
     product=ProductSerializers(read_only=True)
     total=serializers.IntegerField(read_only=True)
     
     class Meta:
       model=BasketItem
       fields="__all__"
       read_only_fields=["id","product","basket","created_at","updated_at","is_active","total"]

class Basketserializers(serializers.ModelSerializer):
     cart_items=BasketItemserializers(read_only=True,many=True)
     cart_item_quanity=serializers.CharField(read_only=True)
     sub_total=serializers.IntegerField(read_only=True)
     class Meta:
        model=Basket
        fields=["id","owner","created_at","updated_at","is_active","cart_items","cart_item_quanity","sub_total"]


   

    
