from django.urls import path
from . import views

urlpatterns=[
     path('accounts/signup/', views.signup, name='signup'),
     path('home/', views.home, name='home'),
     path('', views.home, name='home'),
    # path('items/<int:item_id>/add_photo/', views.add_photo, name='add_photo'),
     path('perishables/', views.PerishableList.as_view(), name='perishables_index'),
     path('perishables/<int:pk>/', views.PerishableDetail.as_view(), name='perishables_detail'),
     path('perishables/create/', views.PerishableCreate.as_view(), name='perishables_create'),
     path('perishables/<int:pk>/update/', views.PerishableUpdate.as_view(), name='perishables_update'),
     path('perishables/<int:pk>/delete/', views.PerishableDelete.as_view(), name='perishables_delete'),
]

