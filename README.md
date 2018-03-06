
## Installation

```
sudo pip3 install djbrut
```

## Usage

```python
from django.http import HttpResponse
from djbrut import Attempt

def some_view(request):
    attempt = Attempt('some rule type name', request)
    # check
    if not attempt.check():
        # error
        return HttpResponse(attempt.error)
    # success
    ...
```
