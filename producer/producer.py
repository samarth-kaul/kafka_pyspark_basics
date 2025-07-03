import json
from faker import Faker
from kafka import KafkaProducer
import time

# Connect to Kafka running in Docker
try:
    producer = KafkaProducer(
    bootstrap_servers='localhost:29092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    print("kafka connected")
except Exception as e:
    print("Failed to connect to Kafka:", e)
    exit(1)

faker = Faker()

def generate_user():
    return {
        "name": faker.name(),
        "email": faker.email(),
        "phone": faker.phone_number(),
        "address": faker.address()
    }

print("Producing messages...\n")
while True:
    message = generate_user()
    producer.send("test-topic", message)
    print(f"✅ Sent: {message}")
    time.sleep(2)