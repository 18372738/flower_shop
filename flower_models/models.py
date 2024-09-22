from django.db import models
from django.core.exceptions import ValidationError
import re

ORDER_CHOICES = (
    ("true", "подтверждение"),
    ("courier", "передан курьеру"),
    ("delivered", "доставлено")
)


class Event(models.Model):
    """События"""
    title = models.CharField("Название события", max_length=200)

    def __str__(self):
        return self.title


class Bouquet(models.Model):
    """Букеты"""
    title = models.CharField("Название букета", max_length=200, unique=True)
    price = models.FloatField("Стоимость", blank=True)
    event = models.ManyToManyField(
        Event,
        verbose_name="Событие",
        related_name="events",
    )
    photo = models.ImageField("Фото")
    description = models.TextField(
        "Описание",
        blank=True
    )
    height = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Высота(см)'
    )
    width = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Ширина(см)'
    )

    def __str__(self):
        return self.title


class Client(models.Model):
    """Клиенты"""
    full_name = models.CharField("ФИО", max_length=200)
    phone = models.CharField('Телефон', max_length=200, unique=True)

    def clean(self):
        if self.phone:
            normalized_phone = re.sub(r'\D', '', self.phone)
            if len(normalized_phone) < 10:
                raise ValidationError("Номер телефона слишком короткий")

            self.phone = normalized_phone

    def save(self, *args, **kwargs):
        self.clean()
        super(Client, self).save(*args, **kwargs)

    def __str__(self):
        return self.full_name


class Order(models.Model):
    """Заказ"""
    client = models.ForeignKey(
        Client,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="clients"
    )
    address = models.CharField("Адрес", max_length=200)
    delivery_date = models.DateTimeField("Дата доставки")
    bouquet = models.ForeignKey(
        Bouquet,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    status = models.CharField(
        verbose_name="Статус",
        choices=ORDER_CHOICES,
        max_length=30,
        default="true",
    )

    def __str__(self):
        return self.client
