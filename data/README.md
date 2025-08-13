# Data Folder

This folder contains the **synthetic dataset** used to populate the Retail Promotions & Sales Data Warehouse.

## Files
- `raw_stores.csv` – Store master data (store_id, region, format, etc.)
- `raw_products.csv` – Product master data (SKU, brand, category, size, cost, price, etc.)
- `raw_customers.csv` – Customer profiles (segment, loyalty tier, etc.)
- `raw_promos.csv` – Promotion master list (rules, dates, channels, etc.)
- `raw_promo_product_map.csv` – Mapping of promos to eligible products
- `raw_inventory_snapshots.csv` – Monthly on-hand & on-order inventory
- `raw_orders.csv` – Orders (header-level data)
- `raw_order_items.csv` – Order line items (SKU, qty, prices, promo applied)
- `README.txt` – Dataset notes
- `schema_dw.sql` – Example staging schema


