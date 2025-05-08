from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

app_name = "management"
urlpatterns = [
    path('', views.index, name='index'),
    path('update_coords/<int:id>', csrf_exempt(views.update_coords), name='update_coords'),
    path('update_shipment_state/<int:id>', csrf_exempt(views.update_shipment_state), name='update_shipment_state')
]