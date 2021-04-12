from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from .models import *
# Serializers define the API representation.
class ItemSerializers(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"