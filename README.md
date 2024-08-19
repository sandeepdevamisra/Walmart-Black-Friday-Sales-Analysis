# Walmart Black Friday Sales Analysis
## Objective
- Develop a real-time data warehousing solution that ingests, processes, and visualizes sales data from Walmart's Black Friday event.
## Data
- Real-time streams:
  - Sales Transaction Stream (transaction_id, product_id, timestamp, quantity, unit_price, store_id)
  - Inventory Updates Stream (product_id, timestamp, quantity_change, store_id)
- Pre-loaded dimension data:
  - Products (product_id, name, category, price, supplier_id)
  - Stores (store_id, location, manager)
## Data Model
<img src="https://github.com/sandeepdevamisra/Walmart-Black-Friday-Sales-Analysis/blob/main/img/data_model.png" alt="architecture" width="80%">

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
  - `src`/
    - `kafka_producer.py`
    - `spark_redshift_stream_inventory.py`
    - `spark_redshift_stream_sales.py`
  - `README.md`
## Steps 
- Load the [products.csv](https://github.com/sandeepdevamisra/Walmart-Black-Friday-Sales-Analysis/blob/main/data/products.csv) and [stores.csv](https://github.com/sandeepdevamisra/Walmart-Black-Friday-Sales-Analysis/blob/main/data/stores.csv) in S3
- Create a schema and load these tables in Redshift
  - products
    ```
    create schema black_friday_sales
    CREATE TABLE black_friday_sales.products (
        product_id VARCHAR(100),
        category VARCHAR(100),
        name VARCHAR(200),
        supplier_id VARCHAR(100),
        price FLOAT8
    );
    COPY black_friday_sales.products
    FROM '<enter S3 path to the file' 
    IAM_ROLE 'enter IAM role associated with Redshift'
    DELIMITER ','
    IGNOREHEADER 1
    REGION '<enter region of Redshift>';
    ```
  - stores
    ```
    CREATE TABLE black_friday_sales.stores (
        store_id VARCHAR(100),
        location VARCHAR(100),
        manager VARCHAR(200)
    );
    COPY black_friday_sales.stores
    FROM '<enter S3 path to the file' 
    IAM_ROLE 'enter IAM role associated with Redshift'
    DELIMITER ','
    IGNOREHEADER 1
    REGION '<enter region of Redshift>';
    ```
- Create the sales and inventory tables in Redshift
  - inventory
    ```
    CREATE TABLE black_friday_sales.inventory_updates(
        product_id VARCHAR(100),
        timestamp_ TIMESTAMP,
        quantity_change INTEGER,
        store_id VARCHAR(100)
    );
    ```
  - sales
    ```
    CREATE TABLE black_friday_sales.inventory_updates(
        transaction_id VARCHAR(100),
        product_id VARCHAR(100),
        timestamp_ TIMESTAMP,
        quantity INTEGER,
        unit_price FLOAT8,
        store_id VARCHAR(100)
    );
    ```
- Also create 2 S3 temporary directories `inventory_temp` for inventory table and `sales_temp` for sales table.
## Run instructions 
- Run the command `docker compose -f docker-compose.yml up -d`. Now the Kafka is up and running.
- In 2 different terminals, run the streaming scripts `python3 spark_redshift_stream_inventory.py` and `python3 spark_redshift_stream_sales.py`.
- Once the streaming scripts are up and running, in another terminal, run the producer script `kafka_producer.py`.
- The data will be ingested in real-time in Redshift. After this, we can perform analysis on the tables as well as connect with Quicksight to visualize.
## Additional instructions
- In Redshift, under security group, go to `inbound rule`. The port of Redshift should be exposed to all IP addresses.
- Spark streaming is running locally, so for connecting it to Redshift, go to `Actions -> Modify Publicly Accessible Setting` and enable `Turn on Publicly accessible` and save changes. However, this is not recommended in a production environment since that can result in a security breach.
- We will need package for interaction between Kafka and Spark, Spark Redshift conector, and Redshift JDBC connector.
- We are writing the data in JDBC format and therefore we will need the Redshift JDBC connector as well. Also we will need Redshift driver.
- Spark version - 3.5 (in reference to the packages). 

