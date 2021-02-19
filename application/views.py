from django.shortcuts import render, redirect
from .models import *
import json
from django.http import JsonResponse
from django.db.models import Q
from django.views import generic
from django.contrib.auth import login as log, get_user_model, authenticate
from django.contrib import messages
from .forms import *

User = get_user_model()


# Create your views here.

def count(request):
    if request.user.is_authenticated:
        cart_count = Cart.objects.select_related('user').filter(user=request.user,checkout=False)
        return JsonResponse({'count': cart_count.count()})
    else:
        return JsonResponse({'count': 0})


# signup page
def signup(request):
    if request.method == 'POST':

        filter_user = User.objects.filter(email=request.POST['email'])
        if filter_user:
            messages.warning(request, 'This email already taken!!')
            return redirect('signup')

        try:
            new_user = User.objects.create(username=request.POST['name'], email=request.POST['email'])
            new_user.set_password(request.POST['password'])
            messages.success(request, 'You have registered successfully!! Login now.')
            return redirect('login')
        except:
            messages.warning(request, 'This username is already taken!')
            return redirect('signup')

    return render(request, 'signup.html')


# login page
def login(request):
    if request.method == 'POST':
        logging_user = User.objects.get(email=request.POST['email'])
        logged = authenticate(username=logging_user, password=request.POST['password'])
        if logged:
            log(request, user=logged)
            return redirect('home')
        messages.warning(request, 'Invalid email or password')
        return redirect('login')
    return render(request, 'login.html')


# newsletter ajax call
def newsletter_subscribe(reqeust, **kwargs):
    data = json.loads(reqeust.body)
    newsletter_instance = Newsletter.objects.filter(email__iexact=data['email'])
    if newsletter_instance:
        return JsonResponse({'msg': 'You are already subscribed to our list. Thank you!'})

    Newsletter.objects.create(email=data['email'])
    return JsonResponse({'msg': 'You have subscribed successfully!'})


# home page
def index(request):
    items = Product.objects.prefetch_related('product_img').all()
    list1 = items[:3]
    list2 = items[3:6]
    list3 = items[6:9]
    ctx = {'list1': list1, 'list2': list2, 'list3': list3, 'count': json.loads(count(request).content)['count']}
    meta = MetaInfo.objects.first()
    ctx['name'] = meta.home_name
    ctx['description'] = meta.home_description
    ctx['title'] = meta.home_title
    return render(request, 'index.html', ctx)


# dual sims page
def dual_sims(request):
    ctx = {'count': json.loads(count(request).content)['count']}
    meta = MetaInfo.objects.first()
    ctx['name'] = meta.dual_sim_name
    ctx['description'] = meta.dual_sim_description
    ctx['title'] = meta.dual_sim_title
    return render(request, 'dual_sims.html')


# monthly deals page
def monthly_deals(request):
    ctx = {'count': json.loads(count(request).content)['count']}
    meta = MetaInfo.objects.first()
    ctx['name'] = meta.monthly_deals_name
    ctx['description'] = meta.monthly_deals_description
    ctx['title'] = meta.monthly_deals_title
    return render(request, 'monthly_deals.html')


# online shop page
def online_shop(request):
    ctx = {'list': Product.objects.prefetch_related('product_img', 'category').all(),
           'count': json.loads(count(request).content)['count']}
    meta = MetaInfo.objects.first()
    ctx['name'] = meta.online_shop_name
    ctx['description'] = meta.online_shop_description
    ctx['title'] = meta.online_shop_title
    return render(request, 'online_shop.html', ctx)


class DetailProduct(generic.DetailView):
    model = Product
    template_name = 'online_shop_detail.html'
    context_object_name = 'detail'

    def get_context_data(self, **kwargs):
        ctx = super(DetailProduct, self).get_context_data(**kwargs)
        product_instance = self.get_queryset()
        ctx['review'] = Rating.objects.select_related('product').filter(product=product_instance)
        ctx['count'] = json.loads(count(self.request).content)['count']
        return ctx


# wishlist page
def wishlist(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'You need to login to add or see the wishlist!')
        return redirect('login')
    ctx = {'list': WishList.objects.select_related('item', 'user').filter(user=request.user),
           'count': json.loads(count(request).content)['count']}
    return render(request, 'wishlist.html', ctx)


