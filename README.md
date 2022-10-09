json-stream-generator - serialize json in generator
===

[![tests](https://github.com/wlatanowicz/json-stream-generator/actions/workflows/tests.yml/badge.svg)](https://github.com/wlatanowicz/json-stream-generator/actions/workflows/tests.yml)
[![pypi](https://img.shields.io/pypi/v/json-stream-generator)](https://pypi.org/project/json-stream-generator/)


`json-stream-generator` allows you to serialize object to JSON string and start the output immediately, without waiting for serialization to complete.

It was designed to be used with Django's `StreamingHttpResponse` or similar concept in other web frameworks to allow sending huge json blobs to the client without triggering load balancer's timeout:

```python
from json_stream_generator import json_generator
from django.http import StreamingHttpResponse

def my_view(request):
    # NOTE: No Content-Length header!
    return StreamingHttpResponse(
        json_generator((num for num in range(100_000_000))),
        content_type="application/json",
        headers={"Content-Disposition": 'attachment; filename="somefilename.json"'},
      )
```

`json-stream-generator` comes with built-in support for [Django Rest Framework](https://www.django-rest-framework.org):

```python
from json_stream_generator.rest_framework.mixins import StreamingListModelMixin
from rest_framework import viewsets


class DemoViewSet(StreamingListModelMixin, viewsets.ModelViewSet):
    queryset = MyModel.objects.all()
    serializer_class = MySerializer
```
