from django.core.management.base import BaseCommand
from management.kafka_consumer import consume_messages  # Import the Kafka consumer function

class Command(BaseCommand):
    help = 'Start Kafka Consumer to listen to shipment status updates'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting Kafka Consumer...'))
        consume_messages()  # Start consuming messages
