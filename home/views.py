from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from home.forms import SignUpForm, SearchForm
from home.models import Setting, ContactFormMessage, ContactFormu, FAQ
from product.models import Product, Category, Comment, Images


def index(request):
    setting = Setting.objects.get(pk=1)
    sliderdata = Product.objects.all()
    lastproducts = Product.objects.all().order_by('-id')[:6]
    randomproducts = Product.objects.all().order_by('?')[:3]
    dayproducts = Product.objects.all()[:6]
    category=Category.objects.all()
    context = {'setting': setting,
               'page': 'home',
               'sliderdata': sliderdata,
               'lastproducts':lastproducts,
               'randomproducts':randomproducts,
               'dayproducts':dayproducts,
               'category': category}
    return render(request, 'index.html', context)


def hakkimizda(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context = {'setting': setting, 'page': 'hakkimizda','category':category,}
    return render(request, 'hakkimizda.html', context)


def referanslar(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context = {'setting': setting, 'page': 'referanslar','category':category,}
    return render(request, 'referanslar.html', context)


def iletisim(request):
    if request.method == 'POST':
        form = ContactFormu(request.POST)
        if form.is_valid():
            data = ContactFormMessage()
            data.name = form.cleaned_data['name']  # formdan bilgiyi al
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()  # veritabanına kaydet
            messages.success(request, "Mesajınız başarı ile gönderilmişitir. Teşekkür Ederiz")
            return HttpResponseRedirect('/iletisim')
    else:
        form = ContactFormu()
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting, 'form': form,'category':category,}
    return render(request, 'iletisim.html', context)


def category_products(request,id,slug):
    products = Product.objects.filter(category_id=id)
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    categorydata = Category.objects.get(pk=id)
    productx = Product.objects.all()[:3]
    producty = Product.objects.all().order_by('?')[:9]
    context = {'products':products,
               'category':category,
               'slug':slug,
               'setting': setting,
               'categorydata':categorydata,
               'productx': productx,
               'producty': producty,
               }
    return render(request,'products.html',context)


def product_detail(request,id,slug):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    product = Product.objects.get(pk=id)
    lastproducts = Product.objects.all().order_by('-id')[:4]
    comments = Comment.objects.filter(product_id=id, status='True')
    producty = Product.objects.all().order_by('?')[:3]
    image = Images.objects.filter(product_id=id)
    context = {
                'product':product,
                'producty':producty,
               'category': category,
               'slug': slug,
               'setting': setting,
        'lastproducts': lastproducts,
        'comments':comments,
        'image':image,
               }
    return render(request,'product_detail.html',context)



def logout_view(request):
    logout(request)

    return HttpResponseRedirect('/')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, "Giriş başarısız. Tekrar Deneyiniz.")
            return HttpResponseRedirect('/login')
    category = Category.objects.all()
    context = {
        'category': category,
    }
    return render(request, 'login.html', context)


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return HttpResponseRedirect('/')

    form = SignUpForm()
    category = Category.objects.all()
    context = {
        'category': category,
        'form':form,
    }
    return render(request, 'login.html', context)




def product_search(request):
    if request.method == 'POST': # check post
        form = SearchForm(request.POST)
        if form.is_valid():
            category = Category.objects.all()
            query = form.cleaned_data['query'] # get form input data
            product = Product.objects.filter(title__icontains=query)
            setting = Setting.objects.get(pk=1)



            context = {'product': product,
                       'category': category,

                       'setting': setting,

                       }
            return render(request, 'search_products.html', context)

    return HttpResponseRedirect('/')



def faq(request):
    category = Category.objects.all()
    faq = FAQ.objects.all()
    setting = Setting.objects.get(pk=1)


    context = {
        'faq': faq,
        'category':category,
        'setting':setting,

    }
    return render(request, 'faq.html', context)