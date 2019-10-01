from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reversefrom jinja2 import Environmentdef environment(**options):
    env = Environment(**options)
    env.globals.update({
        ‘static’: staticfiles_storage.url,
        ‘url’: reverse,
    })
    return env
