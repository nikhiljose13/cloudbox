from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save

class Category(models.Model):
    name=models.CharField(max_length=200,unique=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    title=models.CharField(max_length=200)
    price=models.PositiveIntegerField()
    description=models.CharField(max_length=200)
    picture=models.ImageField(upload_to="images",default="default.jpg")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=True)
    is_trending=models.BooleanField(default=False)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Basket(models.Model):
    owner=models.OneToOneField(User,on_delete=models.CASCADE,related_name="cart")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=True)

    @property
    def cart_items(self):
         return self.cartitem.all()
    
    @property
    def cart_item_quanity(self):
         qs=self.cart_items
         return len(qs)

class BasketItem(models.Model):
    basket=models.ForeignKey(Basket,on_delete=models.CASCADE,related_name="cartitem")
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=True)

def create_basket(sender,instance,created,**kwargs):
        if created:
            Basket.objects.create(owner=instance)
post_save.connect(create_basket,sender=User)