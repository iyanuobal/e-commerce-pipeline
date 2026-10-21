# E-commerce Analytics Pipeline

An end-to-end data engineering project: raw e-commerce data goes in, a tested
star-schema warehouse comes out. Built with Python, PySpark, and SQL, and it
runs entirely on a laptop.

**Business questions it answers**

1. Which product categories and sellers drive the most revenue?
2. How does late delivery affect customer review scores?
3. How do sales trend month over month, by state?

## Architecture

```
Olist CSVs ──► Bronze (raw Parquet) ──► Silver (clean) ──► Gold (star schema)
                    │                       │                    │
              Python ingestion        PySpark transforms    External tables
              + load metadata         + quality checks      + SQL analytics
                                      + quarantine table
```

| Layer | Contents | Tooling |
|---|---|---|
| Bronze | Raw tables as-is, plus `_ingested_at` and `_source_file` | Python |
| Silver | Typed, deduplicated, null-normalized tables; bad rows go to a quarantine table | PySpark |
| Gold | `fact_order_items`, `dim_customer`, `dim_seller`, `dim_product`, `dim_date` | PySpark |
| Serving | External tables over Gold, plus analytics queries | Spark SQL |

See [docs/data_model.md](docs/data_model.md) for the full star schema.

## Data source

[Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
on Kaggle (CC BY-NC-SA 4.0). Download it and place the CSVs in `data/raw/olist/`.
The `data/` folder is gitignored, so the raw files are never committed.

## Planned repo layout

```
ecommerce-pipeline/
├── README.md
├── requirements.txt
├── docs/
│   └── data_model.md
├── data/                # gitignored: raw, bronze, silver, gold
├── src/
│   ├── ingestion/       # Python: load CSVs to Bronze, fetch reference data
│   ├── transform/       # PySpark: Bronze -> Silver -> Gold
│   └── utils/           # shared helpers (logging, schema checks)
├── sql/
│   ├── ddl/             # external table definitions
│   └── analytics/       # business-question queries
└── tests/               # pytest for Python helpers and transform logic
```

## Build roadmap

- [x] **Phase 1: Ingestion (Python).** Validate the raw files, load each CSV to
      Bronze Parquet with load metadata, add logging and error handling.
- [ ] **Phase 2: Silver (PySpark).** Type casting, deduplication, null
      normalization, and a quarantine table for rows that fail checks.
- [ ] **Phase 3: Gold (PySpark).** Build the dimensions and fact table with
      surrogate keys.
- [ ] **Phase 4: External tables (Spark SQL).** Register the Gold files as
      external tables with `CREATE TABLE ... USING PARQUET LOCATION ...`.
- [ ] **Phase 5: SQL analytics.** Answer the three business questions with
      window functions and CTEs.
- [ ] **Phase 6: Tests and docs.** `pytest` for key functions, and fill in the
      "How to run" section below.

## How to run

_To be filled in as the phases are completed._
