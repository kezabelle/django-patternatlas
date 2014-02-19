#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from setuptools import setup, find_packages
import warnings

warnings.filterwarnings("ignore", '.+', PendingDeprecationWarning,
                        'django\.test\..*')
warnings.filterwarnings("ignore", '.+', PendingDeprecationWarning,
                        'django\.template\.base')

try:
    from setuptest import test
    test_config = {
        'cmdclass': {'test': test}
    }
except ImportError:
    test_config = {
        'tests_require': (
            'django-setuptest',
            ),
        'test_suite': 'setuptest.setuptest.SetupTestSuite'
    }
    for argument in ('--failfast', '--autoreload', '--label'):
        if argument in sys.argv:
            sys.argv.remove(argument)


HERE = os.path.abspath(os.path.dirname(__file__))


def make_readme(root_path):
    FILES = ('README.rst', 'LICENSE', 'CHANGELOG', 'CONTRIBUTORS')
    for filename in FILES:
        filepath = os.path.realpath(os.path.join(HERE, filename))
        if os.path.isfile(filepath):
            with open(filepath, mode='r') as f:
                yield f.read()

LONG_DESCRIPTION = "\r\n\r\n----\r\n\r\n".join(make_readme(HERE))

setup(
    name="django-patternatlas",
    version="0.2.1",
    packages=find_packages(),
    install_requires=[
        'Django>=1.4.0',
        'docutils>=0.11',
        'Sphinx>=1.2.1',
        'django-pygments>=0.1',
    ],
    author="Keryn Knight",
    author_email='python-package@kerynknight.com',
    description="",
    long_description=LONG_DESCRIPTION,
    keywords="django styleguide",
    license="BSD License",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Natural Language :: English',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
        'Topic :: Text Processing :: Markup :: HTML',
        'License :: OSI Approved :: BSD License',
    ],
    platforms=['OS Independent'],
    **test_config
)
