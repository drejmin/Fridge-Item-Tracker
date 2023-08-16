from django.forms import ModelForm
from .models import Receipt

class ReceiptForm(ModelForm):
    class Meta:
        model = Receipt
        fields = ['store_name','purchase_date','receipt_total','receipt_image','item_list']
