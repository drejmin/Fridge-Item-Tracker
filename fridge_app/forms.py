from django.forms import ModelForm
from .models import Perishable, Receipt, Reminder


class PerishableForm(ModelForm):
    class Meta:
        model = Perishable
        fields = ['name', 'store_name', 'category',
                  'price', 'expiration', 'receipt', 'reminders']


class ReceiptForm(ModelForm):
    class Meta:
        model = Receipt
        fields = ['store_name', 'purchase_date',
                  'receipt_total', 'item_list']


class ReminderForm(ModelForm):
    class Meta:
        model = Reminder
        fields = ['name', 'description', 'date', 'time', 'send_to_email']
