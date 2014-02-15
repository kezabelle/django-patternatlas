import sys
import wrapt
import functools
from itertools import chain
from collections import defaultdict
try:
    from django.utils.text import camel_case_to_spaces as get_verbose_name
except ImportError:  # pragma: no cover (Django < 1.7)
    from django.db.models.options import get_verbose_name
from django.utils.encoding import python_2_unicode_compatible
from django.db import transaction
from django.conf import settings
from django.core.urlresolvers import reverse
try:
    from importlib import import_module
except ImportError:
    from django.utils.importlib import import_module
from .templatetags.patternatlus import fix_raw_asset


@python_2_unicode_compatible
class Pattern(object):
    __slots__ = ('callable', 'callable_name', 'description', 'is_pattern',
                 'module', 'name', 'request', '_assets', '_content')

    def __init__(self, callable_pattern, request=None):
        self.is_pattern = True
        self.callable = callable_pattern
        self.description = callable_pattern.__doc__
        # weird hack from Django
        patterns_module = sys.modules[callable_pattern.__module__]
        self.module = patterns_module.__name__.split('.')[-2]
        self.callable_name = self.callable.__name__
        self.name = get_verbose_name(self.callable_name).replace('_', ' ')
        self.request = request
        self._content = None
        self._assets = None

    def _get_content(self):
        transaction.enter_transaction_management()
        # transaction.managed(False)
        # sid = transaction.savepoint()
        self._assets = defaultdict(list)
        try:
            output = self.callable
            while callable(output):

                # collect css/js in an ordered fashion, de-duping on the way.
                if hasattr(output, 'assets'):
                    for key, value in output.assets.items():
                        for thing in value:
                            if thing not in self._assets[key]:
                                self._assets[key].append(thing)

                # it's probably a class instance, or a response generator
                output = output(request=self.request)
        finally:
            transaction.abort()
            # transaction.savepoint_rollback(sid)
            # transaction.leave_transaction_management()
        return output

    def content(self):
        if self._content is None:
            self._content = self._get_content()
        return self._content

    def assets(self):
        if self._assets is None:
            self.content()
        return self._assets

    def get_absolute_url(self):
        return reverse('patternatlus:pattern', kwargs={
            'app_label': self.module,
            'pattern': self.callable_name,
        })

    def get_parent_url(self):
        return reverse('patternatlus:app', kwargs={
            'app_label': self.module,
        })

    def __repr__(self):
        return '<{mod}.{cls}: app_label={app}, name={callable}>'.format(
            mod=self.__module__, cls=self.__class__.__name__,
            app=self.module, callable=self.callable_name)

    def __str__(self):
        desc = self.description or ''
        if len(desc) > 30:
            desc = '{0}... truncated'.format(self.description[:30])
        return 'Pattern "{name}" ({desc})'.format(name=self.name,
                                                  desc=desc)

    def __eq__(self, other):
        return self.callable == other.callable

    def __contains__(self, lookup):
        return lookup == self.callable


@python_2_unicode_compatible
class Atlus(object):
    __slots__ = ('discovered', 'request',)

    def __init__(self, presets=None, request=None):
        if presets is not None:
            presets = self.sort(list(presets))
        self.request = request
        self.discovered = presets or []
        self.discover()

    def sort(self, discovered):
        unsorted = tuple(discovered)
        resorted = sorted(unsorted, key=lambda x: (x.module, x.callable_name))
        return resorted

    def discover(self):
        if self.discovered:
            return self.discovered

        discovered = set()
        for app in settings.INSTALLED_APPS:
            module_path = '{0}.patterns'.format(app)
            try:
                module = import_module(module_path)
            except ImportError:
                continue

            for possible_pattern in dir(module):
                if possible_pattern.startswith('_'):
                    continue

                if possible_pattern.isupper():
                    continue

                probable_pattern = getattr(module, possible_pattern)

                if not callable(probable_pattern):
                    continue

                if hasattr(probable_pattern, 'is_pattern'):
                    definite_pattern = Pattern(
                        callable_pattern=probable_pattern,
                        request=self.request)
                    discovered.add(definite_pattern)
        self.discovered = self.sort(discovered)
        return self.discovered

    def app_labels_and_pattern_names(self):
        unsorted_data = ((pattern.module, pattern.callable_name)
                         for pattern in self)
        return sorted(frozenset(unsorted_data))

    def app_labels(self):
        return sorted(frozenset(label for label, pattern
                                in self.app_labels_and_pattern_names()))

    def pattern_names(self):
        return sorted(frozenset(pattern for label, pattern
                                in self.app_labels_and_pattern_names()))

    def assets(self):
        _assets = {
            'top': [],
            'bottom': [],
        }
        # this is rubbish.
        for pattern in self:
            individual_assets = pattern.assets()
            # only loop over the keys we're going to provide to the output.
            for position in _assets.keys():
                values = individual_assets.get(position, ())
                # de-dup and add.
                for value in values:
                    if value not in _assets[position]:
                        _assets[position].append(fix_raw_asset(value))
        return _assets

    def __iter__(self):
        return iter(self.discovered)

    # def __getitem__(self, app_label):
    #     return self.__class__(presets=(x for x in self.discovered
    #                           if x.module == app_label))

    # def __getattr__(self, name):
    #     return self.__class__(presets=(x for x in self.discovered
    #                           if x.callable_name == name))

    def only_app(self, app_label):
        found = set()
        for pattern in self:
            if pattern.module == app_label:
                found.add(pattern)
        return self.__class__(presets=found, request=self.request)

    def only_app_pattern(self, app_label, pattern_name):
        found = set()
        for pattern in self:
            is_in_app = pattern.module == app_label
            is_pattern_name = pattern.callable_name == pattern_name
            if is_in_app and is_pattern_name:
                found.add(pattern)
        return self.__class__(presets=found, request=self.request)

    def __contains__(self, obj):
        return obj in self.discovered

    def __len__(self):
        return len(self.discovered)

    def __nonzero__(self):
        return len(self) > 0

    __bool__ = __nonzero__

    def __str__(self):
        return 'Atlus containing {count} patterns'.format(count=len(self))

    def __repr__(self):
        patts = (repr(pattern) for pattern in self.discovered)
        return '<{mod}.{cls} containing {count} patterns: {patterns}'.format(
            mod=self.__module__, cls=self.__class__.__name__,
            patterns=', '.join(patts), count=len(self))

    def __add__(self, other):
        return self.__class__(presets=chain(self.discovered, other.discovered),
                              request=self.request or other.request)


def is_pattern(func=None, assets=None):
    def __is_pattern(func, assets):
        if not hasattr(func, 'is_pattern'):
            func.is_pattern = True
        if not hasattr(func, 'assets'):
            func.assets = assets or {}
        return func

    if func:
        return __is_pattern(func, assets=assets)
    else:
        return functools.partial(__is_pattern, assets=assets)

    # import pdb; pdb.set_trace()
    # if not hasattr(func, 'is_pattern'):
    #     func.is_pattern = True
    # if not hasattr(func, 'assets'):
    #     func.assets = None or {}
    return func
