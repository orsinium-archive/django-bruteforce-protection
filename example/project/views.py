from django.http import HttpResponse
from djbrut import Attempt


def index(request):
    attempt = Attempt('index', request)
    # check
    if not attempt.check():
        # error
        return HttpResponse(attempt.error)
    # success
    return HttpResponse('ok')
