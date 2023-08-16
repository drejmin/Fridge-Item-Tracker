import os
import uuid
import boto3
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Perishable


# Create your views here.
def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

def home(request):
  return render(request, 'home.html')

class PerishableCreate(LoginRequiredMixin, CreateView):
  model = Perishable
  fields = ['name', 'category', 'store_name', 'price', 'expiration']

  def form_valid(self,form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class PerishableUpdate(LoginRequiredMixin, UpdateView):
  model = Perishable
  fields = ['name', 'category', 'store_name', 'price', 'expiration']
  success_url = '/perishables'

class PerishableDelete(LoginRequiredMixin, DeleteView):
  model = Perishable
  success_url = '/perishables'

class PerishableList(ListView):
  model = Perishable

class PerishableDetail(DetailView):
  model = Perishable
  fields = ['name', 'category', 'store_name', 'price', 'expiration']


# def add_photo(request, item_id):
#     # photo-file will be the "name" attribute on the <input type="file">
#     photo_file = request.FILES.get('photo-file', None)
#     if photo_file:
#         s3 = boto3.client('s3')
#         # need a unique "key" for S3 / needs image file extension too
#         key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
#         # just in case something goes wrong
#         try:
#             bucket = os.environ['S3_BUCKET']
#             s3.upload_fileobj(photo_file, bucket, key)
#             # build the full url string
#             url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
#             # we can assign to item_id or item (if you have a item object)
#             Photo.objects.create(url=url, item_id=item_id)
#         except Exception as e:
#             print('An error occurred uploading file to S3')
#             print(e)
#     return redirect('detail', item_id=item_id)