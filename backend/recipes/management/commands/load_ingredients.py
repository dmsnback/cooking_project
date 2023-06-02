import csv

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    ''' python3 manage.py load_ingredients '''
    def handle(self, *args, **kwargs):
        file_path = './data/ingredients.csv'
        with open(
            file_path, newline='', encoding='utf-8'
        ) as file:
            reader = csv.reader(file)
            for row in reader:
                status, created = Ingredient.objects.update_or_create(
                    name=row[0],
                    measurement_unit=row[1]
                )
