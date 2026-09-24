from django.utils import translation


class AdminEnglishMiddleware:
    """
    يجعل واجهة Django Admin باللغة الإنجليزية فقط،
    دون التأثير على لغة الموقع.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.path.startswith('/admin/'):
            with translation.override('en'):
                return self.get_response(request)

        return self.get_response(request)