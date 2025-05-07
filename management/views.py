# views.py
from django.shortcuts import render
from .models import Warehouses, Shipments
from geopy.geocoders import Nominatim

def index(request):
    warehouses = Warehouses.objects.all()
    shipments = Shipments.objects.all()
    geolocator = Nominatim(user_agent='warehouse_app')
    sum_lat = 0
    sum_long = 0
    warehouses_data = []
    for w in warehouses:
        shipment_data = []
        shipments1 = Shipments.objects.filter(warehouse = w.warehouse_id)
        sum_lat += w.lat
        sum_long += w.long
        location = geolocator.reverse((w.lat, w.long))
        address = location.address if location else "Unknown Address"

        if shipments1:
            for s in shipments1:
                location = geolocator.geocode(s.location)
                shipment_data.append({
                    'id': s.shipment_id,
                    'lat': location.latitude,
                    'long': location.longitude
                })


        warehouses_data.append({
            'id': w.warehouse_id,
            'name': w.name,
            'lat': w.lat,
            'long': w.long,
            'address': address,
            'shipment_data': shipment_data
        })

        
    avg_lat = sum_lat/len(warehouses)
    avg_long = sum_long/len(warehouses)

    context = {
        'warehouses': warehouses_data,
        'avg_lat': avg_lat,
        'avg_long': avg_long,
        'shipments': shipments,
        'shipment_data': shipment_data
    }
    return render(request, 'index.html', context)
