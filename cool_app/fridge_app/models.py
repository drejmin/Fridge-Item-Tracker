from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.urls import reverse


# # Create your models here.
PERISHABLE_CATEGORIES = (
            ('B', 'Bakery'),
            ('D', 'Dairy'),
            ('E', 'Eggs'),
            ('M', 'Meat and Seafood'),
            ('P', 'Produce'),
            ('O', 'Other'),
)

class Receipt(models.Model):
    store_name= models.CharField(max_length=30)
    purchase_date=models.DateField('Purchase Date')
    receipt_total=models.FloatField('Total')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-purchase_date']

class Perishable(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    store_name = models.CharField(max_length=50)
    category = models.CharField(
        max_length=2,
        choices=PERISHABLE_CATEGORIES, 
            default='P'
    )
    price = models.FloatField('Item Price')
    expiration= models.DateField('Expiration Date')

    def get_absolute_url(self):
        return reverse('perishables_detail', kwargs={'pk': self.id})
    
    def __str__(self):
        return f'{self.name} ({self.id})'
    
    
    




    

# class Photo(models.Model):
#     url = models.CharField(max_length=200)
#     cat = models.ForeignKey(Item, on_delete=models.CASCADE)

#     def __str__(self):
#         return f"Photo for item_id: {self.item_id} @{self.url}"