from django.shortcuts import render
from .models import Atlas


def root(request):
    atlas = Atlas(request=request)
    context = {
        'atlas': atlas,
        'atlas_assets': atlas.assets(),
    }
    return render(request, 'patternatlas/root.html', context)


def app(request, app_label):
    master_atlas = Atlas(request=request)
    app_atlas = master_atlas.only_app(app_label)
    context = {
        'atlas': master_atlas,
        'app_atlas': app_atlas,
        'atlas_assets': app_atlas.assets(),
    }
    templates = ('patternatlas/{0}/app_label.html'.format(app_label),
                 'patternatlas/app_label.html')
    return render(request, templates, context)


def pattern(request, app_label, pattern):
    master_atlas = Atlas(request=request)
    pattern_atlas = master_atlas.only_app_pattern(app_label, pattern)
    context = {
        'atlas': master_atlas,
        'app_atlas': master_atlas.only_app(app_label),
        'pattern_atlas': pattern_atlas,
        'atlas_assets': pattern_atlas.assets(),
    }
    templates = ('patternatlas/{0}/{1}/pattern.html'.format(app_label,
                                                            pattern),
                 'patternatlas/{0}/pattern.html'.format(app_label),
                 'patternatlas/pattern.html')
    return render(request, templates, context)
