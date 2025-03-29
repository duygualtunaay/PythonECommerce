from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='user_index'),
    path('update/', views.user_update, name='user_update'),
    path('password/', views.change_password, name='change_password'),
    path('comments/', views.user_comments, name='user_comments'),
    path('deletecomment/<int:id>', views.user_deletecomment, name='user_deletecomment'),
    path('orders/', views.user_orders, name='user_orders'),
    path('orders_product/', views.user_order_product, name='user_order_product'),
    path('orderdetail/<int:id>', views.user_orderdetail, name='user_orderdetail'),
    path('order_product_detail/<int:id>/<int:oid>', views.user_order_product_detail, name='user_order_product_detail'),
    path('product/', views.product, name='product'),
    path('addproduct/', views.addproduct, name='addproduct'),
    path('productedit/<int:id>', views.productedit, name='productedit'),
    path('productdelete/<int:id>', views.productdelete, name='productdelete'),
]