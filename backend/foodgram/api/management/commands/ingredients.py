import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        with open(
            os.path.join(os.path.join(settings.BASE_DIR, 'data'), 'ingredients.json'), 'r'
        ) as file:
            ingredients = json.load(file)
            for ingredient in ingredients:
                Ingredient.objects.create(
                    name=ingredient.get('name'),
                    measurement_unit=ingredient.get('measurement_unit')
                )
