from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth import get_user_model

# Create your models here.


User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Feature(models.Model):
    name = models.CharField(max_length=128)
    feature_name = models.TextField()

    def __str__(self):
        return f'{self.name} is {self.feature_name}'


class ProductImage(models.Model):
    img = models.ImageField(upload_to='mobile/')
    color = models.CharField(max_length=100)

    def get_photo_url(self):
        if self.img and hasattr(self.img, 'url'):
            return self.img.url


class Product(models.Model):
    name = models.CharField(max_length=128)
    features = RichTextUploadingField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    stock = models.IntegerField()
    product_img = models.ManyToManyField(ProductImage)
    dual_sim = models.BooleanField(default=False)
    price = models.BigIntegerField()

    def __str__(self):
        return self.name


class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    color = models.CharField(max_length=255, blank=True, null=True)
    checkout = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.product.name} with this qty {self.qty}'


class UserInfo(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email_address = models.EmailField()
    phone = models.BigIntegerField()
    post_code = models.IntegerField()
    door_number = models.CharField(max_length=255)
    street_name = models.CharField(max_length=255)
    country = models.CharField(max_length=255)

    def __str__(self):
        return self.first_name


class CompleteOrder(models.Model):
    carts = models.ManyToManyField(Cart)
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} order'


class Blog(models.Model):
    title = models.CharField(max_length=255)
    text = RichTextUploadingField()
    date = models.DateField(auto_now=True)
    title_img = models.ImageField(upload_to='blog/')

    def __str__(self):
        return self.title

    def get_photo_url(self):
        if self.title_img and hasattr(self.title_img, 'url'):
            return self.title_img.url


class UserRedirect(models.Model):
    name = models.CharField(max_length=128, unique=False)
    IP = models.BigIntegerField()

    def __str__(self):
        return f'{self.name} with IP:{self.IP}'


class Rating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()

    def __str__(self):
        return f'{self.user.username} comment'


class Newsletter(models.Model):
    email = models.EmailField()

    def __str__(self):
        return self.email


class MetaInfo(models.Model):
    home_title = models.CharField(max_length=255)
    home_name = models.CharField(max_length=255)
    home_description = models.TextField()

    dual_sim_title = models.CharField(max_length=255)
    dual_sim_name = models.CharField(max_length=255)
    dual_sim_description = models.TextField()

    monthly_deals_title = models.CharField(max_length=255)
    monthly_deals_name = models.CharField(max_length=255)
    monthly_deals_description = models.TextField()

    online_shop_title = models.CharField(max_length=255)
    online_shop_name = models.CharField(max_length=255)
    online_shop_description = models.TextField()

    wifi_title = models.CharField(max_length=255)
    wifi_name = models.CharField(max_length=255)
    wifi_description = models.TextField()

    broadband_title = models.CharField(max_length=255)
    broadband_name = models.CharField(max_length=255)
    broadband_description = models.TextField()

    contact_title = models.CharField(max_length=255)
    contact_name = models.CharField(max_length=255)
    contact_description = models.TextField()

    def __str__(self):
        return 'Meta info'


class WishList(models.Model):
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + ' wishlist'
