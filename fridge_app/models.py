from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse


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

class Receipt(models.Model):
    store_name = models.CharField(max_length=30)
    purchase_date = models.DateField('Purchase Date')
    receipt_total = models.DecimalField(
        'Total',
        default=0,
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)],)
    item_list = models.TextField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    url = models.CharField(max_length=200)


    class Meta:
        ordering = ['-purchase_date']

    def __str__(self):
        return f'{self.name}({self.id})'

    def get_absolute_url(self):
        return reverse('receipt_detail', kwargs={'receipt_id': self.id})

class Reminder(models.Model):
    name = models.CharField(max_length=40)
    description = models.TextField(max_length=300, blank=True)
    date = models.DateField()
    time = models.TimeField(
        default='06:00'
    )
    send_to_email = models.EmailField(max_length=70)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task_id = models.CharField(max_length=200, null=True)

    class Meta:
        ordering = ['date']

    def get_absolute_url(self):
        return reverse('reminders_detail', kwargs={'pk': self.id})


class Perishable(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    quantity = models.DecimalField(
        default=1,
        max_digits=3,
        decimal_places=0,
        validators=[MinValueValidator(1)],
    )
    store_name = models.CharField(max_length=50)
    category = models.CharField(
        max_length=1,
        choices=PERISHABLE_CATEGORIES,
    )
    price = models.DecimalField(
        'Total',
        default=0,
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    expiration = models.DateField('Expiration Date')

    reminders = models.ManyToManyField(Reminder)
    receipt = models.ForeignKey(Receipt, on_delete=models.SET_NULL, null=True)

    def get_absolute_url(self):
        return reverse('perishables_detail', kwargs={'pk': self.id})

    def __str__(self):
        return f'{self.name} ({self.id})'

    def get_emoji(self):
        return PERISHABLE_CATEGORIES_EMOJIS[self.category]
