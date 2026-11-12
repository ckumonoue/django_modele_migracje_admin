from decimal import Decimal

from django.db import models


class Product(models.Model):
    name = models.CharField("nazwa", max_length=100)
    price = models.DecimalField("cena", max_digits=8, decimal_places=2)
    is_available = models.BooleanField("dostępny", default=True)
    description = models.TextField("opis", blank=True)
    stock = models.PositiveIntegerField("stan magazynowy", default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "produkt"
        verbose_name_plural = "produkty"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def gross_price(self):
        return (self.price * Decimal("1.23")).quantize(Decimal("0.01"))
