from django.contrib import admin
from .models import Receipt, Reminder

# Register your models here.
admin.site.register(Reminder)
admin.site.register(Receipt)
