from django.conf.urls import patterns, include, url
from bees import urls as bees_urls

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bee_farm.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^bees/', include(bees_urls, namespace='bees')),
)
