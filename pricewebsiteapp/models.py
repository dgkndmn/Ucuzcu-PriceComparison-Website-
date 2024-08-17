from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField()
    link = models.URLField()
    site = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} - {self.price} - {self.image_url} - {self.link} - {self.site}"