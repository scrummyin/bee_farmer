from django.views.generic import TemplateView, FormView
from django.core.urlresolvers import reverse
from django.conf import settings
from kazoo.client import KazooClient
from bees.forms import CreateNodeForm, EditNodeForm, DeleteNodeForm


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

    def get_initial(self):
        result = super(PathMixin, self).get_initial()
        result['path'] = self.node_path
        return result

    def get_context_data(self, **kwargs):
        context_data = super(PathMixin, self).get_context_data(**kwargs)
        context_data['node_path'] = self.node_path
        return context_data


class NodeValueMixin(object):
    """Needs the ZookeeperClientMixin"""
    _node_value = None

    @property
    def node_info(self):
        return self.zk_client.get(self.node_path)

    @property
    def node_value(self):
        if not self._node_value:
            value, stats = self.zk_client.get(self.node_path)
            self._node_value = value
        return self._node_value

    def get_initial(self):
        result = super(NodeValueMixin, self).get_initial()
        result['value'] = self.node_value
        return result

    def get_context_data(self, **kwargs):
        context_data = super(NodeValueMixin, self).get_context_data(**kwargs)
        value, stats = self.zk_client.get(self.node_path)
        context_data['value'] = value
        context_data['stats'] = stats
        return context_data


class SetActiveViewMixin(object):
    def get_context_data(self, **kwargs):
        context = super(SetActiveViewMixin, self).get_context_data(**kwargs)
        context['active_nav_menu'] = {
            self.request.resolver_match.url_name: ' class="active"'
        }
        return context


class DirectoryListingMixin(object):
    """Needs the ZookeeperClientMixin"""

    def get_context_data(self, **kwargs):
        context_data = super(DirectoryListingMixin, self).get_context_data(**kwargs)
        context_data['directories'] = self.zk_client.get_children(self.node_path)
        return context_data


class BrowseNodeView(SetActiveViewMixin, DirectoryListingMixin, NodeValueMixin, PathMixin, ZookeeperClientMixin, TemplateView):
    template_name = 'bees/browse_node.html'


class DeleteNodeView(SetActiveViewMixin, PathMixin, ZookeeperClientMixin, FormView):
    template_name = 'bees/delete_node.html'
    form_class = DeleteNodeForm

    def form_valid(self, form):
        result = super(DeleteNodeView, self).form_valid(form)
        self.zk_client.delete(form.cleaned_data.get('path'))
        return result

    @property
    def formated_parent_path(self):
        return '/' + '/'.join([x for x in self.node_path.split('/') if x][:-1]) + '/'

    def get_success_url(self):
        return reverse('bees:browse_node', kwargs={'path': self.formated_parent_path})


class EditNodeView(SetActiveViewMixin, NodeValueMixin, PathMixin, ZookeeperClientMixin, FormView):
    template_name = 'bees/edit_node.html'
    form_class = EditNodeForm

    def form_valid(self, form):
        result = super(EditNodeView, self).form_valid(form)
        zk_upload_value = str(form.cleaned_data.get('value'))
        self.zk_client.set(form.cleaned_data.get('path'), zk_upload_value)
        return result

    def get_success_url(self):
        return reverse('bees:browse_node', kwargs={'path': self.node_path})


class CreateNodeView(SetActiveViewMixin, PathMixin, ZookeeperClientMixin, FormView):
    template_name = 'bees/create_node.html'
    form_class = CreateNodeForm

    def form_valid(self, form):
        result = super(CreateNodeView, self).form_valid(form)
        new_node_path = form.cleaned_data.get('path') + form.cleaned_data.get('node_name')
        self.zk_client.ensure_path(new_node_path)
        value = form.cleaned_data.get('value', '')
        if value:
            self.zk_client.set(new_node_path, value.encode())
        return result

    def get_success_url(self):
        return reverse('bees:browse_node', kwargs={'path': self.node_path})
