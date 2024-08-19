# Walmart Black Friday Sales Analysis
## Objective
- Develop a real-time data warehousing solution that ingests, processes, and visualizes sales data from Walmart's Black Friday event.
## Data
- Real-time streams:
  - Sales Transaction Stream (transaction_id, product_id, timestamp, quantity, unit_price, store_id)
  - Inventory Updates Stream (product_id, timestamp, quantity_change, store_id)
- Pre-loaded dimension data:
  - Products (product_id, name, category, price, supplier_id)
  - Stores (store_id, location, size, manager)
## Cloud Service
- AWS
## Techstacks
- Docker
- Confluent Kafka
- Spark Streaming
- Redshift
- Quicksight
## Architecture
<img src="https://github.com/sandeepdevamisra/Walmart-Black-Friday-Sales-Analysis/blob/main/img/architecture.png" alt="architecture" width="80%">

## File structure
- `Walmart-Black-Friday-Sales-Analysis`/
  - `img`/
  - `data`/
    - `products.csv`
    - `stores.csv`
  - `artifacts`/
    - `docker-compose.yml`
    - `redshift-jdbc42-2.1.0.12.jar`
  - `src`\
    - `kafka_producer.py`
    - `spark_redshift_stream_inventory.py`
    - `spark_redshift_stream_sales.py`
  - `README.md`
## Steps 
- Load the [products.csv](https://github.com/sandeepdevamisra/Walmart-Black-Friday-Sales-Analysis/blob/main/data/products.csv) and [stores.csv](https://github.com/sandeepdevamisra/Walmart-Black-Friday-Sales-Analysis/blob/main/data/stores.csv) in S3
- Create a schema and load these tables in Redshift
  - products
    ```
    create schema walmart_sales_analysis
    CREATE TABLE walmart_sales_analysis.products (
        product_id VARCHAR(100),
        category VARCHAR(100),
        name VARCHAR(200),
        supplier_id VARCHAR(100),
        price FLOAT4
    );
    COPY walmart_sales_analysis.products
    FROM '<enter S3 path to the file' 
    IAM_ROLE 'enter IAM role associated with Redshift'
    DELIMITER ','
    IGNOREHEADER 1
    REGION '<enter region of Redshift>';
    ```
  - stores
    ```
    CREATE TABLE walmart_sales_analysis.stores (
        store_id VARCHAR(100),
        location VARCHAR(100),
        manager VARCHAR(200)
    );
    COPY walmart_sales_analysis.stores
    FROM '<enter S3 path to the file' 
    IAM_ROLE 'enter IAM role associated with Redshift'
    DELIMITER ','
    IGNOREHEADER 1
    REGION '<enter region of Redshift>';
    ```


