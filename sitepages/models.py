from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.safestring import mark_safe
from colorfield.fields import ColorField
from authentication.models import User
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models.signals import post_save



# Create your models here.


STATUS_CHOICE = (
    ("processing", "Processing"),
    ("shipped", "Shipped"),
    ("delivered", "Delivered"),
)

STATUS = (
    ("draft", "Draft"),
    ("disabled", "Disabled"),
    ("rejected", "Rejected"),
    ("in review", "In Review"),
    ("published", "Published"),
)
RATING = (
    ("1", "★☆☆☆☆"),
    ("2", "★★☆☆☆"),
    ("3", "★★★☆☆"),
    ("4", "★★★★☆"),
    ("5", "★★★★★"),
)


def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Category(models.Model):
    cat_id = ShortUUIDField(unique=True, length=10, max_length=20, prefix="cat", alphabet="abcdefgh123456")
    
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category')
    
    class Meta:
        verbose_name_plural = "Categories"
        
    def category_image(self):
        return mark_safe('<img src="{}" width="50" height="50" />'.format(self.image.url))
    
    def __str__(self):
        return self.title
    
class Tags(models.Model):
    pass
    
    
class Vendor(models.Model):
    ven_id = ShortUUIDField(unique=True, length=10, max_length=20, prefix="ven", alphabet="abcdefgh123456")
    
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to=user_directory_path, default="vendor")
    cover_image = models.ImageField(upload_to=user_directory_path, default="vendor")
    # description = models.TextField(null=True, blank=True)
    description = RichTextUploadingField(null=True, blank=True, default="I am an Amazing Vendor")
    
    
    address = models.CharField(max_length=100, default="")
    contact = models.CharField(max_length=100, default="+234 (223) 545 ")
    chat_resp_time = models.CharField(max_length=100, default="100")
    shipping_time = models.CharField(max_length=100, default="100")
    days_return = models.CharField(max_length=100, default="100")
    authentic_rating = models.CharField(max_length=100, default="100")
    warranty_period = models.CharField(max_length=100, default="100")
    
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Vendor"
        
    def vendor_image(self):
        return mark_safe('<img src="{}" width="50" height="50" />'.format(self.image.url))
    
    def __str__(self):
        return self.title
    
    
    
class Product(models.Model):
    pro_id = ShortUUIDField(unique=True, length=10, max_length=20, prefix="pro", alphabet="abcdefgh123456")
    
    title = models.CharField(max_length=100)
    old_price = models.DecimalField(max_digits=999999999999, decimal_places=2, default="50.00")
    price = models.DecimalField(max_digits=999999999999, decimal_places=2, default="53.00")
    image = models.ImageField(upload_to='product-image',)
    description = RichTextUploadingField(null=True, blank=True)
    # description = models.TextField(null=True, blank=True)
    # color = ColorField()
    
    
    
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="category")
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, related_name= "vendor")
    product_status = models.CharField(choices=STATUS, max_length=10, default="In_review")
    
    tags = TaggableManager(blank=True)
    
    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=True)
    digital = models.BooleanField(default=True)
    
    sku = ShortUUIDField(unique=True, length=4, max_length=10, prefix="sku", alphabet="1234567890")
    
    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Products"
        
    def product_image(self):
        return mark_safe('<img src="{}" width="50" height="50" />'.format(self.image.url))
        
    
    def __str__(self):
        return self.title
    
    def get_percentage(self):
        new_price = (self.price / self.old_price) * 100
        return new_price
    

class ProductImages(models.Model):
    images = models.ImageField(upload_to="product-images")
    product = models.ForeignKey(Product, related_name="pro_images",on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)
    
    
    class Meta:
        verbose_name_plural = "Product Images"
        
        

#                       Cart ,Order, Oderitems 
#                       Cart ,Order, Oderitems 
        
    
class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=999999999999, decimal_places=2, default="53.00")
    paid_status = models.BooleanField(default=True)
    order_date = models.DateTimeField(auto_now_add=True)
    product_status = models.CharField(choices=STATUS_CHOICE, max_length=30, default="processing")
    
    class Meta:
        verbose_name_plural = "Cart Orders"


class CartOrderItem(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=200)
    product_status = models.CharField(max_length=200)
    item = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=999999999999, decimal_places=2, default="53.00")
    total = models.DecimalField(max_digits=999999999999, decimal_places=2, default="53.00")
    
    class Meta:
        verbose_name_plural = "Cart Order Items"
        
    def category_image(self):
        return mark_safe('<img src="{}" width="50" height="50" />'.format(self.image.url))
        
    def order_img(self):
        return mark_safe('<img src="{}" width="50" height="50" />'.format(self.image))



#                       Product review, Wishlist, address
#                       Product review, Wishlist, address


class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name="review")
    review = models.TextField()
    rating = models.CharField(choices=RATING, max_length=20, default=None)
    date = models.DateTimeField(auto_now_add=True)
    
    
    class Meta:
        verbose_name_plural = "Product Reviews"
        
    
    def __str__(self):
        return self.product.title
    
    def get_rating(self):
        return self.rating
    
                    
class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=999999999999, decimal_places=2, default="53.00")
    date = models.DateTimeField(auto_now_add=True)
    
    
    class Meta:
        verbose_name_plural = "Wishlist"
     
    

        
    
    
    

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=100, null=True)
    mobile = models.CharField(max_length=100, null=True)
    status = models.BooleanField(default=False)
    
    
    class Meta:
        verbose_name_plural = "Address"
    
                    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="Image")
    full_name = models.CharField(max_length=100, null=True, blank=True)
    bio = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=20)
    verified = models.BooleanField(default=True)
    
    def __str__(self):
        return self.user.username
    
    
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    
post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)

