from django.conf.urls import url
from .views import create, image_detail, image_like, image_list, image_rangking

urlpatterns = [
    url(r'^$', image_list, name='list'),
    url(r'^create/$', create, name='create'),
    url(r'^ranking/$', image_rangking, name='rangking'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', image_detail, name='detail'),
    url(r'^like/$', image_like, name='like'),
]
