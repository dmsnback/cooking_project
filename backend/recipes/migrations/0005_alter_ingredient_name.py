# Generated by Django 3.2.19 on 2023-06-04 00:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_ingredientrecipe_unique_recipe_ingredient'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='name',
            field=models.CharField(help_text='Напишите название ингредиента', max_length=200, null=True, verbose_name='Название ингредиента'),
        ),
    ]