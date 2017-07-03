from django.conf.urls import url
import views
from .forms import CustomAuthenticationForm
from django.contrib.auth.views import (password_reset_complete,
                                       password_reset_confirm,
                                       password_reset_done,
                                       password_reset,
                                       password_change_done,
                                       password_change,
                                       logout_then_login,
                                       login,
                                       logout)

urlpatterns = (
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', login, {'authentication_form': CustomAuthenticationForm}, name='login'),
    url(r'^logout/$', logout, {'next_page': 'login'}, name='logout'),
    url(r'^login/$', logout_then_login, name='logout_then_login'),
    url(r'^password-change/$', password_change,
        {'template_name': 'registration/password_change_form_.html'}, name='password_change'),
    url(r'^password-change/done/$', password_change_done,
        {'template_name': 'registration/password_change_done_.html'}, name='password_change_done'),
    url(r'^password-reset/$', password_reset,
        {'template_name': 'registration/password_reset_form_.html'}, name='password_reset'),
    url(r'^password-reset/done/$', password_reset_done,
        {'template_name': 'registration/password_reset_done_.html'}, name='password_reset_done'),
    url(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$', password_reset_confirm,
        {'template_name': 'registration/password_reset_confirm_.html'}, name='password_reset_confirm'),
    url(r'^password-reset/complete/$', password_reset_complete,
        {'template_name': 'registration/password_reset_done_.html'}, name='password_reset_complete'),
    url(r'^edit/$', views.edit, name='edit'),
    url(r'^people/$', views.user_list, name='user_list'),
    url(r'^profile/(?P<author>[-\w]+)/notifications/$', views.notifications, name='notifications'),
    url(r'^profile/(?P<author>[-\w]+)/$', views.user_profile, name='user_profile'),
    url(r'^profile/(?P<author>[-\w]+)/follow/$', views.UserFollowView.as_view(), name='follow'),
    url(r'^profile/(?P<author>[-\w]+)/following/$', views.following, name='following'),
    url(r'^profile/(?P<author>[-\w]+)/followers/$', views.followers, name='followers'),
)
