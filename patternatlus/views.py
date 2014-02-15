from django.shortcuts import render
from .models import Atlus


def root(request):
    atlus = Atlus(request=request)
    context = {
        'atlus': atlus,
        'atlus_assets': atlus.assets(),
    }
    return render(request, 'patternatlus/root.html', context)


def app(request, app_label):
    master_atlus = Atlus(request=request)
    app_atlus = master_atlus.only_app(app_label)
    context = {
        'atlus': master_atlus,
        'app_atlus': app_atlus,
        'atlus_assets': app_atlus.assets(),
    }
    templates = ('patternatlus/{0}/app_label.html'.format(app_label),
                 'patternatlus/app_label.html')
    return render(request, templates, context)


def pattern(request, app_label, pattern):
    master_atlus = Atlus(request=request)
    pattern_atlus = master_atlus.only_app_pattern(app_label, pattern)
    context = {
        'atlus': master_atlus,
        'app_atlus': master_atlus.only_app(app_label),
        'pattern_atlus': pattern_atlus,
        'atlus_assets': pattern_atlus.assets(),
    }
    templates = ('patternatlus/{0}/{1}/pattern.html'.format(app_label,
                                                            pattern),
                 'patternatlus/{0}/pattern.html'.format(app_label),
                 'patternatlus/pattern.html')
    return render(request, templates, context)
