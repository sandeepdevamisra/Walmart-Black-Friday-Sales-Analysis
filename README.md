# Walmart Black Friday Sales Analysis
## Objective
- Develop a real-time data warehousing solution that ingests, processes, and visualizes sales data from Walmart's Black Friday event.
## Data
- Real-time streams:
  - Sales Transaction Stream (transaction_id, product_id, timestamp, quantity, unit_price, store_id)
  - Inventory Updates Stream (product_id, timestamp, quantity_change, store_id)
- Pre-loaded dimensional data:
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
  - 
