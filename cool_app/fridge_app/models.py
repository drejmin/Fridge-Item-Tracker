from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date
from django.urls import reverse
from django.forms import DateInput

# Perishable Constants
PERISHABLE_CATEGORIES = (
    ("B", "Bakery 🍞"),
    ("D", "Dairy 🥛"),
    ("E", "Eggs 🐔"),
    ("M", "Meat and Seafood 🍖"),
    ("P", "Produce 🥦"),
    ("O", "Other 🍕"),
)

PERISHABLE_CATEGORIES_EMOJIS = {
    'B': '🍞',
    'D': '🥛',
    'E': '🐔',
    'M': '🍖',
    'P': '🥦',
    'O': '🍕',
}


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

class Receipt(models.Model):
    store_name= models.CharField(max_length=30)
    purchase_date=models.DateField('Purchase Date')
    receipt_total=models.DecimalField(
        'Total',
        default=0,
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        )
    receipt_image=models.ImageField('Image', blank = True)
    item_list = models.TextField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-purchase_date']
    
    def __str__(self):
        return f'{self.name}({self.id})'
    
    def get_absolute_url(self):
        return reverse('receipt_detail', kwargs={'receipt_id': self.id})
    


class Reminder(models.Model):
    name = models.CharField(max_length=40)
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
                                MinValueValidator(0),
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


class Perishable(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    quantity = models.DecimalField(
        default=1,
        max_digits= 3,
        decimal_places=0,
        validators=[MinValueValidator(1)],
    )
    store_name = models.CharField(max_length=50)
    category = models.CharField(
        max_length=1,
        choices= PERISHABLE_CATEGORIES, 
    )
    price = models.DecimalField(
        'Total',
        default=0,
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        )
    expiration= models.DateField('Expiration Date')

    reminders = models.ManyToManyField(Reminder)
    receipt = models.ForeignKey(Receipt, on_delete=models.SET_NULL, null=True)


    def get_absolute_url(self):
        return reverse('perishables_detail', kwargs={'pk': self.id})
    
    def __str__(self):
        return f'{self.name} ({self.id})'
    
    def get_emoji(self):
        return PERISHABLE_CATEGORIES_EMOJIS[self.category]
