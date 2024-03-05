from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name = "home"),
    path("image/", views.image_response, name = "image-response")
]
