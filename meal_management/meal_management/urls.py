# meal_management/urls.py

from django.contrib import admin
from django.urls import path, include
from meals import views as meal_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('meals/', include('meals.urls')),
    path('', meal_views.home, name='home'),  # Ensure this points to the home view
]
