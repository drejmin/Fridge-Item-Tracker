from django.forms import ModelForm
from .models import Perishable, Receipt

class PerishableForm(ModelForm):
  class Meta:
      model = Perishable
      fields = ['name', 'store_name', 'category', 'price', 'expiration']

class ReceiptForm(ModelForm):
    class Meta:
        model = Receipt
        fields = ['store_name','purchase_date','receipt_total','receipt_image','item_list']

