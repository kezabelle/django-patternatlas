import logging
import sys
from bs4 import BeautifulSoup
import functools
from hashlib import sha1
from itertools import chain
from collections import defaultdict
from docutils.core import publish_parts
from sphinx.util.docstrings import prepare_docstring
from pygments import highlight
from pygments.lexers import HtmlLexer
from pygments.formatters import HtmlFormatter
try:
    from django.utils.text import camel_case_to_spaces as get_verbose_name
except ImportError:  # pragma: no cover (Django < 1.7)
    from django.db.models.options import get_verbose_name
from django.utils.encoding import python_2_unicode_compatible
from django.utils.encoding import force_text
from django.utils.encoding import force_bytes
from django.db import transaction
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
try:
    from importlib import import_module
except ImportError:
    from django.utils.importlib import import_module
try:
    from django.utils.text import slugify
except ImportError:
    from django.template.defaultfilters import slugify
from .templatetags.patternatlas import fix_raw_asset


logger = logging.getLogger(__name__)


@python_2_unicode_compatible
class Pattern(object):
    __slots__ = ('callable', 'callable_name', '_description', 'is_pattern',
                 'module', 'module_name', 'name', 'request', '_assets',
                 '_content', '_module_description')

    def __init__(self, callable_pattern, request=None):
        self.is_pattern = True
        self.callable = callable_pattern
        self._description = self._fix_docstring(callable_pattern.__doc__)
        # weird hack from Django
        patterns_module = sys.modules[callable_pattern.__module__]
        self.module = patterns_module.__name__.split('.')[-2]
        self.module_name = get_verbose_name(self.module).replace('_', ' ')
        self._module_description = self._fix_docstring(patterns_module.__doc__)
        self.callable_name = slugify(force_text(get_verbose_name(self.callable.__name__)))
        self.name = get_verbose_name(self.callable.__name__).replace('_', ' ')
        self.request = request
        self._content = None
        self._assets = None

    def _fix_docstring(self, data):
        if data is None:
            return ''
        else:
            return "\n".join(prepare_docstring(data))

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

        return "\n".join(x for x in output.splitlines() if x.strip())

    def content(self):
        if self._content is None:
            self._content = self._get_content()
        return self._content

    def content_syntax_highlighted(self):
        lexer = HtmlLexer(stripall=True, encoding='utf-8')
        formatter = HtmlFormatter(linenos=False, encoding='utf-8')
        content = self.content()
        try:
            soup = BeautifulSoup(content, ["html5lib", "lxml"])
            content = soup.prettify(formatter=None)
        except:  # noqa no idea wtf it could raise
            logger.info("Unable to prettify with BeautifulSoup4, so just "
                        "carry on and see if pygments can do something "
                        "with it.", exc_info=1, extra={'request': self.request})
        try:
            return highlight(content, lexer=lexer, formatter=formatter)
        except:  # no idea wtf it could raise.
            logger.error("Unable to use pygments to highlight given content",
                         exc_info=1, extra={'request': self.request})
            return '<unparsable>'

    def assets(self):
        if self._assets is None:
            self.content()
        return self._assets

    def get_absolute_url(self):
        return reverse('patternatlas:pattern', kwargs={
            'app_label': self.module,
            'pattern': self.callable_name,
        })

    def get_parent_url(self):
        return reverse('patternatlas:app', kwargs={
            'app_label': self.module,
        })

    def get_unique_ref(self):
        return sha1(
            force_bytes(' '.join((self.module, self.callable_name)))
        ).hexdigest()

    def get_short_ref(self):
        return self.get_unique_ref()[:8]

    def __repr__(self):
        return '<{mod}.{cls}: app_label={app}, name={callable}>'.format(
            mod=self.__module__, cls=self.__class__.__name__,
            app=self.module, callable=self.callable_name)

    def __str__(self):
        desc = self._description or ''
        if len(desc) > 30:
            desc = '{0}... truncated'.format(self.description[:30])
        return 'Pattern "{name}" ({desc})'.format(name=self.name,
                                                  desc=desc)

    def __eq__(self, other):
        return self.callable == other.callable

    def __contains__(self, lookup):
        return lookup == self.callable

    @property
    def __doc__(self):
        return to_rst(self._description)

    @property
    def __moduledoc__(self):
        return to_rst(self._module_description)

    description = __doc__
    module_description = __moduledoc__


