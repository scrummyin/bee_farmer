from django.views.generic import TemplateView
from django.conf import settings
from kazoo.client import KazooClient


class ZookeeperClientMixin(object):
    @property
    def zk_client(self):
        if hasattr(self, "_zk_client"):
            return self._zk_client
        self._zk_client = KazooClient(hosts=settings.ZOOKEEPER_HOSTS)
        self._zk_client.start()
        return self._zk_client


class PathMixin(object):
    @property
    def node_path(self):
        return self.kwargs.get('path')

    def get_context_data(self, **kwargs):
        context_data = super(PathMixin, self).get_context_data(**kwargs)
        context_data['node_path'] = self.node_path
        return context_data


class NodeValueMixin(object):
    """Needs the ZookeeperClientMixin"""

    def get_context_data(self, **kwargs):
        context_data = super(NodeValueMixin, self).get_context_data(**kwargs)
        value, stats = self.zk_client.get(self.node_path)
        context_data['value'] = value
        context_data['stats'] = stats
        return context_data


class DirectoryListingMixin(object):
    """Needs the ZookeeperClientMixin"""

    def get_context_data(self, **kwargs):
        context_data = super(DirectoryListingMixin, self).get_context_data(**kwargs)
        context_data['directories'] = self.zk_client.get_children(self.node_path)
        return context_data


class BrowseNodeView(DirectoryListingMixin, NodeValueMixin, PathMixin, ZookeeperClientMixin, TemplateView):
    template_name = 'bees/browse_node.html'

class CreateNodeView(PathMixin, ZookeeperClientMixin):
    templateview = 'bees/create_node.html'
