from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class Manufacturer(models.Model):
    name = models.CharField(max_length=120)
    country = models.CharField(max_length=120)

    def __str__(self):
        return self.name


class Client(AbstractUser):
    is_seller = models.BooleanField(default=False, )

    def save(
        self,
        *args,
        **kwargs,
    ):
        self.is_seller = self.is_seller is not False

        super().save(*args, **kwargs)


class Seller(models.Model):
    client = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    seller_license = models.CharField(max_length=120, unique=True)
    license_expiration_date = models.DateField()

    def __str__(self):
        return self.client.username


class Car(models.Model):
    model = models.CharField(max_length=120)
    year = models.IntegerField()
    mileage = models.IntegerField()
    price = models.IntegerField()
    comment = models.CharField(max_length=255, blank=True, null=True)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, related_name="cars")
    owner = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name="cars")

    def __str__(self):
        return self.model
