import os
import uuid
import boto3
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from .models import Perishable, Receipt, Reminder

# Create your views here.
def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('/')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

def home(request):
  return render(request, 'home.html')

# Views for Perishables ----------------------------------------------------------

class PerishableCreate(LoginRequiredMixin, CreateView):
  model = Perishable
  fields = ['name','quantity', 'category', 'store_name', 'price', 'expiration']
  
  def form_valid(self,form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class PerishableUpdate(LoginRequiredMixin, UpdateView):
  model = Perishable
  fields = ['name','quantity','category', 'store_name', 'price', 'expiration']
  success_url = '/perishables'

class PerishableDelete(LoginRequiredMixin, DeleteView):
  model = Perishable
  success_url = '/perishables'

class PerishableList(ListView):
  model = Perishable

class PerishableDetail(DetailView):
  model = Perishable
  fields = ['name','quantity', 'category', 'store_name', 'price', 'expiration']
  
# Views for Receipt ----------------------------------------------------------

@login_required
def receipt_index(request):
  receipts = Receipt.objects.filter(user=request.user)
  return render(request, 'receipt/index.html',{
    'receipts': receipts
  })

@login_required
def receipt_detail(request, receipt_id):
  receipt = Receipt.objects.get(id=receipt_id)
  return render(request, 'receipt/details.html',{
    'receipt': receipt
  })

class ReceiptCreate(LoginRequiredMixin, CreateView):
  model = Receipt
  fields = ['store_name','purchase_date','receipt_total','receipt_image','item_list']

  def form_valid(self,form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class ReceiptUpdate(LoginRequiredMixin, UpdateView):
  model = Receipt
  fields = ['store_name','purchase_date','receipt_total','receipt_image','item_list']

class ReceiptDelete(LoginRequiredMixin, DeleteView):
  model = Receipt
  success_url = '/receipt'

# Views for Reminders ------------------------------------------------------------

class ReminderList(LoginRequiredMixin, ListView):
  model = Reminder

class ReminderDetail(LoginRequiredMixin, DetailView):
  model = Reminder

class ReminderCreate(LoginRequiredMixin, CreateView):
  model = Reminder
  fields = ['name', 'type', 'date', 'remind_days_prio_by', 'remind_time', 'send_to_email', 'time_zone']
  
  def form_valid(self, form):
    # Assign the logged in user (self.request.user)
    form.instance.user = self.request.user  # form.instance is the cat
    # Let the CreateView do its job as usual
    return super().form_valid(form)

class ReminderUpdate(LoginRequiredMixin, UpdateView):
  model = Reminder
  fields = ['name', 'type', 'date', 'remind_days_prio_by', 'remind_time', 'send_to_email', 'time_zone']

class ReminderDelete(LoginRequiredMixin, DeleteView):
  model = Reminder
  success_url = '/reminders'

