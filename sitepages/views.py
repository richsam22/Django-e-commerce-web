from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.http import JsonResponse
from urllib import request
from django.contrib import messages
from taggit.models import Tag
from django.db.models import Count, Avg
from .models import Category, Vendor, Product, ProductImages, CartOrder, CartOrderItem, ProductReview, WishList, Address, Profile
from .forms import ProductReviewForm, ProfileForm

from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
from django.core import serializers





# Create your views here.

def Home(request):
    # products = Product.objects.all().order_by("-date")
    products = Product.objects.filter(product_status="published", featured=True)
    
    context = {
        "products": products
    }
    
    return render(request, "home.html", context)

def product_list(request):
    products = Product.objects.filter(product_status="published").order_by("-date")
    
    context = {
        "products": products
    }
    
    return render(request, "product_list.html", context)

def category(request):
    categories = Category.objects.all()
    
    context = {
        "categories": categories
    }
    
    return render(request, "category.html", context)

def category_product(request, cat_id):
    category = Category.objects.get(cat_id=cat_id)
    products = Product.objects.filter(product_status="published", category=category)
    
    context = {
        "category": category,
        "products": products,
    }
    
    return render(request, "category_product.html", context)

def vendor_list(request):
    vendor = Vendor.objects.all()
    
    context = {
        "vendor": vendor
    }
    
    return render(request, "vendor.html", context)

def vendor_detail(request, ven_id):
    vendor = Vendor.objects.get(ven_id=ven_id)
    products = Product.objects.filter(product_status="published", vendor=vendor)
    
    context = {
        "vendor": vendor,
        "products": products,
    }
    
    return render(request, "vendor_detail.html", context)

def product_detail(request, pro_id):
    product = Product.objects.get(pro_id=pro_id)
    products = Product.objects.filter(category=product.category).exclude(pro_id=pro_id)
    
    # getting all review related to product
    review = ProductReview.objects.filter(product=product).order_by("-date")
    
    # getting average review 
    average_rating = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))
    
    # product review form
    review_form = ProductReviewForm()
    
    pro_images = product.pro_images.all()
    
    context = {
        "product": product,
        "review_form": review_form,
        "pro_images": pro_images,
        "products": products,
        "review": review,
        "average_rating": average_rating,
        
    }
    
    return render(request, "product_detail.html", context)

def tag(request, tag_slug=None):
    products = Product.objects.filter(product_status="published").order_by("-id")
    
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        products = products.filter(tags__in=[tag])
        
    context = {
        "products": products,
        "tag": tag,
    }
    
    return render(request, "tag.html", context)
    

def reviewform(request, pro_id):
    product = Product.objects.get(pro_id=pro_id)
    user = request.user
    
    review = ProductReview.objects.create(
        user=user,
        product=product,
        review = request.POST['review'],
        rating = request.POST['rating'],
    )
    
    context = {
        "user": user.username,
        "review": request.POST['review'],
        "rating": request.POST['rating'],
    }
    
    average_review = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))
    
    
    return JsonResponse(
       {
        "bool": True,
        "context": context,
        "average_review": average_review
       }
    )


def search(request):
    query = request.GET.get("q")
    
    products = Product.objects.filter(title__icontains=query, description__icontains=query).order_by("-date")
    
    context = {
        "products": products,
        "query": query,
    }
    
    return render(request, "search.html", context)
    
    
