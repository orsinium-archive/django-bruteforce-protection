Usage
-----

.. code:: python

    from django.http import HttpResponse
    from djbrut import Attempt

    def some_view(request):
        attempt = Attempt(request)
        # check
        if not attempt.check():
            # error
            return HttpResponse(attempt.error)
        # success
        ...
