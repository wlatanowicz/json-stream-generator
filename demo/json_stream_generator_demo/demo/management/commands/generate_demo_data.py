from django.core.management.base import BaseCommand

from ... import models


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--count", type=int, help="Number of records to generate", default=1000
        )

    def handle(self, *args, **options):
        for _ in range(options["count"]):
            models.Demo().save()
