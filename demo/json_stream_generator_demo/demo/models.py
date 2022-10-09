import random
import string
from email.policy import default

from django.db import models


def default_number():
    return random.random()


def default_text():
    return "".join(random.choices(population=string.ascii_letters, k=16))


class Demo(models.Model):
    number = models.FloatField(default=default_number)
    text = models.CharField(max_length=16, default=default_text)
