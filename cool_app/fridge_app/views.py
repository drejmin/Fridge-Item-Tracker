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
from .models import Perishable, Receipt, Reminder, Photo
from datetime import datetime
from .forms import ReminderForm


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
    fields = ['name', 'quantity', 'category',
              'store_name', 'price', 'expiration']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PerishableUpdate(LoginRequiredMixin, UpdateView):
    model = Perishable
    fields = ['name', 'quantity', 'category',
              'store_name', 'price', 'expiration']
    success_url = '/perishables'


class PerishableDelete(LoginRequiredMixin, DeleteView):
    model = Perishable
    success_url = '/perishables'


class PerishableList(ListView):
    model = Perishable


class PerishableDetail(DetailView):
    model = Perishable
    fields = ['name', 'quantity', 'category',
              'store_name', 'price', 'expiration']
    form = ReminderForm()
    # reminder_form = ReminderForm()
    # return render(request, 'fridge_app/perishable_detail.html',
    #  {'name': name, 'description': description, 'date': date, 'time': time, 'send_to_email': send_to_email})

    #  reminder_form = ReminderForm()
    #   return render(request, 'perishables/detail.html', {
    #     'perishable': perishable, 'reminder_form': reminder_form,
    #     })


# Views for Receipt ----------------------------------------------------------


@login_required
def receipt_index(request):
    receipts = Receipt.objects.filter(user=request.user)
    return render(request, 'receipt/index.html', {
        'receipts': receipts
    })


@login_required
def receipt_detail(request, receipt_id):
    receipt = Receipt.objects.get(id=receipt_id)
    return render(request, 'receipt/details.html', {
        'receipt': receipt
    })


class ReceiptCreate(LoginRequiredMixin, CreateView):
  model = Receipt
  fields = ['store_name','purchase_date','receipt_image','receipt_total','item_list']

  def form_valid(self,form):
    form.instance.user = self.request.user
    return super().form_valid(form)
  

class ReceiptUpdate(LoginRequiredMixin, UpdateView):
  model = Receipt
  fields = ['store_name','purchase_date','receipt_image','receipt_total','item_list']


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
    fields = ['name', 'description', 'date', 'time', 'send_to_email']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ReminderUpdate(LoginRequiredMixin, UpdateView):
    model = Reminder
    fields = ['name', 'description', 'date', 'time', 'send_to_email']


class ReminderDelete(LoginRequiredMixin, DeleteView):
    model = Reminder
    success_url = '/reminders'

# Adding a reminder via modal ----------------------------------------------------------

def add_reminder(request, pk):
    if request.method == 'POST':
        form = ReminderForm(request.POST)
        try:
            if form.is_valid():
                form.save()
                return redirect('/perishables/')  # Redirect to a success page
        except Exception as e:

            pass
    else:
        form = ReminderForm()

    return redirect('perishables_detail', pk=pk)
    # return render(request, 'fridge_app/perishable_detail.html/',
    #               {'form': form})


# def add_reminder(request, perishable_id):
#     # creates a ModelForm instance using the data that was submitted in the form
#     form = ReminderForm(request.POST)
# # validate the form
#     if form.is_valid():
#         new_reminder = form.save(commit=False)
#         new_reminder.perishable_id = perishable_id
#         new_reminder.save()
#         return redirect('/perishables_detail/', perishable_id=perishable_id)

# def add_reminder(request, perishable_id):
#     if request.method == 'POST':
#         form = ReminderForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('/perishables/')  # Redirect to a success page
#     else:
#         form = ReminderForm()

#     # return render(request, 'perishable_detail.html', {'form': form})
#     return render(request, '/perishable_detail.html/',  {'perishable_id': perishable_id, 'form': form})

#------photo upload for receipts----------------------------------------------------------------------------------
@login_required
def add_receipt(request, receipt_id):
  receipt_image = request.FILES.get('photo-file', None)
  if receipt_image:
      s3 = boto3.client('s3')
      key = uuid.uuid4().hex[:6] + receipt_image.name[receipt_image.name.rfind('.'):]
  try:
        bucket = os.environ['S3_BUCKET']
        s3.upload_fileobj(receipt_image, bucket, key)
        url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
        Photo.objects.create(url=url, receipt_id=receipt_id)
  except Exception as e:
        print('An error occurred uploading file to S3')
        print(e)
  return redirect('receipt_detail', receipt_id=receipt_id)




