from django.contrib.auth.models import AbstractUser
from django.db import models

from datetime import date
from slugify import slugify

class CustomUser(AbstractUser):
    """
    Модель кастомного пользователя, расширяющая стандартную модель Django User.
    Добавлены поля для описания и даты создания профиля.
    """

    created_at = models.DateField(default=date.today)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username

    @classmethod
    def username_exists(cls, username):
        return cls.objects.filter(username=username).exists()

    @classmethod
    def email_exists(cls, email):
        return cls.objects.filter(email=email).exists()

class Gift(models.Model):
    """Модель подарка. Содержит информацию о названии, цене, описании, URL и статусе резервации."""

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    url = models.URLField()
    reserved = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Переопределенный метод сохранения модели. Генерирует уникальный слаг на основе названия подарка."""

        if not self.slug:
            original_slug = slugify(self.name)
            self.slug = original_slug
            counter = 1
            while Gift.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

class Wishlist(models.Model):
    """Модель списка желаний. Связывает пользователя с подарками и содержит событие, для которого создается список."""

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    products = models.ManyToManyField(Gift, related_name='products')
    event = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    def __str__(self):
        return f'{self.user}`s wishlist {self.event}'

    def save(self, *args, **kwargs):
        if not self.slug:
            original_slug = f'{slugify(str(self.user))}-{slugify(str(self.event))}'
            self.slug = original_slug
            counter = 1
            while Gift.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)