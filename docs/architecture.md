flowchart LR
  A["CSV Dataset (data/retail_dw_sample)"] -->|COPY| B["Postgres STAGING (schema stg)"]
  B -->|SQL / ETL| C["Conformed Dimensions & Facts (schema retail_dw)"]
  C -->|Direct Connect| D["Power BI Reports and DQ Views"]


