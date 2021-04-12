from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers
from .views import ItemViewSet,ItemListView

router = routers.DefaultRouter()
router.register(r'item', ItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('filter_item/',ItemListView.as_view(),name = 'filter_item')
]