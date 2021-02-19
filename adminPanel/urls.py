from django.urls import path
from .views import *

app_name = 'adminPanel'
urlpatterns = [
    path('admin-home/',index,name='admin-home'),

    # products url
    path('admin-mobiles/<str:name>/',MobileListView.as_view(),name='admin-mobiles'),
    path('admin-add-mobiles/<str:name>/',phone_add,name='add-mobiles'),
    path('admin-mobile-detail/<str:name>/<int:pk>/',MobileDetailView.as_view(),name='mobile-detail'),
    path('admin-edit/<str:name>/<int:pk>/',phone_add,name='edit-product'),

    # blog url
    path('admin-blog/',BlogList.as_view(),name='blog-list'),
    path('admin-blog-detail/<int:pk>/',BlogDetail.as_view(),name='blog-detail'),
    path('admin-add-blog/',add_blog,name='blog-add'),
    path('admin-add-blog/<str:name>/<int:pk>/',add_blog,name='blog-edit'),

    # redirected user
    path('admin-redirect-user-info/',UserRedirect.as_view(),name='redirected_user'),


    # complete order
    path('admin-complete-orders/',CompleteOrderList.as_view(),name='complete-order'),
    path('admin-comlpete-order-detail/<int:pk>/',CompleteOrderDetail.as_view(),name='complete-order-detail'),


    # meta info urls
    path('meta-info/',meta_info,name='meta-info'),
]