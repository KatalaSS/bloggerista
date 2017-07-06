from django.conf.urls import url
from . views import (home,
                     post_detail,
                     create,
                     search,
                     post_like_toggle,
                     PostLikeToggle)


urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^search/$', search, name='search'),
    url(r'^create/$', create, name='create'),
    url(r'^(?P<slug>[-\w]+)/$', post_detail, name='detail'),
    url(r'^(?P<slug>[-\w]+)/likes$', post_like_toggle, name='like-toggle'),
    url(r'^(?P<slug>[-\w]+)/like/$', PostLikeToggle.as_view(permanent=False), name='like-toggle2'),

]
