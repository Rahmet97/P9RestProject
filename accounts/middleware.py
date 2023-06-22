from django.http import HttpResponseNotFound


class BlockAdminMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        ip_address = '172.25.0.1'

        if request.path.startswith('/admin') and request.META.get('REMOTE_ADDR') != ip_address:
            return HttpResponseNotFound()
        return self.get_response(request)