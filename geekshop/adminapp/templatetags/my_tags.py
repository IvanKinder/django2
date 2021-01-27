from django import template
from django.conf import settings


register = template.Library()


def media_folder_users(string):
    if not string:
        string = 'users_avatars/default.jpg'
        # return f'{settings.MEDIA_URL}{string}'
        return f'/media/{string}'

    return f'{string}'


# @register.filter(name='media_folder_products')
# def media_folder_products(string):
#     if not string:
#         string = 'products_images/default.jpg'
#
#     return f'{settings.MEDIA_URL}{string}'


register.filter('media_folder_users', media_folder_users)
