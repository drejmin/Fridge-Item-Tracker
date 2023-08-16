from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from datetime import date
from django.urls import reverse

# Reminder Constants
REMINDER_TYPES = (
    ("D", "Day"),
    ("E", "Expiration"),
    ("G", "Garbage"),
)

REMINDER_TIMES = (
    ("M", "Morning"),
    ("L", "Noon"),
    ("A", "Afternoon"),
    ("E", "Evening"),
    ("N", "Night"),
)

TIME_ZONES = (
    ("PT", "Pacific Time"),
    ("MT", "Mountain Time"),
    ("CT", "Central Time"),
    ("ET", "Eastern Time"),
)

# # Create your models here.
class Receipt(models.Model):
    store_name = models.CharField(max_length=30)
    purchase_date = models.DateField('Purchase Date')
    receipt_total = models.FloatField('Total')
    receipt_image = models.ImageField('Image')
    item_list = models.TextField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-purchase_date']
    
    def __str__(self):
        return f'{self.name}({self.id})'
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'receipt_id': self.id})

class Reminder(models.Model):
    name = models.CharField(max_length=30)
    type = models.CharField(
            max_length = 1,
            choices = REMINDER_TYPES,
            # TODO: meet with team to decide default reminder
            default = 'D'
        )
    date = models.DateTimeField('Reminder Date')
    remind_days_prio_by =  models.IntegerField(
                            default = 0,
                            validators=[
                                MaxValueValidator(6),
                            ],
                        )
    remind_time = models.CharField(
                    max_length = 1,
                    choices = REMINDER_TIMES,
                    default = 'M'
                    )
    send_to_email = models.EmailField(max_length = 70)
    time_zone = models.CharField(
                    max_length = 2,
                    choices = TIME_ZONES,
                    default = 'CT',
                    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['date']

    def get_absolute_url(self):
        return reverse('reminders_detail', kwargs={'pk': self.id})




    

# class Photo(models.Model):
#     url = models.CharField(max_length=200)
#     cat = models.ForeignKey(Item, on_delete=models.CASCADE)

#     def __str__(self):
#         return f"Photo for item_id: {self.item_id} @{self.url}"