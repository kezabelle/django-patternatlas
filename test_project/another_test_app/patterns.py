"""
This just serves to demonstrate the _splitting_ and __filtering__ by
application.

Also we don't support markdown.
"""
from django.template.context import RequestContext
from django.template.loader import render_to_string
from patternatlas import is_pattern


@is_pattern
def example_header(request):
    """
    This is how all headings should be rendered
    """
    return render_to_string('example_header.html', {},
                            context_instance=RequestContext(request))


def nested_callable2(request):
    return render_to_string('example_nested.html', {},
                            context_instance=RequestContext(request))


def nested_callable1(request):
    return nested_callable2


@is_pattern(assets={'top': ('css/example_base.css', 'css/example_progress.css')})
def example_nested_callable(request):
    """
    Somtimes it is useful to be able to have your pattern serve as a dispatch
    method for another callable. When rendering, the ``Pattern`` object will
    continue trying to call return values until they are no longer callable.

    This allows potentially infinite nesting of callables, as long as they
    take the required parameters (``request``).
    """
    return nested_callable1
