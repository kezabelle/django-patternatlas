from django.shortcuts import render
from .models import Atlus


def root(request):
    context = {
        'atlus': Atlus(request=request),
    }
    return render(request, 'patternatlus/root.html', context)


def app(request, app_label):
    master_atlus = Atlus(request=request)
    context = {
        'atlus': master_atlus,
        'app_atlus': master_atlus.only_app(app_label),
    }
    templates = ('patternatlus/{0}/app_label.html'.format(app_label),
                 'patternatlus/app_label.html')
    return render(request, templates, context)


def pattern(request, app_label, pattern):
    master_atlus = Atlus(request=request)
    context = {
        'atlus': master_atlus,
        'app_atlus': master_atlus.only_app(app_label),
        'pattern_atlus': master_atlus.only_app_pattern(app_label, pattern),
    }
    templates = ('patternatlus/{0}/{1}/pattern.html'.format(app_label,
                                                            pattern),
                 'patternatlus/{0}/pattern.html'.format(app_label),
                 'patternatlus/pattern.html')
    return render(request, templates, context)
