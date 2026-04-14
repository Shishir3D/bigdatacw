# Data Problems and Solutions

---

## 1. Products Table

| # | Problem | Solution |
|---|---------|----------|
| 1 | **20 rows** had a null `category` | Mapped each `subcategory` to its parent category (e.g. `Laptops → Electronics`, `Womens → Clothing`) using a lookup map |
| 2 | **50 rows** had a null `unit_price` | Filled with the mean `unit_price_at_sale` from `order_items` for that product. One product not found in order_items was filled with the overall mean |
| 3 | **250 order_items rows** referenced product_ids that do not exist in the products table (orphan records) | Reported the count and product_ids — flagged for review |
| 4 | No duplicate `product_id` rows | Confirmed: 0 duplicates |

---

## 2. Customers Table

| # | Problem | Solution |
|---|---------|----------|
| 1 | **800 rows** had a null `email` | Filled with `"unknown@domain.com"` |
| 2 | **175 rows** had an invalid email format (e.g. space in address) | Flagged using regex — reported but not dropped |
| 3 | **300 rows** had a null `age_group` | Filled with `"-1"` so it does not affect the distribution of real age groups |
| 4 | **153 emails** were shared by more than one customer | Reported — each customer should have a unique email |
| 5 | **1,202 orders** referenced a `customer_id` that did not exist in the customers table | Created dummy parent rows with placeholder values and added them to maintain referential integrity |
| 6 | No duplicate `customer_id` rows | Confirmed: 0 duplicates |
| 7 | No customer had multiple `age_group` values | Confirmed: 0 violations |

---

## 3. Orders Table

| # | Problem | Solution |
|---|---------|----------|
| 1 | **300 rows** had a null `discount_pct` | Filled with `0.0` — a missing discount means no discount was applied |
| 2 | **500 duplicate `order_id` rows** | Removed duplicates, keeping the first occurrence (400,500 → 400,000 rows) |
| 3 | `order_date` was stored as a string | Cast to `DateType` using `to_date()` — 0 unparseable values |

---

## 4. Order Items Table

| # | Problem | Solution |
|---|---------|----------|
| 1 | **400 rows** had a `line_total` that did not match `quantity × unit_price_at_sale` | Flagged as calculation mismatches (tolerance ±0.01 for rounding) — reported but not modified |
| 2 | **250 rows** referenced a `product_id` not found in the products table | Reported as orphan records |
| 3 | No null values in any column | Confirmed: 0 nulls |
| 4 | No duplicate `order_item_id` rows | Confirmed: 0 duplicates |

> No data transformations were needed. The table was validated only.

---

## 5. Reviews Table

| # | Problem | Solution |
|---|---------|----------|
| 1 | **3,000 rows** had a null `review_score` | Filled with `0.0` — treated as no rating given |
| 2 | **600 rows** had a `review_score` of `6.0` (valid range is 0–5) | Capped to `5.0` |
| 3 | `review_score` data type was inconsistent | Cast to `Double` |
| 4 | `review_date` was stored as a string | Cast to `DateType` using `to_date()` |
| 5 | **180 reviews** had a `review_date` before the `order_date` | Detected by joining reviews with orders on `order_id` — flagged as timeline violations |

---

## 6. Suppliers Table

| # | Problem | Solution |
|---|---------|----------|
| 1 | `contract_start` was stored as a string | Cast to `DateType` using `to_date()` — 0 unparseable values |
| 2 | No null values in any column | Confirmed: 0 nulls |
| 3 | No duplicate `supplier_id` rows | Confirmed: 0 duplicates |

> No data transformations were needed. The table was validated only.

---

## 7. Date Dimension Table

| # | Problem | Solution |
|---|---------|----------|
| 1 | `full_date` was stored as a string | Cast to `DateType` using `to_date()` |
| 2 | `quarter` was stored as labels (`Q1`, `Q2`, `Q3`, `Q4`) | Converted to integers (`1`, `2`, `3`, `4`) for correct sorting and aggregation |
| 3 | No null values in any column | Confirmed: 0 nulls |
| 4 | No duplicate `date_id` rows | Confirmed: 0 duplicates |
| 5 | Distinct value sanity check passed | `day_of_week`: 7, `month_name`: 12, `quarter`: 4, `is_weekend`: 2, `is_np_holiday`: 2 |