@python_2_unicode_compatible
class Atlas(object):
    __slots__ = ('discovered', 'request',)

    def __init__(self, presets=None, request=None):
        self.request = request
        if presets is not None:
            presets = self.sort(list(presets))
        self.discovered = presets or []
        # avoid re-collecting ...
        if presets is None:
            self.discover()

    def sort(self, discovered):
        unsorted = tuple(discovered)
        resorted = sorted(unsorted, key=lambda x: (x.module, x.callable_name))
        return resorted

    def discover(self):
        discovered_reprs = set()
        discovered_patterns = []

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
                    pattern_repr = repr(definite_pattern)
                    if pattern_repr not in discovered_reprs:
                        discovered_patterns.append(definite_pattern)
                        discovered_reprs.add(pattern_repr)
        self.discovered = self.sort(discovered_patterns)
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
                    fixed_value = fix_raw_asset(value)
                    if fixed_value not in _assets[position]:
                        _assets[position].append(fixed_value)
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
        found_reprs = set()
        found_patterns = []
        for pattern in self:
            if pattern.module == app_label:
                pattern_repr = repr(pattern)
                if pattern_repr not in found_reprs:
                    found_patterns.append(pattern)
                    found_reprs.add(pattern_repr)
        return self.__class__(presets=found_patterns, request=self.request)

    def only_app_pattern(self, app_label, pattern_name):
        found_reprs = set()
        found_patterns = []
        for pattern in self:
            is_in_app = pattern.module == app_label
            is_pattern_name = pattern.callable_name == pattern_name
            if is_in_app and is_pattern_name:
                pattern_repr = repr(pattern)
                if pattern_repr not in found_reprs:
                    found_patterns.append(pattern)
                    found_reprs.add(pattern_repr)
        return self.__class__(presets=found_patterns, request=self.request)

    def __contains__(self, obj):
        return obj in self.discovered

    def __len__(self):
        return len(self.discovered)

    def __nonzero__(self):
        return len(self) > 0

    __bool__ = __nonzero__

    def __str__(self):
        return '{cls} containing {count} patterns'.format(
            count=len(self), cls=self.__class__.__name__)

    def __repr__(self):
        patts = (repr(pattern) for pattern in self.discovered)
        return '<{mod}.{cls} containing {count} patterns: {patterns}>'.format(
            mod=self.__module__, cls=self.__class__.__name__,
            patterns=', '.join(patts), count=len(self))

    def __add__(self, other):
        return self.__class__(presets=chain(self.discovered, other.discovered),
                              request=self.request or other.request)

    @property
    def __doc__(self):
        # output module's description if we're in an app only Atlas.
        if len(self.app_labels()) == 1:
            return self.discovered[0].module_description or ''
        else:
            patts = (repr(pattern) for pattern in self.discovered)
            title = force_text(self)
            doc = """
            {sep}
            {cls}
            {sep}

            The following have been defined:
            {patterns}
            """.format(cls=title, sep='=' * len(title),
                       patterns="\n\n".join(patts))
            prepared_doc = prepare_docstring(doc)
            parsed_doc = to_rst("\n".join(prepared_doc))
            return parsed_doc

    description = __doc__
    module_description = __doc__

    def __getitem__(self, value):
        try:
            return self.discovered[int(value)]
        except (TypeError, ValueError) as e:
            return super(Atlas, self).__getitem__(value)


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
    return func


def to_rst(docstring):
    if len(docstring) < 1:
        return ''
    try:
        parsed = publish_parts(source=force_text(docstring),
                               source_path=None, destination_path=None,
                               writer_name='html',
                               settings_overrides={
                                   'input_encoding': 'unicode',
                                   'doctitle_xform': True,
                                   'initial_header_level': 1,
                               })['body']
    except:
        if settings.DEBUG:
            raise
        parsed = docstring
    return mark_safe(parsed)
