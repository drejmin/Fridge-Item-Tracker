from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.urls import reverse

# # Create your models here.

class Receipt(models.Model):
    store_name= models.CharField(max_length=30)
    purchase_date=models.DateField('Purchase Date')
    receipt_total=models.FloatField('Total')
    receipt_image=models.ImageField('Image')
    item_list = models.TextField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-purchase_date']
    
    def __str__(self):
        return f'{self.name}({self.id})'
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'receipt_id': self.id})





    

# class Photo(models.Model):
#     url = models.CharField(max_length=200)
#     cat = models.ForeignKey(Item, on_delete=models.CASCADE)

#     def __str__(self):
#         return f"Photo for item_id: {self.item_id} @{self.url}"