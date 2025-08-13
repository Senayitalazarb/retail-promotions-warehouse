# Architecture — Retail Promotions & Sales Data Warehouse

This project implements a compact Kimball-style warehouse for retail sales, promotions, and inventory.  
**Stack:** PostgreSQL (DW) • Python (ingest/loader) • dbt Core (modeling) • Power BI (BI)

---

## 1) High-level data flow

```mermaid
flowchart LR
  A[CSV Dataset\n(data/retail_dw_sample)] -->|COPY| B[Postgres STAGING\nschema: stg.*]
  B -->|SQL/ETL| C[CONFORMED DIMENSIONS & FACTS\nschema: retail_dw.*]
  C -->|Direct Connect| D[Power BI\nReports & DQ Views]
  subgraph Guardrails
    C --> V1[v_bad_promo_unlimited_cash]
    C --> V2[v_promo_date_issues]
    C --> V3[v_promo_leakage_signals]
  end

