from django.urls import path

from store import views

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.routers import DefaultRouter

routers=DefaultRouter()
routers.register("products",views.ProductView,basename="products")

urlpatterns = [
    path("register/",views.SignUpview.as_view()),
    path("token/",ObtainAuthToken.as_view()),
]+routers.urls
