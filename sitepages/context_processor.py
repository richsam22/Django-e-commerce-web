from .models import Category, Vendor, Product, ProductImages, CartOrder, CartOrderItem, ProductReview, WishList, Address
from django.contrib import messages

def default(request):
    categories = Category.objects.all()
    try:
        address = Address.objects.get(user=request.user)
    except:
        address = None
        
    try:
        wishlist = WishList.objects.filter(user=request.user)
    except:
        messages.warning(request, "You need to Login before accessing wishlist")
        wishlist = 0
    
    return {
        'categories': categories,
        'address': address,
        'wishlist': wishlist
    }