from django import template
from django.core.urlresolvers import reverse

register = template.Library()


@register.inclusion_tag('bees/_breadcrumbs.html', takes_context=True)
def create_bread_crumb_links(context):
    base_line = '<a href="%s">%s</a>'
    the_crumbs = []
    partials = filter(bool, context.get('node_path', '').split('/'))
    base_path = '/'
    the_crumbs.append(base_line % (reverse('bees:browse_node', kwargs={'path': '/'}), 'root:'))
    for node in partials:
        node_name = node + '/'
        base_path += node_name
        url = reverse('bees:browse_node', kwargs={'path': base_path})
        the_crumbs.append(base_line % (url, node), )
    return {'the_crumbs': the_crumbs}
