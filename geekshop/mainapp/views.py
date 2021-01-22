import random

from django.conf import settings
from django.core.cache import cache
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404

from basketapp.models import Basket
from mainapp.models import Product, ProductCategory


def get_links_menu():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.filter(is_active=True)
            cache.set(key, links_menu)
        return links_menu
    else:
        return ProductCategory.objects.filter(is_active=True)


def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}'
        category = cache.get(key)
        if category is None:
            category = get_object_or_404(ProductCategory, pk=pk)
            cache.set(key, category)
        return category
    else:
        return get_object_or_404(ProductCategory, pk=pk)


def main(request):
    # products = Product.objects.all()[:4]
    products = Product.objects.filter(is_active=True, category__is_active=True).select_related('category')[:3]
    content = {
        'title': 'Главная',
        'products': products,
        # 'basket': get_basket(request.user),
    }
    return render(request, 'mainapp/index.html', content)


# def get_basket(user):
#     if user.is_authenticated:
#         return Basket.objects.filter(user=user)
#     return []

def get_hot_product():
    products_list = Product.objects.all()
    return random.sample(list(products_list), 1)[0]


def get_same_products(hot_product):
    return Product.objects.filter(category__pk=hot_product.category.pk).exclude(pk=hot_product.pk)[:3]


def products(request, pk=None, page=1):
    links_menu = get_links_menu()

    if pk is not None:
        if pk == 0:
            products_list = Product.objects.all()
            category = {'name': 'все', 'pk': 0}
        else:
            # category = ProductCategory.objects.get(pk=pk)
            category = get_category(pk)
            products_list = Product.objects.filter(category__pk=pk)

        paginator = Paginator(products_list, 2)
        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)

        content = {
            'title': 'Продукты',
            'links_menu': links_menu,
            'products': products_paginator,
            'category': category,
            # 'basket': quantity_and_price
            # 'basket': get_basket(request.user),
            'hot_product': get_hot_product(),
        }

        return render(request, 'mainapp/products_list.html', content)

    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)

    content = {
        'title': 'Продукты',
        'links_menu': links_menu,
        # 'basket': get_basket(request.user),
        'hot_product': hot_product,
        'same_products': same_products,
    }
    return render(request, 'mainapp/products.html', content)


def product(request, pk):
    title = 'продукты'

    content = {
        'title': title,
        'links_menu': get_links_menu(),
        'product': get_object_or_404(Product, pk=pk),
        # 'basket': get_basket(request.user),
    }
    return render(request, 'mainapp/product.html', content)


def contacts(request):
    content = {
        'title': 'Контакты',
        # 'basket': get_basket(request.user),
    }
    return render(request, 'mainapp/contact.html', content)


def not_found(request, exception):
    return render(request, '404.html', {'item': 'item'}, status=404)
