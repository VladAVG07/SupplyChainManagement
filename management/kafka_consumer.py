from confluent_kafka import Consumer, KafkaException
from django.core.mail import send_mail
from django.conf import settings
from .models import Shipments
import json

# Kafka Consumer Configuration
consumer_config = {
    'bootstrap.servers': 'localhost:9092',  # Kafka Broker
    'group.id': 'shipment-status-consumer-group',  # Consumer group ID
    'auto.offset.reset': 'earliest',  # Start consuming from the earliest available message
}

consumer = Consumer(consumer_config)

# Subscribe to the Kafka topic
consumer.subscribe(['shipment-status-updates'])

# Function to consume messages and send email
def consume_messages():
    try:
        while True:
            msg = consumer.poll(timeout=1.0)  # Poll for new messages
            if msg is None:
                continue  # No message available, continue polling
            if msg.error():
                raise KafkaException(msg.error())
            else:
                # Message received successfully
                shipment_update = msg.value().decode('utf-8')
                if(shipment_update != 'start'):
                    shipment_data = json.loads(shipment_update)
                    # Send email based on the shipment update
                    send_shipment_email(shipment_data)

    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()

# Function to send an email when shipment status changes
def send_shipment_email(shipment_data):
    shipment_id = shipment_data['shipment_id']
    status = shipment_data['status']

    # Get shipment info from the database
    shipment = Shipments.objects.filter(shipment_id=shipment_id).first()
    if shipment:
        subject = f"Shipment {shipment_id} Status Changed"
        message = f"The status of your shipment {shipment_id} has been updated to: {status}"
        
        # You can use the warehouse email or customer email here
        recipient_list = ['vlad-gabriel.apostol@asmi.ro']  # Assuming the warehouse has an email field

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,  # Sender's email (use your email here)
            recipient_list,
            fail_silently=False,
        )
        print(f"Email sent for shipment {shipment_id} with status {status}")
