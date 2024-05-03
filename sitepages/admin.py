from django.contrib import admin
from .models import Category, Vendor, Product, ProductImages, CartOrder, CartOrderItem, ProductReview, WishList, Address, Profile




class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages

    
    
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    list_display = ["user", "title", "product_image", "price", "category", "vendor", "featured", "product_status", "pro_id", ]

class CategoryAdmin(admin.ModelAdmin):
    list_display = ["title", "category_image"]

class VendorAdmin(admin.ModelAdmin):
    list_display = ["title", "vendor_image"]

class CartOrderAdmin(admin.ModelAdmin):
    list_editable = ["paid_status", "product_status"]
    list_display = ["user", "price", "paid_status", "order_date", "product_status"]

class CartOrderItemAdmin(admin.ModelAdmin):
    list_display = ["order", "invoice_no", "item", "image", "quantity", "price", "total"]

class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ["user", "product", "review", "rating"]

class WishListAdmin(admin.ModelAdmin):
    list_display = ["user", "product"]

class AddressAdmin(admin.ModelAdmin):
    list_editable = [ "address", "status"]
    list_display = ["user", "address", "status"]

class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "verified", "phone"]
    
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(CartOrder, CartOrderAdmin)
admin.site.register(CartOrderItem, CartOrderItemAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(WishList, WishListAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Profile, ProfileAdmin)


