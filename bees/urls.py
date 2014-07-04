from django.conf.urls import patterns, url
from bees.views import BrowseNodeView


urlpatterns = patterns('',
    url(r'^browse(?P<path>.*)$', BrowseNodeView.as_view(), name="browse_node"),
)
