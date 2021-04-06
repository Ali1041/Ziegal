from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView
name = 'application'

urlpatterns = [
    # signup url
    path('signup/',signup,name='signup'),

    # login url
    path('login/',login,name='login'),

    # logout url
    path('logout/',LogoutView.as_view(),name='logout'),

    # newsletter subscribe url
    path('newsletter/subscribe/',newsletter_subscribe,name='newsletter'),

    # home url
    path('',index,name='home'),

    # dual sims url
    path('dual-sims/',dual_sims,name='dual-sims'),

    # monthly deals
    path('monthly-deals/',monthly_deals,name='monthly-deals'),

    # wishlist url
    path('wishlist/',wishlist,name='wishlist'),
    path('wishlist-add/<int:pk>/',add_wishlist,name='wishlist-add'),

    # online shop url
    path('online-shop/',online_shop,name='online-shop'),
    path('online-shop<slug:slug>/<int:pk>/',DetailProduct.as_view(),name='detail-online-shop'),

    # z_wifi url
    path('z-wifi/',z_wifi,name='z-wifi'),

    # broadband deals url
    path('broadband-deals/',broadband_deals,name='broadband_deals'),

    # cart urls
    path('add-to-cart/<int:pk>/<int:qty>/<str:color>/',add_to_cart,name='add-to-cart'),
    path('my-cart/',cart_list,name='cart'),
    path('update-cart/<int:pk>/<int:qty>/',update_cart,name='update-cart'),
    path('delete-cart/<int:pk>/',delete_cart,name='delete-cart'),
    path('count/',count,name='count'),


    # checkout cart
    path('checkout/',checkout,name='checkout'),

    # misallaneous
    path('search/<str:name>/',search,name='search'),
    path('thank-you/',thank_you,name='thank-you'),
    path('mission-statement/',mission_statement,name='mission-statement'),
    path('privacy-policy/',privacy_policy,name='privacy-policy'),
    path('terms-and-condition/',terms_condition,name='terms-condition'),


    # blog urls
    path('blog-list/',blog_list,name='blog-list'),
    path('blog-detail/<slug:slug>/<int:pk>/',blog_detail,name='blog-detail'),
]