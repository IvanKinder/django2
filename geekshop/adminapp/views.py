from django.contrib.auth.decorators import user_passes_test
from django.db.models.expressions import F
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from adminapp.forms import ShopUserAdminEditForm, ProductCategoryEditForm, ProductEditForm, OrderEditForm
from authapp.forms import ShopUserRegisterForm
from authapp.models import ShopUser


# Users
from mainapp.models import ProductCategory, Product


# @user_passes_test(lambda u: u.is_superuser)
# def users(request):
#     title = 'Админка'
#     users_list = ShopUser.objects.all().order_by('is_active')
#     content = {
#         'objects': users_list,
#         'title': title
#     }
#     return render(request, 'adminapp/users.html', content)
from ordersapp.models import Order


class UsersListView(ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'
    # ordering = ...
    # paginate_by = 2

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


# @user_passes_test(lambda u: u.is_superuser)
# def user_create(request):
#     if request.method == 'POST':
#         user_form = ShopUserRegisterForm(request.POST, request.FILES)
#         if user_form.is_valid():
#             user_form.save()
#             return HttpResponseRedirect(reverse('admin:users'))
#     else:
#         user_form = ShopUserRegisterForm()
#
#     content = {
#         'update_form': user_form
#     }
#     return render(request, 'adminapp/user_update.html', content)


class UserCreateView(CreateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('admin:users')
    form_class = ShopUserRegisterForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


# @user_passes_test(lambda u: u.is_superuser)
# def user_update(request, pk):
#     edit_user = get_object_or_404(ShopUser, pk=pk)
#     if request.method == 'POST':
#         edit_form = ShopUserAdminEditForm(request.POST, request.FILES, instance=edit_user)
#         if edit_form.is_valid():
#             edit_form.save()
#             return HttpResponseRedirect(reverse('adminapp:user_update', args=[edit_user.pk]))
#     else:
#         edit_form = ShopUserAdminEditForm(instance=edit_user)
#
#     content = {
#         'update_form': edit_form
#     }
#
#     return render(request, 'adminapp/user_update.html', content)


class UserUpdateView(UpdateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('admin:users')
    form_class = ShopUserAdminEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'пользователи/редактирование'
        return context


# @user_passes_test(lambda u: u.is_superuser)
# def user_delete(request, pk):
#     user_item = get_object_or_404(ShopUser, pk=pk)
#
#     if request.method == 'POST':
#         if user_item.is_active:
#             user_item.is_active = False
#         else:
#             user_item.is_active = True
#         user_item.save()
#         return HttpResponseRedirect(reverse('admin:users'))
#
#     content = {
#         'user_to_delete': user_item
#     }
#     return render(request, 'adminapp/user_delete.html', content)


class UserDeleteView(DeleteView):
    model = ShopUser
    template_name = 'adminapp/user_delete.html'
    success_url = reverse_lazy('admin:users')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_active:
            self.object.is_active = False
        else:
            self.object.is_active = True
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


# Categories

# @user_passes_test(lambda u: u.is_superuser)
# def category_create(request):
#     new_category = ProductCategory()
#     if request.method == 'POST':
#         category_form = ProductCategoryEditForm(request.POST, request.FILES, instance=new_category)
#         if category_form.is_valid():
#             category_form.save()
#             return HttpResponseRedirect(reverse('admin:categories'))
#     else:
#         category_form = ProductCategoryEditForm()
#
#     content = {
#         'update_form': category_form
#     }
#     return render(request, 'adminapp/category_update.html', content)


class ProductCategoryCreateView(CreateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('admin:categories')
    # fields = '__all__'  # без стилей
    form_class = ProductCategoryEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


# @user_passes_test(lambda u: u.is_superuser)
# def categories(request):
#     categories_list = ProductCategory.objects.all().order_by('is_active')
#     content = {
#         'objects': categories_list
#     }
#
#     return render(request, 'adminapp/categories.html', content)


class ProductCategoriesListView(ListView):
    model = ProductCategory
    template_name = 'adminapp/categories.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


# @user_passes_test(lambda u: u.is_superuser)
# def category_update(request, pk):
#     edit_category = get_object_or_404(ProductCategory, pk=pk)
#     if request.method == 'POST':
#         edit_category = ProductCategoryEditForm(request.POST, request.FILES, instance=edit_category)
#         edit_category.save()
#         return HttpResponseRedirect(reverse('adminapp:categories'))
#     else:
#         edit_form = ProductCategoryEditForm(instance=edit_category)
#
#     content = {
#         'update_form': edit_form
#     }
#
#     return render(request, 'adminapp/category_update.html', content)


class ProductCategoryUpdateView(UpdateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('admin:categories')
    # fields = '__all__'  # без стилей
    form_class = ProductCategoryEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категории/редактирование'
        return context

    def form_valid(self, form):
        if 'discount' in form.cleaned_data:
            discount = form.cleaned_data['discount']
            if discount:
                self.object.product_set.update(price=F('price') * (1 - discount / 100))
        return super().form_valid(form)

# @user_passes_test(lambda u: u.is_superuser)
# def category_delete(request, pk):
#     category_item = get_object_or_404(ProductCategory, pk=pk)
#
#     if request.method == 'POST':
#         if category_item.is_active:
#             category_item.is_active = False
#         else:
#             category_item.is_active = True
#         category_item.save()
#         return HttpResponseRedirect(reverse('admin:categories'))
#
#     content = {
#         'category_to_delete': category_item
#     }
#     return render(request, 'adminapp/category_delete.html', content)


class ProductCategoryDeleteView(DeleteView):
    model = ProductCategory
    template_name = 'adminapp/category_delete.html'
    success_url = reverse_lazy('admin:categories')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        category_products = str(Product.objects.filter(category__pk=str(self.object.pk)))
        # category_products = str(self.object.pk)

        with open('log.txt', 'w') as log_file:
            log_file.write(category_products)

        if self.object.is_active:
            self.object.is_active = False
            # for product in category_products:
            #     product.object.is_active = False
            #     product.object.save()
        else:
            self.object.is_active = True
            # for product in category_products:
            #     product.object.is_active = True
            #     product.object.save()
        self.object.save()
        # self.object.is_active = False
        # self.object.save()

        return HttpResponseRedirect(self.get_success_url())


# Products

@user_passes_test(lambda u: u.is_superuser)
def product_create(request, pk):
    category_item = get_object_or_404(ProductCategory, pk=pk)

    if request.method == 'POST':
        update_form = ProductEditForm(request.POST, request.FILES)
        if update_form.is_valid():
            update_form.save()
            return HttpResponseRedirect(reverse('adminapp:products', args=[pk]))
    else:
        update_form = ProductEditForm()

    content = {
        'update_form': update_form,
        'category': category_item
    }

    return render(request, 'adminapp/product_update.html', content)


@user_passes_test(lambda u: u.is_superuser)
def products(request, pk):
    category_item = get_object_or_404(ProductCategory, pk=pk)
    products_list = Product.objects.filter(category=category_item)

    content = {
        'objects': products_list,
        'category': category_item
    }

    return render(request, 'adminapp/products.html', content)


# @user_passes_test(lambda u: u.is_superuser)
# def product_read(request, pk):
#     product_item = get_object_or_404(Product, pk=pk)
#     content = {
#         'object': product_item
#     }
#     return render(request, 'adminapp/product_read.html', content)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'adminapp/product_read.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


# @user_passes_test(lambda u: u.is_superuser)
# def product_update(request, pk):
#     product_item = get_object_or_404(Product, pk=pk)
#
#     if request.method == 'POST':
#         update_form = ProductEditForm(request.POST, request.FILES, instance=product_item)
#         if update_form.is_valid():
#             update_form.save()
#             return HttpResponseRedirect(reverse('adminapp:products', args=[pk]))
#     else:
#         update_form = ProductEditForm(instance=product_item)
#
#     content = {
#         'update_form': update_form,
#         'category': product_item.category
#     }
#
#     return render(request, 'adminapp/product_update.html', content)


class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('admin:products')
    form_class = ProductEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'продукты/редактирование'
        return context


@user_passes_test(lambda u: u.is_superuser)
def product_delete(request, pk):
    product_item = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        if product_item.is_active:
            product_item.is_active = False
        else:
            product_item.is_active = True
        product_item.save()
        return HttpResponseRedirect(reverse('admin:products', args=[product_item.category_id]))

    content = {
        'product_to_delete': product_item
    }
    return render(request, 'adminapp/product_delete.html', content)


class OrderListView(ListView):
    model = Order
    template_name = 'adminapp/orders.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class OrderUpdateView(UpdateView):
    model = Order
    template_name = 'adminapp/orders.html'
    success_url = reverse_lazy('admin:orders')
    form_class = OrderEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'заказы/редактирование'
        return context
