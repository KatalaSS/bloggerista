from django.conf.urls import url
from . views import home, post_detail, like_count_blog, create, search


urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^search/$', search, name='search'),
    url(r'^create/$', create, name='create'),
    url(r'^detail/(?P<slug>[-\w]+)/$', post_detail, name='detail'),
    url(r'^like-blog/$', like_count_blog, name='like_count_blog'),
]
