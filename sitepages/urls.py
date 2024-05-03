from django.urls import path, include
from django.conf.urls import handler404
from .views import *



app_name = "sitepages"

urlpatterns = [
    path('', Home, name='home'),
    path('product/', product_list, name='productlist'),
    path('product/<pro_id>/', product_detail, name='product_det'),
    
    ######### Category #####
      
    path('category/', category, name='category'),
    path('category/<cat_id>/', category_product, name='categorycid'),
    
    ######### Vendor #####
    
    path('vendor/', vendor_list, name='vendor'),
    path('vendor/<ven_id>/', vendor_detail, name='vendor_det'),
    
    ######### Tags #####
    path('product/tag/<slug:tag_slug>/', tag, name='tag'),
    
    ######### Add review #####
    path('review/<str:pro_id>/', reviewform, name='review'),
    
    ######### Search #####
    path('search/', search, name='search'),
    
    ######### Add to Cart #####
    path('add_to_cart/', add_to_cart, name='add_to_cart'),
    path('cart/', cart_view, name='cart'),
    
    ######### Delete item from Cart #####
    path('delete_from_cart/', delete_cart, name='delete_from_cart'),
    
    ######### Update Cart #####
    path('update_cart/', update_cart, name='update_cart'),
    
    ######### Checkout #####
    path('checkout/', checkout, name='checkout'),
    
    ######### Paypal #####
    path('paypal/', include('paypal.standard.ipn.urls')),
    
    ######### Payment successful #####
    path('payment_completed/', payment_complete_view, name='payment_completed'),
    
    ######### Payment failed #####
    path('payment_failed/', payment_failed_view, name='payment_failed'),
    
    ######### Dashboard #####
    path('dashboard/', dashboard, name='dashboard'),
    
    ######### Dashboard Order #####
    path('dashboard/order/<int:id>', order_detail, name='order'),
    
    ######### Making Address default  #####
    path('default-address/', default_address, name='default-address'),
    
    ######### Wishlist  #####
    path('wishlist/', wishlist, name='wishlist'),
    
    ######### Adding to Wishlist  #####
    path('add-to-wishlist/', add_to_wishlist, name='add-to-wishlist'),
    
    ######### Removing from Wishlist  #####
    path('remove-from-wishlist/', remove_wishlist, name='remove-from-wishlist'),
    
    ######### Editing profile  #####
    path('profile-edit/', profile_edit, name='profile-edit'),
    
    ######### About Page  #####
    path('about/', about, name='about'),
    
    ######### 404 Page  #####
    path('404/', custom_404, name='404'),
]

    

