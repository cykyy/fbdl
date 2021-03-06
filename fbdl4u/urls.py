from django.urls import path
from django.conf.urls import url
from fbdl import settings
from django.views.static import serve
from .views import *

app_name = 'fbdl'
urlpatterns = [
    path('', fbdl_front_view, name='fbdl_front_view'),
    path('ajax/insert/', ajax_post_fb_link, name='fbdl_aj_1'),
    path('ajax/dl/', ajax_post_format_dl, name='fbdl_aj_2'),
    path('contact/', contact_us_view, name='contact'),
    path('privacy-policy/', privacy_policy_view, name='privacy_policy_view'),
    path('terms/', terms_view, name='terms_view'),
]

# for development mode
if settings.DEBUG:
    """urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]"""
    urlpatterns += [
        url(r'^media/audio/deliver/(?P<path>.*)$', serve, {
            'document_root': 'media/audio/deliver/',
        }),
    ]
