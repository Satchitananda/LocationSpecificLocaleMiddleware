from django.conf import settings
from django.utils import translation
from django.utils.datastructures import SortedDict

def startswithany(to_check, parts):
    for p in parts:
        if to_check.startswith(p):
            return p
    return None

def supported_languages_for_path(path):
    language_from_path = translation.get_language_from_path(
        path, supported=SortedDict(settings.LANGUAGES)
    )

    if language_from_path:
        path = path.replace('/%s' % language_from_path, '', 1)

    res = startswithany(path, settings.LOCATION_LANGUAGES_MAPPING.keys())
    if res:
        return {
            'languages': list(settings.LOCATION_LANGUAGES_MAPPING[res].get('languages', [])),
            'fallback': settings.LOCATION_LANGUAGES_MAPPING[res].get('fallback', settings.LANGUAGE_CODE)
        }

    # Falling to site language
    return {
        'languages': [settings.LANGUAGE_CODE],
        'fallback': settings.LANGUAGE_CODE
    }

def get_language(request, check_path=True):
    language = translation.get_language_from_request(
        request, check_path=check_path)
    language_from_path = translation.get_language_from_path(
        request.path_info, supported=SortedDict(settings.LANGUAGES)
    )

    # If language detected by path, just return it
    if language_from_path:
        return language_from_path

    supported_languages = supported_languages_for_path(request.path_info)
    if language in supported_languages['languages']:
        return language
    else:
        return supported_languages['fallback']