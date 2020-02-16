from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


# Create your models here.
class SalesReport(models.Model):
    month = models.IntegerField(validators=[MinValueValidator(1),
                                            MaxValueValidator(12)])
    sales = models.FloatField()
    product = models.CharField(max_length=25)


class SalesHistory(models.Model):
    bookstore = models.CharField(max_length=20)
    sale_qty = models.IntegerField()
    city = models.CharField(max_length=50)
    sale_date = models.DateTimeField(default=False)
    price = models.DecimalField(max_digits=5, decimal_places=2)
