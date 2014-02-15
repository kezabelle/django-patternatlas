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
