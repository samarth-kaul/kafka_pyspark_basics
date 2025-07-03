import json
from kafka import KafkaConsumer

# Create a consumer subscribing to 'test-topic'
try:
    consumer = KafkaConsumer(
    'test-topic',
    bootstrap_servers='localhost:29092',
    auto_offset_reset='earliest',  # start from beginning if no offset  
    group_id='my-group',             
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )
    print("kafka connected")
except Exception as e:
    print("Failed to connect to Kafka:", e)
    exit(1)

print("Waiting for messages...\n")

for message in consumer:
    print(f"Received: {message.value}")