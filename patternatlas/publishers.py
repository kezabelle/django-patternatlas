from nap.publisher import Publisher
from nap.http import NotFound
from .models import Atlas
from .serialiser import PatternSerialiser

class PatternPublisher(Publisher):
    api_name = 'patternatalas'
    serialiser = PatternSerialiser()

    OBJECT_PATTERN = r'.+?\..+?'

    def get_object_list(self):
        return Atlas()

    def get_object(self, object_id):
        if object_id.count('.') != 1:
            raise NotFound()
        app, sep, pattern = object_id.partition('.')
        master_atlas = Atlas()
        pattern_atlas = master_atlas.only_app_pattern(app, pattern)
        if len(pattern_atlas) != 1:
            raise NotFound
        return pattern_atlas[0]
