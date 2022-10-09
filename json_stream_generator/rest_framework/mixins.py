import rest_framework
from django.db.models.query import QuerySet
from django.http import StreamingHttpResponse

from .. import json_generator


class StreamingListModelMixin:
    ensure_queryset_iterator = True

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            data = self.get_serialization_generator(page)
            return self.get_paginated_response(data)

        data = self.get_serialization_generator(queryset)
        return self.get_streaming_json_response(data)

    def get_paginated_response(self, data):
        assert self.paginator is not None
        original_response = self.paginator.get_paginated_response(data)
        wrapped_data = original_response.data
        return self.get_streaming_json_response(wrapped_data)

    def get_serialization_generator(self, queryset):
        return (self.get_serializer(item, many=False).data for item in queryset)

    def get_streaming_json_response(self, data):
        depth = 2 if isinstance(data, dict) else 1
        json_stream = json_generator(data, depth=depth)
        return StreamingHttpResponse(
            json_stream,
            content_type="application/json",
        )

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.ensure_queryset_iterator and isinstance(queryset, QuerySet):
            return super().get_queryset().iterator()
        return queryset
