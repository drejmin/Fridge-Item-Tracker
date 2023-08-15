from django.urls import path
from . import views

urlpatterns=[
     path('accounts/signup/', views.signup, name='signup'),
     path('home/', views.home, name='home')
    # path('items/<int:item_id>/add_photo/', views.add_photo, name='add_photo'),
]

