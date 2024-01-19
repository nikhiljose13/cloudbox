from rest_framework  import serializers
from django.contrib.auth.models import User

from store.models import Product

class Userserializers(serializers.ModelSerializer):
    class Meta:
         model=User
         fields=["id","username","email","password"]
         read_only_fields=["id"]
    def create(self, validated_data):
         return User.objects.create_user(**validated_data)
    
class ProductSerializers(serializers.ModelSerializer):
     class Meta:
       model=Product
       fields="__all__"