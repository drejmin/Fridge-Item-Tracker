from django.forms import ModelForm
from .models import Perishable

class PerishableForm(ModelForm):
  class Meta:
      model = Perishable
      fields = ['name', 'store_name', 'category', 'price', 'expiration']