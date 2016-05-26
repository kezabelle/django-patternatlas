=============
Pattern Atlas
=============

:author: Keryn Knight
:version: 0.3.0

``django-patternatlas`` is a re-usable application for collecting components
(templates, CSS, javascript etc) into a single living style guide.

It reads a ``patterns`` module for each of the ``INSTALLED_APPS`` and
collects callables with the attribute ``is_pattern``, and then assembles
them into a browsable webapp.

Installation
------------

Writing pattern callables
-------------------------

Freezing your style guide
-------------------------

Publishing your patterns in sitemaps
------------------------------------

Testing
-------

The license
-----------

It's the `FreeBSD`_. There's should be a ``LICENSE`` file in the root of the repository, and in any archives.

.. _FreeBSD: http://en.wikipedia.org/wiki/BSD_licenses#2-clause_license_.28.22Simplified_BSD_License.22_or_.22FreeBSD_License.22.29
