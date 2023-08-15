from django.db import models
from django.contrib.auth.models import User
from datetime import date

# Create your models here.
class Photo(models.Model):
    url = models.CharField(max_length=200)
    cat = models.ForeignKey(Item, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for item_id: {self.item_id} @{self.url}"