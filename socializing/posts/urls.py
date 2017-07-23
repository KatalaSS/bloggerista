from django.conf.urls import url
from . views import (home,
                     create_post,
                     post_detail,
                     post_update,
                     post_delete,
                     comment_delete,
                     search,
                     post_like_toggle,
                     PostLikeToggle)


urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^search/$', search, name='search'),
    url(r'^create/$', create_post, name='create'),
    url(r'^(?P<slug>[-\w]+)/$', post_detail, name='detail'),
    url(r'^(?P<slug>[-\w]+)/update/$', post_update, name='update'),
    url(r'^(?P<slug>[-\w]+)/delete/$', post_delete, name='delete'),
    url(r'^(?P<slug>[-\w]+)/(?P<pk>\d+)/delete/$', comment_delete, name='comment_delete'),
    url(r'^(?P<slug>[-\w]+)/likes$', post_like_toggle, name='like-toggle'),
    url(r'^(?P<slug>[-\w]+)/like/$', PostLikeToggle.as_view(permanent=False), name='like-toggle2'),
]
