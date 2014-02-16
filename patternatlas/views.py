from django.shortcuts import render
from django.http import Http404
from .models import Atlas


def root(request):
    atlas = Atlas(request=request)
    context = {
        'atlas': atlas,
        'atlas_assets': atlas.assets(),
        'kwargs': {
            'app_label': None,
            'pattern_name': None,
        },
    }
    return render(request, 'patternatlas/root.html', context)


def app(request, app_label):
    master_atlas = Atlas(request=request)
    app_atlas = master_atlas.only_app(app_label)
    if len(app_atlas) == 0:
        raise Http404('Atlas contained no patterns')
    context = {
        'atlas': master_atlas,
        'app_atlas': app_atlas,
        'atlas_assets': app_atlas.assets(),
        'kwargs': {
            'app_label': app_label,
            'pattern_name': None,
        },
    }
    templates = ('patternatlas/{0}/app_label.html'.format(app_label),
                 'patternatlas/app_label.html')
    return render(request, templates, context)


def pattern(request, app_label, pattern):
    master_atlas = Atlas(request=request)
    app_atlas = master_atlas.only_app(app_label)
    if len(app_atlas) == 0:
        raise Http404('Atlas contained no patterns')
    pattern_atlas = app_atlas.only_app_pattern(app_label, pattern)
    if len(pattern_atlas) == 0:
        raise Http404('Pattern not found in requested atlas')
    context = {
        'atlas': master_atlas,
        'app_atlas': app_atlas,
        'pattern_atlas': pattern_atlas,
        'atlas_assets': pattern_atlas.assets(),
        'kwargs': {
            'app_label': app_label,
            'pattern_name': pattern,
        },
    }
    templates = ('patternatlas/{0}/{1}/pattern.html'.format(app_label,
                                                            pattern),
                 'patternatlas/{0}/pattern.html'.format(app_label),
                 'patternatlas/pattern.html')
    return render(request, templates, context)
