from django.urls import path
from . import views

urlpatterns = [

    path('accounts/signup/', views.signup, name='signup'),
    path('home/', views.home, name='home'),
    path('', views.home, name='home'),

    # URLs for Perishables
    path('perishables/', views.PerishableList.as_view(), name='perishables_index'),
    path('perishables/<int:pk>/', views.PerishableDetail.as_view(),
         name='perishables_detail'),
    path('perishables/create/', views.PerishableCreate.as_view(),
         name='perishables_create'),
    path('perishables/<int:pk>/update/',
         views.PerishableUpdate.as_view(), name='perishables_update'),
    path('perishables/<int:pk>/delete/',
         views.PerishableDelete.as_view(), name='perishables_delete'),

    # URLs for Receipt
    path('receipt/', views.receipt_index, name='receipt_index'),
    path('receipt/<int:receipt_id>/', views.receipt_detail, name='receipt_detail'),
    path('receipt/create/', views.ReceiptCreate.as_view(), name='receipt_create'),
    path('receipt/<int:pk>/update/',
         views.ReceiptUpdate.as_view(), name='receipt_update'),
    path('receipt/<int:pk>/delete/',
         views.ReceiptDelete.as_view(), name='receipt_delete'),
    path('receipt/<int:receipt_id>/add_receipt/',
         views.add_receipt, name='add_receipt'),

    # URLs for Reminders
    path('reminders/', views.ReminderList.as_view(), name='reminders_index'),

    path('reminders/<int:pk>/', views.ReminderDetail.as_view(),
         name='reminders_detail'),
    path('reminders/create/', views.ReminderCreate.as_view(),
         name='reminders_create'),
    path('reminders/<int:pk>/update/',
         views.ReminderUpdate.as_view(), name='reminders_update'),
    path('reminders/<int:pk>/delete/',
         views.ReminderDelete.as_view(), name='reminders_delete'),

    # URLs for Add Reminders tp Perishable
    path('perishable/<int:perishable_id>/add_reminder/',
         views.AddReminder.as_view(), name='add_reminder'),

    # Send Email
    path('send_email/<int:reminder_id>', views.send_email, name='send_email'),

]
