from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('meal-entry/', views.meal_entry, name='meal_entry'),
    path('bazar-entry/', views.bazar_entry, name='bazar_entry'),
    path('meal-summary/', views.meal_summary, name='meal_summary'),
    path('person-list/', views.person_list, name='person_list'),
    path('person-create/', views.person_create, name='person_create'),
    path('person-edit/<int:pk>/', views.person_edit, name='person_edit'),
    path('person-delete/<int:pk>/', views.person_delete, name='person_delete'),
    path('meal-details/', views.meal_details, name='meal_details'),
]
