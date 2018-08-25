from django.conf.urls import url
from .views import user_login, user_register, edit_profile, user_list, user_detail, user_follow


urlpatterns = [
    #url(r'^login/$', user_login, name='login'),
    url(r'^users/$', user_list, name='list'),
    url(r'^users/follow/$', user_follow, name='follow'),
    url(r'^users/(?P<username>[-\w]+)/$', user_detail, name='detail'),
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^register/$', user_register, name='register'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),
    url(r'^profile/edit/$', edit_profile, name='edit-profile'),
    url(r'^logout-then-login/$', 'django.contrib.auth.views.logout_then_login', name='logout-then-login'),
    url(r'^password-change/(?P<post_change_redirect>[\w:-]+)$', 'django.contrib.auth.views.password_change', name='password-change'),
    url(r'^password-change/done/$', 'django.contrib.auth.views.password_change_done', name='password_change_done'),
    url(r'^password-reset/(?P<post_reset_redirect>[\w:]+)$', 'django.contrib.auth.views.password_reset', name='password_reset'),
    url(r'^password-reset/done/$', 'django.contrib.auth.views.password_reset_done',
        name='password_reset_done'),
    url(r'^password-reset/confirm/(?P<uidb64>[\w-]+)/(?P<token>[\w-]+)/(?P<post_reset_redirect>[\w:-]+)/$',
        'django.contrib.auth.views.password_reset_confirm',
        name='password_reset_confirm'),
    url(r'^password-reset/complete/$', 'django.contrib.auth.views.password_reset_complete',
        name='password_reset_complete')
]