def add_to_cart(request):
    cart_product = {}
    
    cart_product[str(request.GET['id'])] = {
        'qty': request.GET['qty'],
        'title': request.GET['title'],
        'price': request.GET['price'],
        'image': request.GET['image'],
        'pid': request.GET['pid'],
        
    }
    
    if 'cart_data_obj' in request.session:
        if str(request.GET['id']) in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = int(cart_product[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)
            request.session['cart_data_obj'] = cart_data
        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data
            
    else:
        request.session['cart_data_obj'] = cart_product
    return JsonResponse({"data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj'])})


def cart_view(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            
            # Split the price string into a list of prices
            prices = item['price'].split()
            price_list = [float(price) for price in prices]
            # Update the total amount
            cart_total_amount += int(item['qty']) * sum(price_list)
            
            
        return render(request, "cart.html", {"cart_data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']),'cart_total_amount':cart_total_amount})
    else:
        messages.warning(request, "Your Cart is Empty")
        return redirect("/")
        
        
def delete_cart(request):
    product_id =str(request.GET['id'])
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            del request.session['cart_data_obj'][product_id]
    
    
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            request.session['cart_data_obj'] = cart_data  
            
            # Split the price string into a list of prices
            prices = item['price'].split()
            price_list = [float(price) for price in prices]
            # Update the total amount
            cart_total_amount += int(item['qty']) * sum(price_list)
    
    
    context = render_to_string('cart_list.html', {"cart_data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']),'cart_total_amount':cart_total_amount})
    
    return JsonResponse({"data": context, 'totalcartitems': len(request.session['cart_data_obj'])})
            
def update_cart(request):
    product_id =str(request.GET['id'])
    product_qty =str(request.GET['qty'])
    
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = product_qty
            request.session['cart_data_obj'] = cart_data
    
    
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            request.session['cart_data_obj'] = cart_data  
            
            # Split the price string into a list of prices
            prices = item['price'].split()
            price_list = [float(price) for price in prices]
            # Update the total amount
            cart_total_amount += int(item['qty']) * sum(price_list)
    
    
    context = render_to_string('cart_list.html', {"cart_data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']),'cart_total_amount':cart_total_amount})
    
    return JsonResponse({"data": context, 'totalcartitems': len(request.session['cart_data_obj'])})
            
@login_required
def checkout(request):
    
    cart_total_amount = 0
    total_amount = 0
    
    # Checking if cart_data_obj session exist
    if 'cart_data_obj' in request.session:
        
        # Getting total amount for paypal amount
        for p_id, item in request.session['cart_data_obj'].items():
            prices = item['price'].split()
            price_list = [float(price) for price in prices]
            total_amount += int(item['qty']) * sum(price_list)
         
        # Creating order object   
        order = CartOrder.objects.create(
            user=request.user,
            price=total_amount,
        )
        
        # Getting total amount for the cart
        for p_id, item in request.session['cart_data_obj'].items():
            prices = item['price'].split()
            price_list = [float(price) for price in prices]
            cart_total_amount += int(item['qty']) * sum(price_list)
            
            cart_order_item = CartOrderItem.objects.create(
                order=order,
                invoice_no="INVOICE_NO" + str(order.id), # INVOICE_NO-5
                item=item['title'],
                image=item['image'],
                quantity=item['qty'],
                price=item['price'],
                total=float(item['qty']) * float(item['price']),
            )
        
        
    
    host = request.get_host()
    paypal_dict = {
        'business': settings.PAYPAL_RECIEVER_EMAIL,
        'amount': cart_total_amount,
        'item_name': 'Order-Item-No-' + str(order.id),
        'invoice': 'INVOICE_NO-' + str(order.id),
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host, reverse('sitepages:paypal-ipn')),
        'return_url': 'http://{}{}'.format(host, reverse('sitepages:payment_completed')),
        'cancel_url': 'http://{}{}'.format(host, reverse('sitepages:payment_failed')),
        }
    
    paypal_payment_button = PayPalPaymentsForm(initial=paypal_dict)
    
    # cart_total_amount = 0
    # if 'cart_data_obj' in request.session:
    #     for p_id, item in request.session['cart_data_obj'].items():
             
    #         prices = item['price'].split()
    #         price_list = [float(price) for price in prices]
    #         cart_total_amount += int(item['qty']) * sum(price_list)
    
    try:
        active_address = Address.objects.get(user=request.user, status=True)
    except:
        messages.warning(request, "You can only Activate one Address")
        active_address = None
    
    return render(request, "checkout.html", {"cart_data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']),'cart_total_amount':cart_total_amount, 'paypal_payment_button':paypal_payment_button, 'active_address': active_address})

@login_required
def payment_complete_view(request):
    
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
             
            
            # Split the price string into a list of prices
            prices = item['price'].split()
            price_list = [float(price) for price in prices]
            # Update the total amount
            cart_total_amount += int(item['qty']) * sum(price_list)
    return render(request, 'payment-complete.html', {"cart_data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']),'cart_total_amount':cart_total_amount,})

@login_required
def payment_failed_view(request):
    return render(request, 'payment-failed.html')

@login_required
def dashboard(request):
    orders = CartOrder.objects.filter(user=request.user).order_by("-id")
    address = Address.objects.filter(user=request.user)
    
    profile = Profile.objects.get(user=request.user)
    
    if request.method == "POST":
        address = request.POST.get("address")
        mobile = request.POST.get("mobile")
        
        new_address = Address.objects.create(
            user=request.user,
            address=address,
            mobile=mobile,
        )
        messages.success(request, "Address Added Successfully")
        return redirect("sitepages:dashboard")
    
    context = {
        'orders': orders,
        'address': address,
        'profile': profile
    }
    return render(request, 'dashboard.html', context)

def order_detail(request, id):
    order = CartOrder.objects.get(user=request.user, id=id)
    products = CartOrderItem.objects.filter(order=order)
    context = {
        'products': products
    }
    return render(request, 'order_detail.html', context)

def default_address(request):
    id = request.GET["id"]
    Address.objects.update(status=False)
    Address.objects.filter(id=id).update(status=True)
    
    return JsonResponse({"boolean": True})

@login_required
def wishlist(request):
    wishlist = WishList.objects.all()
    
    context = {
        "wishlist": wishlist
    }
    return render(request, 'wishlist.html', context)

def add_to_wishlist(request):
    product_id = request.GET["id"]
    product = Product.objects.get(id=product_id)
    
    context = {}
    
    wishlist_count = WishList.objects.filter(product=product, user=request.user).count()
    print(wishlist_count)
    
    if wishlist_count > 0:
        context = {
            "bool": True
        }
    else:
        new_wishlist = WishList.objects.create(
            user=request.user,
            product=product,
        )
        context = {
            "bool": True
        }
        
    return JsonResponse(context)
    
    
def remove_wishlist(request):
    product_id = request.GET["id"]
    wishlist = WishList.objects.filter(user=request.user)
    
    wishlist_d = WishList.objects.get(id=product_id)
    delete_product = wishlist_d.delete()
    
    context = {
        "bool": True,
        "wishlist": wishlist
    }
    wishlist_json = serializers.serialize("json", wishlist)
    data = render_to_string("wishlist_delete.html", context)
    return JsonResponse({"data": data, "wishlist": wishlist_json})

def profile_edit(request):
    profile_image = Profile.objects.get(user=request.user)
    
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile_image)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.save()
            messages.success(request, "Profile Updated Successfully")
            return redirect("/dashboard")
    else:
        form = ProfileForm(instance=profile_image)
            
    context = {
        "form": form,
        "profile_image": profile_image,
    }
    return render(request, "profile.html", context)



def about(request):
    return render(request, "about.html")

def custom_404(request):
    return render(request, "404.html")




