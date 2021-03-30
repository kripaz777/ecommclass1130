from django.shortcuts import render
from django.views.generic.base import View
from .models import *
# Create your views here.
class BaseView(View):
    views = {}

class HomeView(BaseView):
    def get(self,request):
        self.views['categories'] = Category.objects.filter(status = 'active')
        self.views['sliders'] = Slider.objects.filter(status = 'active')
        self.views['brands'] = Brand.objects.filter(status = 'active')
        self.views['ads'] = Ad.objects.all()
        self.views['hots'] = Item.objects.filter(label = 'hot')
        self.views['news'] = Item.objects.filter(label = 'new')
        self.views['sales'] = Item.objects.filter(label='sale')
        self.views['defaults'] = Item.objects.filter(label='')
        return render(request,'index.html',self.views)