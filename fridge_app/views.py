from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from .models import Perishable, Receipt, Reminder
from .forms import ReminderForm, ReceiptForm
from django.views.generic.edit import FormView
from django.core.mail import send_mail
from django.http import HttpResponse
import os
import boto3
import uuid
from django.urls import reverse, reverse_lazy


# Create your views here.
def send_email(request, reminder_id):
    error_message = ''
    reminder = Reminder.objects.get(id=reminder_id)
    subject = reminder.name + ' ' + 'Forget Me Not Reminder'
    message = reminder.description
    from_email = 'forget.me.no.sei.620@gmail.com'
    try:
        send_mail(
            subject,
            message,
            from_email,
            [reminder.send_to_email],
            fail_silently=False,
            auth_user=os.environ['SES_USER'],
            auth_password=os.environ['SES_PW']
        )
    except Exception as e:
        if 'not verified' in e.__str__():
            error_message = "Please send an email to <a href = \"mailto: forget.me.no.sei.620@gmail.com\">forget.me.no.sei.620@gmail.com</a> to be added to the list of verified emails.  Thank you!"
        else:
            error_message = e
    context = {'reminder': reminder, 'error_message': error_message}
    return render(request, 'fridge_app/reminder_detail.html', context)


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
    fields = ['store_name', 'purchase_date', 'receipt_total', 'item_list']
    
    def get(self, request, perishable_id):
        perishable = Perishable.objects.get(pk=perishable_id)
        form = ReceiptForm()
        context = {'form': form, 'perishable': perishable}
        return render(request, self.template, context)

    def post(self, request, perishable_id):
        perishable = Perishable.objects.get(pk=perishable_id)
        form = ReceiptForm(request.POST)
        if form.is_valid():
            receipt = form.save(commit=False)
            receipt.user = request.user  # Associate the user
            receipt.save()  # saves the receipt with the user association
            perishable.receipts.add(receipt)
            return redirect('perishables_detail', pk=perishable.pk)
        context = {'form': form, 'perishable': perishable}
        return render(request, self.template, context)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ReceiptUpdate(LoginRequiredMixin, UpdateView):
    model = Receipt
    fields = ['store_name', 'purchase_date', 'receipt_total', 'item_list']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add ModelB instance to the context
        perishables = Perishable.objects.all()
        context['perishables'] = perishables


        return context


class ReceiptDelete(LoginRequiredMixin, DeleteView):
    model = Receipt
    success_url = '/receipt'
    
def add_remove_perishable(request, receipt_id):
# get receipt
    receipt= Receipt.objects.get(id=receipt_id)

    # list to add
    a_list = request.POST.getlist('perishables_list')
    item_list = receipt.perishable_set.all()

    # if list from multiselect is empty
    if not a_list:
        # remove all perishables
        for p in item_list:
            receipt.perishable_set.remove(p.id)
    # if list from multiselect is NOT empty
    else:
        # if receipt perishables is empty
        if not item_list:
            # add everything from multiselect list
            for p in a_list:
                receipt.perishable_set.add(p)
        # if receipt perishables is NOT empty
        else:
            # build list of items to keep in receipt perishables
            r_keep_list = item_list.filter(id__in=a_list)

            # add new items to receipt perishables
            for p in a_list:
                if p not in r_keep_list:
                    receipt.perishable_set.add(p)
                    
            # build list of items to remove in receipt perishables
            r_remove_list = item_list.exclude(id__in=a_list)

            # remove items from receipt perishables
            for p in r_remove_list:
                receipt.perishable_set.remove(p.id)

# redirect to receipt detail (same page as multiselect list)
    return redirect('receipts_detail', pk=receipt_id)



# Views for Reminders ------------------------------------------------------------

class ReminderList(LoginRequiredMixin, ListView):
    model = Reminder


class ReminderDetail(LoginRequiredMixin, DetailView):
    model = Reminder

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add ModelB instance to the context
        perishables = Perishable.objects.all()
        context['perishables'] = perishables


        return context


class ReminderCreate(LoginRequiredMixin, CreateView):
    model = Reminder
    fields = ['name', 'description', 'date', 'time', 'send_to_email']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ReminderUpdate(LoginRequiredMixin, UpdateView):
    model = Reminder
    fields = ['name', 'description', 'date', 'time', 'send_to_email']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add ModelB instance to the context
        perishables = Perishable.objects.all()
        context['perishables'] = perishables


        return context

class ReminderDelete(LoginRequiredMixin, DeleteView):
    model = Reminder
    success_url = '/reminders'

