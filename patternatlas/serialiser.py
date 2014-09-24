from nap.serialiser import Serialiser
try:
    from nap.serialiser.fields import StringField
except ImportError:  # old version of nap ... damn FB and his restructuring.
    from nap.fields import StringField


class PatternSerialiser(Serialiser):
    pattern = StringField(attribute='name')
    pattern_name = StringField(attribute='callable_name')
    content = StringField(attribute="content")
    description = StringField(attribute="_description")
    description_html = StringField(attribute="description")
    module = StringField(attribute="module")
    module_name = StringField(attribute="module_name")
    module_description = StringField(attribute="_module_description")
    module_description_html = StringField(attribute="module_description")
    module_url = StringField(attribute="get_parent_url")
    url = StringField(attribute="get_absolute_url")
