# Architecture — Retail Promotions & Sales Data Warehouse

This project implements a compact Kimball-style warehouse for retail sales, promotions, and inventory.  
**Stack:** PostgreSQL (DW) • Python (ETL loader) • dbt Core (modeling) • Power BI (BI layer)

---

## 1) High-Level Data Flow

```mermaid
flowchart LR
  A[CSV Dataset<br/>(data/retail_dw_sample)] -->|COPY| B[Postgres STAGING<br/>schema: stg]
  B -->|SQL / ETL| C[Conformed Dimensions & Facts<br/>schema: retail_dw]
  C -->|Direct Connect| D[Power BI<br/>Reports & DQ Views]

  subgraph Guardrails
    V1[v_bad_promo_unlimited_cash]
    V2[v_promo_date_issues]
    V3[v_promo_leakage_signals]
  end

  C --> V1
  C --> V2
  C --> V3
