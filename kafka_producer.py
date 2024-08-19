from kafka import KafkaProducer
import json
import random
from datetime import datetime
import time
import boto3
import uuid
import csv
from io import StringIO
import pandas as pd

# Kafka configuration
bootstrap_servers = ['localhost:9092']  # Change to your Kafka server address
sales_transaction_topic = 'sales_topic'  # Change to your Kafka topic name
inventory_updates_topic = 'inventory_topic'


# Creating Kafka producer
producer = KafkaProducer(bootstrap_servers=bootstrap_servers,
                         value_serializer=lambda x: json.dumps(x).encode('utf-8'))


s3 = boto3.client('s3')

products_obj = s3.get_object(Bucket='black-friday-sales', Key='products.csv')
products_data = products_obj['Body'].read().decode('utf-8')
products_data = pd.read_csv(StringIO(products_data))

stores_obj = s3.get_object(Bucket='black-friday-sales', Key='stores.csv')
stores_data = stores_obj['Body'].read().decode('utf-8')
stores_data = pd.read_csv(StringIO(stores_data))

# Functions to generate random data
def generate_uuid():
    random_uuid = uuid.uuid4()
    uuid_str = f"T-{random_uuid}"
    return uuid_str

def generate_random_timestamp():
    random_time = "{:02d}:{:02d}:{:02d}".format(random.randint(0, 23), random.randint(0, 59), 
                    random.randint(0, 59))
    timestamp = "2023-11-24 {}".format(random_time)
    return timestamp

def generate_mock_data():

    transaction_id = generate_uuid()
    product_row_num = random.randint(0,9)
    stores_row_num = random.randint(0,4)
    product_id = products_data.loc[product_row_num, 'product_id']
    timestamp = generate_random_timestamp()
    quantity = random.randint(1,6)
    unit_price = int(products_data.loc[product_row_num, 'price'])
    store_id = stores_data.loc[stores_row_num, 'store_id']

    sales_transaction = {
        'transaction_id': transaction_id,
        'product_id': product_id,
        'timestamp_': timestamp,
        'quantity' : quantity,
        'unit_price' : unit_price,
        'store_id' : store_id
    }

    inventory_updates = {
        'product_id': product_id,
        'timestamp_': timestamp,
        'quantity_change' : -quantity,
        'store_id' : store_id
    }

    return sales_transaction, inventory_updates

# Infinite loop to continuously send data
try:
    while True:
        sales_transaction, inventory_updates = generate_mock_data()
        producer.send(sales_transaction_topic, value=sales_transaction)
        producer.send(inventory_updates_topic, value=inventory_updates)
        print(f"Sales Transaction sent: {sales_transaction}")
        print(f"Inventory Updates sent: {inventory_updates}")
        time.sleep(3)
except KeyboardInterrupt:
    print("Data generation stopped.")
