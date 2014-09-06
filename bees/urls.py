from django.conf.urls import patterns, url
from bees.views import BrowseNodeView, CreateNodeView, EditNodeView


urlpatterns = patterns('',
    url(r'^browse(?P<path>.*)$', BrowseNodeView.as_view(), name="browse_node"),
    url(r'^create(?P<path>.*)$', CreateNodeView.as_view(), name="create_node"),
    url(r'^edit(?P<path>.*)$', EditNodeView.as_view(), name="edit_node"),
)
