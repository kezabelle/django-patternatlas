=============
Pattern Atlas
=============

``django-patternatlas`` is a re-usable application for collecting components
(templates, CSS, javascript etc) into a single living style guide.

It reads a ``patterns`` module for each of the ``INSTALLED_APPS`` and
collects callables with the attribute ``is_pattern``, and then assembles
them into a browsable webapp.

Currently at version: 0.2.0

Writing pattern callables
-------------------------

An example pattern component::

    from django.template.loader import render_to_string
    from patternatlas import is_pattern

    @is_pattern
    def example_header(request):
        return render_to_string('header.html', {})

That's it.

Patterns may also be classes::

    class ExampleHeader(object):
        is_pattern = True

        def __init__(self, request):
            self.request = request

        def __call__(self, request):
            return render_to_string('header.html', {})

Including asset dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can require assets, though the way to do it differs between functions and
classes::

    @is_pattern(assets={'top': ['style.css', 'style2.css']})
    def example_header(request):
        ...

For classes::

    class ExampleHeader(object):
        assets = {'top': ['style.css', 'style2.css']}

There are two keys available for assets: ``top`` and ``bottom``, the former
is used for CSS and javascript etc that needs to be loaded up-front, while
the latter is typically for javascript usage.

Callables in callables
^^^^^^^^^^^^^^^^^^^^^^

If a given pattern returns a **callable**, rather than a string of rendered
output, that callable will itself be called. This will occur until a callable
chain stops returning new callables. A simple example::

    def callable1(request):
        return callable2

    def callable2(request):
        return ''

    @is_pattern
    def entry_callable(request):
        return callable1

In the above example, the contents of ``callable2`` are ultimately what is
rendered in the browser, though the pattern ``entry_callable`` is what is
auto-discovered, and what declares any assets. This allows for easily wrapping of existing callables to be exposed as patterns,
while keeping the dependencies separate.

Each callable in the chain must accept ``request`` as a keyword argument.

Installation
------------

add ``patternatlas`` to your settings::

    INSTALLED_APPS += ('patternatlas',)

Add the app to your main ``urls.py``::

    from django.conf.urls import include, patterns
    import patternatlas

    urlpatterns += ('',
        url(r'^styleguide/', include(patternatlas.urlconf)),
    )

Write yourself some patterns, and visit ``/styleguide/`` in your browser.

Database interactions
---------------------

In theory, when a ``Pattern`` is rendered (by calling ``.content``, in a template)
it will attempt to abort any database transactions in progress, so that the patterns you write can interact with the database.

How well that works, I don't really know yet, and for performance reasons alone I'd suggest avoiding hitting the database, instead favouring constructing your ``Model`` instances without calling ``.save()`` on them, or creating a giant dictionary of values that fulfils the contract between the template and the context.

Freezing your style guide
-------------------------

Currently, support for building your style guide into static HTML is only
available using `django_medusa`_, though this may expand in future.

To freeze, add ``django_medusa`` to your ``INSTALLED_APPS``, set the
required configuration variables, and do::

    python manage.py staticsitegen

.. _django_medusa: https://github.com/mtigas/django-medusa
