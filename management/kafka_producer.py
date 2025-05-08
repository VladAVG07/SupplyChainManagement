from confluent_kafka import Producer
import json

# Kafka Configuration
kafka_config = {
    'bootstrap.servers': 'localhost:9092',  # Kafka Broker
    'client.id': 'django-shipment-app',
}

# Create the Kafka producer
producer = Producer(kafka_config)

# Kafka Producer Callback
def delivery_callback(err, msg):
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

# Function to send message to Kafka
def send_shipment_status_update(shipment_id, status):
    message = {
        "shipment_id": str(shipment_id),
        "status": str(status),
    }
    
    # Sending the message to the Kafka topic
    producer.produce('shipment-status-updates', value=str(json.dumps(message)), callback=delivery_callback)
    producer.flush()

def init_topic():
    producer.produce('shipment-status-updates', value = 'start', callback = delivery_callback)
    producer.flush()
