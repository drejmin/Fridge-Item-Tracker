from django.urls import path
from . import views

urlpatterns=[
     path('accounts/signup/', views.signup, name='signup'),
     path('home/', views.home, name='home'),
     path('', views.home, name='home'),
     path('reciept/receipt/', views.receipt_index, name='receipt_index'),
     path('reciept/receipt/<int:receipt_id>/', views.receipt_detail, name ='receipt_detail'),
     path('receipt/create/', views.ReceiptCreate.as_view(), name = 'receipt_create'),
     path('receipt/<int:pk>/update/', views.ReceiptUpdate.as_view(), name= 'receipt_update'),
     path('receipt/<int:pk>/delete/', views.ReceiptDelete.as_view(), name= 'receipt_delete'),
    # path('items/<int:item_id>/add_photo/', views.add_photo, name='add_photo'),
]

