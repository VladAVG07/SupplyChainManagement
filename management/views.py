# views.py
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotAllowed
from .models import Warehouses, Shipments
from geopy.geocoders import Nominatim
from time import sleep
import json
from .kafka_producer import send_shipment_status_update, init_topic

def index(request):
    init_topic()
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
        sleep(1)
        address = location.address if location else "Unknown Address"

        if shipments1:
            for s in shipments1:
                location = geolocator.geocode(s.location)
                shipment_data.append({
                    'id': s.shipment_id,
                    'lat': location.latitude,
                    'long': location.longitude,
                    'status': s.delivery_status
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

def update_coords(request, id):
    if request.method == 'POST':
        # Handle the POST request logic here
        shipment_data = json.loads(request.body)
        shipment = Shipments.objects.filter(shipment_id = id)[0]
        shipment.latitude = shipment_data['latitude']
        shipment.longitude = shipment_data['longitude']
        shipment.save(update_fields=['latitude', 'longitude'])

        return JsonResponse({'message': f'Coordinates updated for ID: {id}'})
    else:
        # Return a 405 Method Not Allowed response for non-POST requests
        return HttpResponseNotAllowed(['POST'])
    

def update_shipment_state(request, id):
    if(request.method == 'POST'):
        shipment_data = json.loads(request.body)
        shipment = Shipments.objects.filter(shipment_id = id)[0]
        shipment.delivery_status = shipment_data['status']
        shipment.save(update_fields = ['delivery_status'])

        send_shipment_status_update(shipment.shipment_id, shipment.delivery_status)

        return JsonResponse({'message': 'Updated successfully'})
    
    else:
        return HttpResponseNotAllowed(['POST'])

