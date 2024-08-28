from django.db import models
from django.core.validators import MinLengthValidator

# Create your models here.
class Auto(models.Model):
    nickname = models.CharField(max_length=100)
    mileage = models.PositiveIntegerField()
    comments = models.CharField(max_length = 300)
    make = models.ForeignKey('Make', on_delete = models.CASCADE, null=False)

    def __str__(self):
        return self.nickname

class Make(models.Model):
    name = models.CharField(max_length=200,
    help_text='Enter a make(eg. Ford)',
    validators = [MinLengthValidator(3, "Must be greater than 2 characters")]
    )

    def __str__(self):
        return self.name