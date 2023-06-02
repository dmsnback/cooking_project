from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models


User = get_user_model()


class Tag(models.Model):
    '''Модель тегов'''
    name = models.CharField(
        'Название тега',
        max_length=200,
        help_text='Напишите название тэга'
    )
    color = models.CharField(
        'Цветовой HEX-код',
        max_length=7,
        validators=[
            RegexValidator(
                regex='^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})',
                message='Значение не является цветом в формате HEX'
            )
        ],
        help_text='Напишите Цветовой HEX-код в формате #ffffff',
    )
    slug = models.SlugField(
        'URL тега',
        max_length=200,
        unique=True,
        help_text='Напишите URL для тега'
    )

    class Meta:
        verbose_name = 'Тэг',
        verbose_name_plural = 'Тэги'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    '''Модель ингредиента'''
    name = models.CharField(
        'Название ингредиента',
        max_length=200,
        help_text='Напишите название ингредиента'
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=200,
        help_text='Напишите единицу измерения'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Recipe(models.Model):
    '''Модель рецепта'''
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe',
        verbose_name='Список ингредиентов',
        related_name='recipes',
        help_text='Выберите или добавте ингридиенты'

    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Список тэгов',
        related_name='recipes',
        help_text='Выберите или добавте тэги'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор рецепта',
        on_delete=models.SET_NULL,
        related_name='recipes',
        null=True,
        help_text='Выберите автора рецепта'

    )
    image = models.ImageField(
        'Изображение рецепта',
        upload_to='recipes/',
        help_text='Загрузите фото готового блюда'
    )
    name = models.CharField(
        'Название блюда',
        max_length=200,
        help_text='Напишите название блюда'
    )

    text = models.TextField(
        'Описание рецепта',
        help_text='Напишите рецепт'
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления(минут)',
        help_text='Выберите время приготовления в минутах',
        validators=[
            MinValueValidator(
                limit_value=1,
                message='Время должно быть больше нуля.'
            )
        ]
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('name',)

    def __str__(self):
        return f'{self.name}, {self.cooking_time}'


class IngredientRecipe(models.Model):
    '''Модель ингредиентов в рецепте'''
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredient_list',
        verbose_name='Рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент'
    )
    amount = models.PositiveSmallIntegerField(
        'Количество в рецепте',
        validators=[
            MinValueValidator(
                limit_value=1,
                message='Количество должно быть больше нуля.'
            )
        ]
    )

    class Meta:

        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'

    def __str__(self):
        return (
            f'{self.ingredient.name} {self.ingredient.measurement_unit}'
            f'{self.amount}'
        )


class Favorite(models.Model):
    '''Модель избранного'''
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique favorite'
            )
        ]

    def __str__(self):
        return f'{self.user} добавил {self.recipe} в избранное'


class ShoppingCart(models.Model):
    '''Модель списка покупок'''
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique shopping cart'
            )
        ]

    def __str__(self):
        return f'{self.user} добавил {self.recipe} в список покупок'
