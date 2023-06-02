from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.db.models import TextChoices


username_validator = UnicodeUsernameValidator()


class UserRole(TextChoices):
    USER = 'user', 'Пользователь'
    ADMIN = 'admin', 'Администратор'


class User(AbstractUser):
    '''Кастоиная модель пользователя.'''

    ROLE_CHOICES = UserRole

    email = models.EmailField(
        'Адрес электронной почты',
        max_length=254,
        blank=True,
        unique=True,
        help_text='Введите адрес электронной почты',
    )
    username = models.CharField(
        'Username',
        max_length=150,
        unique=True,
        help_text='Введите ник пользователя',
        validators=[username_validator]
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
        help_text='Введите имя пользователя',
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        help_text='Введите фамилию пользователя'
    )
    password = models.CharField(
        'Пароль',
        max_length=150,
        help_text='Введите пароль'
    )
    role = models.CharField(
        'Роль пользователя',
        choices=ROLE_CHOICES.choices,
        max_length=10,
        default=ROLE_CHOICES.USER,
        help_text='Выберите роль пользователя'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def __str__(self):
        return self.get_full_name()

    def save(self, *args, **kwargs):
        if self.role == UserRole.ADMIN:
            self.is_staff = True
            self.is_superuser = True
        super().save(*args, **kwargs)

    @property
    def is_admin(self):
        return self.role == UserRole.ADMIN or self.is_superuser


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique follow'
            )
        ]

        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('id',)

    def __str__(self):
        return f'{self.user} подписался на {self.author}'