def add_remove_perish(request, reminder_id):
    # get reminder
    reminder = Reminder.objects.get(id=reminder_id)
    
    # list to add
    a_list = request.POST.getlist('perishables_list')
    reminder_list = reminder.perishable_set.all()

    # if list from multiselect is empty
    if not a_list:
        # remove all perishables
        for p in reminder_list:
            reminder.perishable_set.remove(p.id)
    # if list from multiselect is NOT empty
    else:
        # if reminder perishables is empty
        if not reminder_list:
            # add everything from multiselect list
            for p in a_list:
                reminder.perishable_set.add(p)
        # if reminder perishables is NOT empty
        else:
            # build list of items to keep in reminder perishables
            r_keep_list = reminder_list.filter(id__in=a_list)

            # add new items to reminder perishables
            for p in a_list:
                if p not in r_keep_list:
                    reminder.perishable_set.add(p)
                    
            # build list of items to remove in reminder perishables
            r_remove_list = reminder_list.exclude(id__in=a_list)

            # remove items from reminder perishables
            for p in r_remove_list:
                reminder.perishable_set.remove(p.id)

    # redirect to reminder detail (same page as multiselect list)
    return redirect('reminders_detail', pk=reminder_id)



# Adding a reminder to a perishable item ----------------------------------------------------------


class AddReminder(View):
    template = 'fridge_app/reminder_add.html'

    def get(self, request, perishable_id):
        perishable = Perishable.objects.get(pk=perishable_id)
        form = ReminderForm()
        context = {'form': form, 'perishable': perishable}
        return render(request, self.template, context)

    def post(self, request, perishable_id):
        perishable = Perishable.objects.get(pk=perishable_id)
        form = ReminderForm(request.POST)
        if form.is_valid():
            reminder = form.save(commit=False)
            reminder.user = request.user  # Associate the user
            reminder.save()  # saves the reminder with the user association
            perishable.reminders.add(reminder)
            return redirect('perishables_detail', pk=perishable.pk)
        context = {'form': form, 'perishable': perishable}
        return render(request, self.template, context)

# ------photo upload for receipts----------------------------------------------------------------------------------


@login_required
def add_receipt(request, receipt_id):
    receipt_image = request.FILES.get('receipt-image', None)
    if receipt_image:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + \
            receipt_image.name[receipt_image.name.rfind('.'):]
    try:
        bucket = os.environ['S3_BUCKET']
        s3.upload_fileobj(receipt_image, bucket, key)
        url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
        receipt = Receipt.objects.get(id=receipt_id)
        receipt.url = url
        receipt.save()
    except Exception as e:
        print('An error occurred uploading file to S3')
        print(e)
    return redirect('receipt_detail', receipt_id=receipt_id)

# perishables list in todo list style

class PerishablesListView(ListView):
    model = Perishable
    name = "perishable_list/index.html"

class PerishableItemListView(ListView):
    model = Perishable
    name = "perishable_list/index.html"

    def get_queryset(self):
        return Perishable.objects.filter(perishable_id=self.kwargs["list_id"])

    def get_context_data(self):
        context = super().get_context_data()
        context["perishable_list"] = Perishable.objects.get(id=self.kwargs["list_id"])
        return context

class PerishableListCreate(CreateView):
    model = Perishable
    fields = ["name"]

    def get_context_data(self):
        context = super(PerishableListCreate, self).get_context_data()
        context["name"] = "Add a new Item"
        return context

class PerishableItemCreate(CreateView):
    model = Perishable
    fields = [
        "perishable_list",
        "name",
        "quantity",
        "category",
    ]

    def get_initial(self):
        initial_data = super(PerishableItemCreate, self).get_initial()
        perishable_list = Perishable.objects.get(id=self.kwargs["list_id"])
        initial_data["perishable_list"] = perishable_list
        return initial_data

    def get_context_data(self):
        context = super(PerishableItemCreate, self).get_context_data()
        perishable_list = Perishable.objects.get(id=self.kwargs["list_id"])
        context["perishable_list"] = perishable_list
        context["title"] = "Create a new item"
        return context

    def get_success_url(self):
        return reverse("list", args=[self.object.perishable_list_id])

class PerishableItemUpdate(UpdateView):
    model = Perishable
    fields = [
        "perishable_list",
        "name",
        "quantity",
        "category",
    ]

    def get_context_data(self):
        context = super(PerishableItemUpdate, self).get_context_data()
        context["perishable_list"] = self.object.perishable_list
        context["name"] = "Edit item"
        return context

    def get_success_url(self):
        return reverse("list", args=[self.object.perishable_list_id])
    
class PerishableListDelete(DeleteView):
    model = Perishable
    success_url = reverse_lazy("index")

class PerishableItemDelete(DeleteView):
    model = Perishable

    def get_success_url(self):
        return reverse_lazy("list", args=[self.kwargs["list_id"]])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["perishable_list"] = self.object.perishable_list
        return context