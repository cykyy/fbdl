from django.urls import path
from .views import *

app_name = 'fbdl'
urlpatterns = [
    path('', fbdl_front_view, name='fbdl_front_view'),
    path('ajax/insert/', ajax_post_fb_link, name='fbdl_aj_1'),
    path('ajax/dl/', ajax_post_format_dl, name='fbdl_aj_2'),
]
