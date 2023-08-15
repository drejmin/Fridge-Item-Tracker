from django.urls import path
from . import views

urlpatterns=[
    path('acounts/signup/', views.signup, name='signup'),
    
]