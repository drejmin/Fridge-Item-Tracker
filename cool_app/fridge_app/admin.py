from django.contrib import admin
from .models import Perishable, Receipt, Reminder

admin.site.register(Perishable)
admin.site.register(Reminder)
admin.site.register(Receipt)