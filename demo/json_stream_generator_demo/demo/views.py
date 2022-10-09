from time import sleep, time

from django.http import StreamingHttpResponse
from json_stream_generator import json_generator
from json_stream_generator.rest_framework.mixins import StreamingListModelMixin
from rest_framework import viewsets
from rest_framework.response import Response

from . import models, serializers


class DemoViewSet(StreamingListModelMixin, viewsets.ModelViewSet):
    queryset = models.Demo.objects.all()
    serializer_class = serializers.DemoSerializer


class InfiniteDemoViewSet(StreamingListModelMixin, viewsets.ModelViewSet):
    queryset = models.Demo.objects.all()
    serializer_class = serializers.DemoSerializer

    def get_queryset(self):
        while True:
            yield from super().get_queryset()
            sleep(1)


def demo_view(request):
    def get_data():
        for i in range(100):
            yield {"number": i, "timestamp": time()}
            sleep(1)

    return StreamingHttpResponse(
        json_generator(get_data()),
        content_type="application/json",
    )
