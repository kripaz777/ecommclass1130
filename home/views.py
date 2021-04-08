from django.shortcuts import render,redirect
from django.views.generic.base import View
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
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

class ItemDetailView(BaseView):
    def get(self,request,slug):
        self.views['item_detail'] = Item.objects.filter(slug= slug)
        self.views['brand'] = Brand.objects.filter(status = 'active')
        self.views['count'] = []
        for i in self.views['brand']:
            count_food = Item.objects.filter(brand = i.id).count()
            d = {'name':i.name,'count':count_food}
            self.views['count'].append(d)

        self.views['count_cat'] = Category.objects.filter(status='active')
        self.views['cat_count'] = []
        for i in self.views['count_cat']:
            count_food = Item.objects.filter(category = i.id).count()
            dd = {'name':i.name,'image':i.image,'cat_count':count_food}
            self.views['cat_count'].append(dd)


        cat = Item.objects.get(slug = slug).category_id
        self.views['catitems'] = Item.objects.filter(category = cat)
        self.views['reviews'] = Review.objects.filter(slug= slug)
        return render(request,'product-detail.html',self.views)

def review(request):
    if request.method == 'POST':
        rating = request.POST['rating']
        review = request.POST['review']
        slug = request.POST['slug']
        username = request.user.username
        email = request.user.email

        user_review = Review.objects.create(
            rating = rating,
            review = review,
            username = username,
            email = email,
            slug = slug
        )
        user_review.save()
        return redirect(f'/products/{slug}')

class CategoryView(BaseView):
    def get(self,request,slug):
        cat_id = Category.objects.get(slug = slug).id
        self.views['catdetail'] = Item.objects.filter(category = cat_id)
        return render(request, 'product-list.html', self.views)

class SearchView(BaseView):
    def get(self,request):
       # query = request.GET.get('search',None)
       if request.method == 'GET':
            query = request.GET['search']
            self.views['search_product'] = Item.objects.filter(title__icontains = query)
            return render(request,'search.html',self.views)

       return render(request, 'search.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        fname = request.POST['fname']
        lname = request.POST['lname']
        if password == cpassword:
            if User.objects.filter(username = username).exists():
                messages.error(request,'This username is already taken')
                return redirect('home:account')

            elif User.objects.filter(email = email).exists():
                messages.error(request,'This email is already taken.')
                return redirect('home:account')

            else:
                user = User.objects.create_user(
                    username = username,
                    email = email,
                    password = password,
                    first_name = fname,
                    last_name = lname
                )
                user.save()
                messages.success(request,'You are registered.')
                return redirect('/')

        else:
            messages.error(request, 'These passwords do not match.')
            return redirect('home:account')

    return render(request, 'signup.html')

