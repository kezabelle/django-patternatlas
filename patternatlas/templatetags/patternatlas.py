from django import template
from django.utils.safestring import mark_safe
from django.contrib.staticfiles.storage import staticfiles_storage

register = template.Library()

css_template = '<link rel="stylesheet" type="text/css" href="{path}">'
js_template = '<script type="text/javascript" src="{path}""></script>'


@register.filter
def fix_raw_asset(value):
    if value.endswith('.css'):
        value = css_template.format(path=staticfiles_storage.url(value))
    elif value.endswith('.js'):
        value = js_template.format(path=staticfiles_storage.url(value))
    return mark_safe(value)


@register.filter
def fix_raw_assets(value):
    final_assets = []
    for asset in value:
        final_assets.append(fix_raw_asset(asset))
    return "\n".join(final_assets)
