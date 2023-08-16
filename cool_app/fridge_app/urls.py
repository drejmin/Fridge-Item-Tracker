from django.urls import path
from . import views

urlpatterns=[
    path('accounts/signup/', views.signup, name='signup'),
    path('home/', views.home, name='home'),
    path('', views.home, name='home'),
  
    # URLs for Receipt
    path('receipt/', views.receipt_index, name='receipt_index'),
    ath('receipt/<int:receipt_id>/', views.receipt_detail, name ='receipt_detail'),
    path('receipt/create/', views.ReceiptCreate.as_view(), name = 'receipt_create'),
    path('receipt/<int:pk>/update/', views.ReceiptUpdate.as_view(), name= 'receipt_update'),
    path('receipt/<int:pk>/delete/', views.ReceiptDelete.as_view(), name= 'receipt_delete'),

    # URLs for Reminders
    path('reminders/', views.ReminderList.as_view(), name='reminders_index'),
    path('reminders/<int:pk>/', views.ReminderDetail.as_view(), name='reminders_detail'),
    path('reminders/create/', views.ReminderCreate.as_view(), name='reminders_create'),
    path('reminders/<int:pk>/update/', views.ReminderUpdate.as_view(), name='reminders_update'),
    path('reminders/<int:pk>/delete/', views.ReminderDelete.as_view(), name='reminders_delete'),
  

]

