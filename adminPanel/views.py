from django.shortcuts import render, redirect
from application.models import *
from .forms import *
from django.views import generic


# Create your views here.

# Admin home page
def index(request):
    return render(request, 'adminPanel/admin_home.html')


# table view of mobile list
class MobileListView(generic.ListView):
    model = Product
    context_object_name = 'list'
    template_name = 'adminPanel/admin_phone_list.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx['category'] = self.kwargs['name']
        return ctx

    def get_queryset(self):
        qs = Product.objects.select_related('category').filter(category__name=self.kwargs['name'])
        return qs


class MobileDetailView(generic.DetailView):
    model = Product
    context_object_name = 'detail'
    template_name = 'adminPanel/admin_phone_detail.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['category'] = self.kwargs['name']
        return ctx


# Add phone form
def phone_add(request, **kwargs):
    form = PhoneForm(request.POST or None, request.FILES or None)
    ctx = {}
    if request.method == 'POST':
        imgs = request.FILES.getlist('image')
        colors = request.POST.getlist('color')
        imgs_model = []

        if len(kwargs) > 1:
            product = Product.objects.select_related('category').get(pk=kwargs['pk'])
            for i in product.product_img.all():
                spliting = i.get_photo_url().split('/')
                print(spliting)
                imgs.append(f'{spliting[-2]}/{spliting[-1]}')
            print(imgs)
            product.product_img.clear()
            for item,color in zip(imgs,colors):
                print(item)
                product_image = ProductImage.objects.create(color=color, img=item)
                imgs_model.append(product_image.pk)
            category = Category.objects.get(name=kwargs['name'])
            product.category = category
            product.product_img.add(*imgs_model)
            product.name = request.POST['name']
            product.stock = request.POST['stock']
            product.features = request.POST['features']

            product.save()
            return redirect('adminPanel:mobile-detail',kwargs['name'],kwargs['pk'])


        else:
            for item,color in zip(imgs,colors):
                product_image = ProductImage.objects.create(color=color, img=item)
                imgs_model.append(product_image.pk)

            category = Category.objects.get(pk=int(request.POST['category']))
            sim = False
            try:
                if request.POST['dual_sim'] == 'on':
                    sim = True
            except:
                pass
            product = Product.objects.create(
                name=request.POST['name'],
                features=request.POST['features'],
                stock=request.POST['stock'],
                category=category,
                price=request.POST['price'],
                dual_sim=sim
            )

            product.product_img.add(*imgs_model)
            return redirect('adminPanel:admin-mobiles',kwargs['name'])

    # edit product get request
    if len(kwargs)>1:
        product_instance = Product.objects.get(pk=kwargs['pk'])
        form = PhoneForm(instance=product_instance)
        ctx['product'] = product_instance

    ctx['form'] = form
    ctx['category'] = kwargs['name']
    return render(request, 'adminPanel/admin_phone_add.html', ctx)


# blog list
class BlogList(generic.ListView):
    model = Blog
    template_name = 'adminPanel/admin_blog_list.html'
    context_object_name = 'list'


# blog detail
class BlogDetail(generic.DetailView):
    model = Blog
    template_name = 'adminPanel/admin_blog_detail.html'
    context_object_name = 'detail'


# add blog
def add_blog(request, **kwargs):
    ctx = {}
    form = BlogForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':

        # editing a existing blog
        if kwargs:
            blog_instance = Blog.objects.get(pk=kwargs['pk'])
            img = blog_instance.title_img

            # in-case picture is changed
            if request.FILES:
                img = request.FILES.get('title_img')

            blog_instance.title_img = img
            blog_instance.title = request.POST['title']
            blog_instance.text = request.POST['text']
            blog_instance.save()

            return redirect('adminPanel:blog-detail', blog_instance.pk)


        # adding a new blog
        else:
            if form.is_valid():
                form.save(commit=True)
                return redirect('adminPanel:blog-list')

    # get request for edit
    if kwargs:
        blog_instance = Blog.objects.get(pk=kwargs['pk'])
        form = BlogForm(instance=blog_instance)
        ctx['blog'] = blog_instance

    ctx['form'] = form

    return render(request, 'adminPanel/admin_blog_add.html', ctx)


# redirected users
class UserRedirect(generic.ListView):
    model = UserRedirect
    template_name = 'adminPanel/admin_user_info.html'
    context_object_name = 'list'


# Complete order list
class CompleteOrderList(generic.ListView):
    model = CompleteOrder
    template_name = 'adminPanel/admin_complete_orders_list.html'
    context_object_name = 'list'


# Complete order detail
class CompleteOrderDetail(generic.DetailView):
    model = CompleteOrder
    template_name = 'adminPanel/admin_complete_order_detail.html'
    context_object_name = 'detail'


# meta info for each page
def meta_info(request):
    meta = MetaInfo.objects.first()
    form = MetaInfoForm(instance=meta)
    if request.method == 'POST':
        form = MetaInfoForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect('adminPanel:meta-info')
    return render(request,'adminPanel/admin_meta_info.html',{'form':form})
