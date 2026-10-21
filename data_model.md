# Data Model (Gold layer)

A star schema built around one fact table.

**Grain of the fact table:** one row per order item (one product line within
an order).

```
                    dim_date
                       │
dim_customer ──── fact_order_items ──── dim_seller
                       │
                  dim_product
```

## fact_order_items

| Column | Type | Notes |
|---|---|---|`  
| order_item_key | bigint | Surrogate key |
| order_id | string | Degenerate dimension (kept on the fact) |
| order_item_id | int | Line number within the order |
| customer_key | bigint | FK to dim_customer |
| seller_key | bigint | FK to dim_seller |
| product_key | bigint | FK to dim_product |
| purchase_date_key | int | FK to dim_date (yyyymmdd) |
| order_status | string | e.g. delivered, canceled |
| price | decimal(10,2) | Measure |
| freight_value | decimal(10,2) | Measure |
| delivery_days | int | Purchase to delivery; null if undelivered |
| is_late | boolean | Delivered after the estimated date |
| review_score | int | 1-5, null if no review. Per order, so repeats across items in the same order |

## dim_customer

| Column | Type | Notes |
|---|---|---|
| customer_key | bigint | Surrogate key |
| customer_unique_id | string | Natural key |
| city | string | |
| state | string | |

## dim_seller

| Column | Type | Notes |
|---|---|---|
| seller_key | bigint | Surrogate key |
| seller_id | string | Natural key |
| city | string | |
| state | string | |

## dim_product

| Column | Type | Notes |
|---|---|---|
| product_key | bigint | Surrogate key |
| product_id | string | Natural key |
| category_name_en | string | Translated from Portuguese |
| weight_g | int | |

## dim_date

| Column | Type | Notes |
|---|---|---|
| date_key | int | yyyymmdd |
| full_date | date | |
| year | int | |
| quarter | int | |
| month | int | |
| day_of_week | int | |
| is_weekend | boolean | |

## Design notes to revisit

- `customer_id` in the raw data is per order, while `customer_unique_id` is per
  person. dim_customer uses customer_unique_id because it identifies the actual person, doesn't change with every new order and it answers the question "how many repeat customers do we have?"

- Payments and reviews are many-to-one with orders. For v1, review score is
  folded into the fact table; a separate `fact_payments` table could come later.

  -`review_score` is per order, not per item, so it repeats across items in the same order. Average it the order level, not over fact rows.

