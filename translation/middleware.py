from django.conf import settings
from django.middleware.locale import LocaleMiddleware
from django.core.urlresolvers import is_valid_path
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.utils.cache import patch_vary_headers
from django.utils import translation

from .utils import get_language, supported_languages_for_path

class LocationSpecificLocaleMiddleware(LocaleMiddleware):
    def process_request(self, request):
        check_path = self.is_language_prefix_patterns_used()
        translation.activate(get_language(request, check_path))
        request.LANGUAGE_CODE = translation.get_language()

    def process_response(self, request, response):
        language = translation.get_language()
        supported_languages = supported_languages_for_path(request.path_info)['languages']
        language_from_path = translation.get_language_from_path(
            request.path_info, supported=supported_languages
        )

        if not language_from_path and language not in supported_languages:
            return HttpResponseNotFound()

        if (response.status_code == 404 and not language_from_path
            and self.is_language_prefix_patterns_used()):
            urlconf = getattr(request, 'urlconf', None)
            language_path = '/%s%s' % (language, request.path_info)
            path_valid = is_valid_path(language_path, urlconf)
            if (not path_valid and settings.APPEND_SLASH
                and not language_path.endswith('/')):
                path_valid = is_valid_path("%s/" % language_path, urlconf)

            if path_valid:
                language_url = "%s://%s/%s%s" % (
                    'https' if request.is_secure() else 'http',
                    request.get_host(), language, request.get_full_path())
                return HttpResponseRedirect(language_url)

        if not (self.is_language_prefix_patterns_used()
                and language_from_path):
            patch_vary_headers(response, ('Accept-Language',))
        if 'Content-Language' not in response:
            response['Content-Language'] = language
        return response
