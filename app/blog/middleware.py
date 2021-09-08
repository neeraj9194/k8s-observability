from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.models import User


def health(get_response):

    def middleware(request):
        if request.path == "/health":
            # DB check
            try:
                User.objects.all()
                return HttpResponse("Healthy")
            except Exception:
                return HttpResponseBadRequest("Unhealthy")
        return get_response(request)
    return middleware
