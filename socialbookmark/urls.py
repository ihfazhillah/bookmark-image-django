from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from .views import dashboard

from django.views.generic import TemplateView

urlpatterns = [
    # Examples:
    # url(r'^$', 'social.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^', include('accounts.urls', namespace='accounts')),
    url(r'^social-auth/', include('social.apps.django_app.urls', namespace='social')),
    url(r'^dashboard/$', dashboard, name='dashboard'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^images/', include('images.urls', namespace='images')),
    url(r'^base_file/$', TemplateView.as_view(template_name='base.html')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