# AJAX request for wishlist addition
def add_wishlist(request, **kwargs):
    print(kwargs)

    # for anonymous users
    if not request.user.is_authenticated:
        messages.warning(request, 'You are not logged in. To add items to the wishlist, you must login first!')
        return redirect('login')

    # for logged in users
    product_instance = Product.objects.get(pk=kwargs['pk'])
    WishList.objects.create(item=product_instance, user=request.user)
    return redirect('wishlist')


# broadband deals page
def broadband_deals(request):
    ctx = {'count': json.loads(count(request).content)['count']}
    meta = MetaInfo.objects.first()
    ctx['name'] = meta.broadband_name
    ctx['description'] = meta.broadband_description
    ctx['title'] = meta.broadband_title
    return render(request, 'broadband_deals.html')


#  z-wifi page
def z_wifi(request):
    ctx = {'count': json.loads(count(request).content)['count']}
    meta = MetaInfo.objects.first()
    ctx['name'] = meta.wifi_name
    ctx['description'] = meta.wifi_description
    ctx['title'] = meta.wifi_title
    return render(request, 'z_wifi.html')


# search page
def search(request, **kwargs):
    query_item = Product.objects.prefetch_related('product_img', 'category').filter(
        Q(name__icontains=kwargs['name']) | Q(features__in=kwargs['name']) | Q(category__name=kwargs['name'])
    )
    return render(request, 'search.html', {'list': query_item, 'count': json.loads(count(request).content)['count']})


# add to cart
def add_to_cart(request, **kwargs):
    if not request.user.is_authenticated:
        return JsonResponse({'added': 'redirect'})
    product_instance = Product.objects.get(pk=kwargs['pk'])
    color = kwargs['color']

    # in-case no color is given
    if kwargs['color'] == 'none':
        for i in product_instance.product_img.all():
            color = i.color
            break

    # item being added already exist in cart so qty is increased
    prev_cart = Cart.objects.select_related('product', 'user').filter(product_id=product_instance.pk)
    if prev_cart:
        prev_cart[0].qty = prev_cart[0].qty + 1
        prev_cart[0].save()
        return JsonResponse({'added': 'updated'})

    # new item is added in cart
    new_cart = Cart.objects.create(product=product_instance, user=request.user, qty=kwargs['qty'],
                                   color=color)
    return JsonResponse({'added': 'added'})


# cart page
def cart_list(request):
    ctx = {'list': Cart.objects.select_related('product', 'user').filter(user=request.user,checkout=False),
           'count': json.loads(count(request).content)['count']}
    total_price = 0
    for item in ctx['list']:
        total_price += item.product.price * item.qty
    ctx['price'] = total_price
    return render(request, 'cart.html', ctx)


# updating the cart AJAX call
def update_cart(request, **kwargs):
    product_instance = Product.objects.get(pk=kwargs['pk'])
    prev_cart = Cart.objects.select_related('product', 'user').filter(product_id=product_instance.pk)
    if prev_cart:
        prev_cart[0].qty = kwargs['qty']
        prev_cart[0].save()
        return JsonResponse({'added': 'updated'})


# deleting item from cart ajax call
def delete_cart(request, **kwargs):
    product_instance = Product.objects.get(pk=kwargs['pk'])
    prev_cart = Cart.objects.select_related('product', 'user').get(product_id=product_instance.pk)
    prev_cart.delete()
    return JsonResponse({'deleted': 'deleted'})


def checkout(request):
    ctx = {}
    form = CheckoutForm(request.POST or None)
    ctx['form'] = form
    if request.method == 'POST':
        if form.is_valid():
            checkout_user = form.save(commit=True)

            carts = Cart.objects.select_related('product','user').filter(user=request.user)
            complete_order = CompleteOrder.objects.create(
                user=checkout_user,
            )
            complete_order.carts.add(*carts)
            complete_order.save()
            carts.update(checkout=True)
            return redirect('thank-you')

    return render(request, 'checkout.html', ctx)


def thank_you(request):
    return render(request, 'thank_you.html')
