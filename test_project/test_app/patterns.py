from random import randint
from django.contrib.auth.models import User
from django.template.context import RequestContext
from django.template.loader import render_to_string
from patternatlus import is_pattern


@is_pattern(assets={'top': ['css/example_base.css',
                            'css/example_table.css']})
def example_table(request):
    """
    How tables should be rendered wherever they're used.
    """
    users = [User(
        username='username{0}'.format(randint(1, 1000)),
        first_name='ForeName {0}'.format(randint(1, 10)),
        last_name='SurName {0}'.format(randint(11, 20)))
        for x in range(1, 5)]
    context = {
        'object_list': users,
    }
    return render_to_string('example_table.html', context,
                            context_instance=RequestContext(request))


@is_pattern(assets={'top': ['css/example_base.css',
                            'css/example_breadcrumbs.css']})
def example_breadcrumbs(request):
    users = [User(
        username='username{0}'.format(randint(1, 1000)),
        first_name='ForeName {0}'.format(randint(1, 10)),
        last_name='SurName {0}'.format(randint(11, 20)))
        for x in range(1, 5)]
    context = {
        'object_list': users,
    }
    return render_to_string('example_breadcrumbs.html', context,
                            context_instance=RequestContext(request))


class ExamplePagination(object):
    is_pattern = True

    assets = {
        'top': ('css/example_base.css', 'css/example_pagination.css'),
    }

    def __init__(self, request):
        self.request = request

    def __call__(self, request):
        context = {
            'pages': range(1, 10),
        }
        return render_to_string('example_pagination.html', context,
                                context_instance=RequestContext(request))
