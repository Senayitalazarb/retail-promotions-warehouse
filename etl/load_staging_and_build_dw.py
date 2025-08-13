#!/usr/bin/env python3
import os, sys, psycopg2

# Map of CSV -> (target table, columns)
MAP = {
    "raw_stores.csv": ("stg.stores", ["store_id","name","region","format","opened_date","closed_date"]),
    "raw_products.csv": ("stg.products", ["sku","upc","brand","category","subcategory","size","cost","list_price","status","effective_from"]),
    "raw_customers.csv": ("stg.customers", ["customer_id","segment","loyalty_tier","created_ts"]),
    "raw_promos.csv": ("stg.promos", ["promo_id","name","type","benefit_type","benefit_value","min_threshold","max_uses_per_cust","start_ts","end_ts","channels_allowed","inclusion_rule_json","exclusion_rule_json","created_by","created_ts","status"]),
    "raw_promo_product_map.csv": ("stg.promo_product_map", ["promo_id","sku","rule_type"]),
    "raw_inventory_snapshots.csv": ("stg.inventory_snapshots", ["snapshot_date","store_id","sku","on_hand","on_order","cost"]),
    "raw_orders.csv": ("stg.orders", ["order_id","order_ts","store_id","customer_id","channel"]),
    "raw_order_items.csv": ("stg.order_items", ["order_id","order_line_id","sku","qty","unit_price","gross_sales","promo_id","discount_amt","net_sales"]),
}

def conn_from_env():
    # Leverage libpq envs; fall back to defaults if not set
    dsn = " ".join(
        f"{k}={v}" for k, v in {
            "host": os.getenv("PGHOST", "localhost"),
            "port": os.getenv("PGPORT", "5432"),
            "dbname": os.getenv("PGDATABASE", "retail"),
            "user": os.getenv("PGUSER", "senayitberhane"),
            # PGPASSWORD read automatically by libpq if set in env
        }.items()
    )
    return psycopg2.connect(dsn)

def copy_csv(cur, path, table, cols):
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Missing file: {path}")
    with open(path, "r", encoding="utf-8") as f:
        cur.copy_expert(f"COPY {table} ({', '.join(cols)}) FROM STDIN WITH CSV HEADER", f)

def main(csv_dir):
    print("Connecting to Postgres using env vars (PGHOST/PGPORT/PGDATABASE/PGUSER/PGPASSWORD if set)…")
    conn = conn_from_env()
    conn.autocommit = True
    cur = conn.cursor()

    # Optional DDL (guarded by env var)
    if os.getenv("RUN_DDL", "0") == "1":
        ddl_path = os.path.join(os.path.dirname(__file__), "postgres_dw_full_ddl.sql")
        print(f"RUN_DDL=1 → applying DDL: {ddl_path}")
        with open(ddl_path, "r", encoding="utf-8") as f:
            cur.execute(f.read())
    else:
        print("RUN_DDL not set → skipping DDL (schemas/tables assumed to exist).")

    # Truncate staging tables (idempotent)
    print("Truncating staging tables…")
    for _, (table, _) in MAP.items():
        cur.execute(f"TRUNCATE {table};")

    # Load each CSV
    print(f"Loading CSVs from: {csv_dir}")
    for fname, (table, cols) in MAP.items():
        full_path = os.path.join(csv_dir, fname)
        print(f"  -> {fname}  →  {table}")
        copy_csv(cur, full_path, table, cols)

    print("✅ Loaded all staging tables successfully.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python etl/load_staging_and_build_dw.py /path/to/retail_dw_sample")
        sys.exit(1)
    main(sys.argv[1])
