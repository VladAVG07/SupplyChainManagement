from django.urls import path

from . import views

app_name = "management"
urlpatterns = [
    path('', views.index, name='index'),
    path('update_coords/<int:id>', views.update_coords, name='update_coords')
]