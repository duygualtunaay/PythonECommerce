from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from home.models import Setting
from order.models import OrderProduct, Order
from product.models import Category, Comment, Product, ProductForm
from user.forms import UserUpdateForm, ProfileUpdateForm
from user.models import UserProfile


def index(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user.id)
    context={
        'setting':setting,
        'category':category,
        'profile':profile,

             }
    return render(request,'user_profile.html',context)


@login_required(login_url='/login') # Check login
def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user) # request.user is user  data
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your account has been updated!')
            return HttpResponseRedirect('/user')
    else:
        category = Category.objects.all()
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile) #"userprofile" model -> OneToOneField relatinon with user
        context = {
            'category': category,
            'user_form': user_form,
            'profile_form': profile_form
        }
        return render(request, 'user_update.html', context)

@login_required(login_url='/login') # Check login
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return HttpResponseRedirect('/user')
        else:
            messages.error(request, 'Please correct the error below.<br>'+ str(form.errors))
            return HttpResponseRedirect('/user/password')
    else:
        category = Category.objects.all()
        form = PasswordChangeForm(request.user)
        return render(request, 'change_password.html', {'form': form,'category': category
                       })


def user_comments(request):
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    current_user = request.user
    comments = Comment.objects.filter(user_id=current_user.id)
    context = {
        'category': category,
        'comments': comments,
        'setting':setting,
    }
    return render(request, 'user_comments.html', context)

@login_required(login_url='/login') # Check login
def user_deletecomment(request,id):
    current_user = request.user
    Comment.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, 'Comment deleted..')
    return HttpResponseRedirect('/user/comments')


@login_required(login_url='/login') # Check login
def user_orders(request):
    #category = Category.objects.all()
    current_user = request.user
    orders=Order.objects.filter(user_id=current_user.id)
    context = {#'category': category,
               'orders': orders,
               }
    return render(request, 'user_orders.html', context)

@login_required(login_url='/login') # Check login
def user_orderdetail(request,id):
    category = Category.objects.all()
    current_user = request.user
    order = Order.objects.get(user_id=current_user.id, id=id)
    orderitems = OrderProduct.objects.filter(order_id=id)
    context = {
        'category': category,
        'order': order,
        'orderitems': orderitems,
    }
    return render(request, 'user_order_detail.html', context)

@login_required(login_url='/login') # Check login
def user_order_product(request):
    category = Category.objects.all()
    current_user = request.user
    order_product = OrderProduct.objects.filter(user_id=current_user.id).order_by('-id')
    context = {'category': category,
               'order_product': order_product,
               }
    return render(request, 'user_order_products.html', context)

@login_required(login_url='/login') # Check login
def user_order_product_detail(request,id,oid):
    category = Category.objects.all()
    current_user = request.user
    order = Order.objects.get(user_id=current_user.id, id=oid)
    orderitems = OrderProduct.objects.filter(id=id,user_id=current_user.id)
    context = {
        'category': category,
        'order': order,
        'orderitems': orderitems,
    }
    return render(request, 'user_order_detail.html', context)


@login_required(login_url="/login")
def addproduct(request):

   if request.method == 'POST':  # check post
      form = ProductForm(request.POST, request.FILES)
      if form.is_valid():
         current_user=request.user
         data = Product()  # create relation with model
         data.user_id=current_user.id
         data.title = form.cleaned_data['title']
         data.keywords = form.cleaned_data['keywords']
         data.description = form.cleaned_data['description']
         data.image = form.cleaned_data['image']
         data.slug = form.cleaned_data['slug']
         data.detail = form.cleaned_data['detail']
         data.status = 'False'
         data.save()  # save data to table
         messages.success(request, 'Ürün eklenmiştir. Yönetici Onayı beklemektedir!')
         return HttpResponseRedirect('/user/product')
      else:
         messages.success(request, 'product form error :'+ str(form.errors))
         return HttpResponseRedirect('/user/addproduct')


   else:
       category = Category.objects.all()
       setting = Setting.objects.get(pk=1)
       form = ProductForm()
       context = {
           'category':category,
           'form':form,
           'setting':setting,
       }
       return render(request, 'user_addproduct.html', context)

@login_required(login_url="/login")
def product(request):
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    current_user = request.user
    product = Product.objects.filter(user_id=current_user.id)

    context = {
        'category': category,
        'product': product,
        'setting': setting,
    }
    return render(request, 'user_product.html', context)

@login_required(login_url="/login")
def productdelete(request,id):
    current_user = request.user
    Product.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request,'product Deleted')
    return HttpResponseRedirect('/user/product')


def productedit(request,id):
    product = Product.objects.get(id=id)
    setting = Setting.objects.get(pk=1)
    if request.method == 'POST':  # check post
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ürününüz eklenmiştir. Yönetici Onayı beklemektedir!')
            return HttpResponseRedirect('/user/product')
        else:
            messages.success(request, 'product form error :' + str(form.errors))
            return HttpResponseRedirect('/user/productedit/'+str(id))


    else:
        category = Category.objects.all()
        form = ProductForm(instance=product)
        context = {
            'category': category,
            'form': form,
            'setting': setting,
        }
        return render(request, 'user_productedit.html', context)



