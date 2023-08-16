from django.urls import path
from . import views

urlpatterns=[
    path('accounts/signup/', views.signup, name='signup'),
    path('home/', views.home, name='home'),
    path('', views.home, name='home'),
    # path('items/<int:item_id>/add_photo/', views.add_photo, name='add_photo'),

    # URLs for Reminders
    path('reminders/', views.ReminderList.as_view(), name='reminders_index'),
    path('reminders/<int:pk>/', views.ReminderDetail.as_view(), name='reminders_detail'),
    path('reminders/create/', views.ReminderCreate.as_view(), name='reminders_create'),
    path('reminders/<int:pk>/update/', views.ReminderUpdate.as_view(), name='reminders_update'),
    path('reminders/<int:pk>/delete/', views.ReminderDelete.as_view(), name='reminders_delete'),
  

]

