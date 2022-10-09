from rest_framework import serializers

from . import models


class DemoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Demo
        fields = "__all__"
