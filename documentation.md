# Data Inconsistency Findings

This document summarizes the data inconsistencies found in the coursework dataset.

## Summary of 14 Data Inconsistencies

Through a comprehensive analysis of the coursework dataset, the following 14 specific data inconsistencies have been identified across all CSV files.

### 1. Missing Values: `discount_pct` in `orders.csv`
- **Finding**: 300 records have missing values in the `discount_pct` column.
- **Dataset**: [Coursework_dataset/orders.csv](Coursework_dataset/orders.csv)
- **Impact**: Affects revenue calculations and financial reporting.

### 2. Multi-column Missingness: `email` & `age_group` in `customers.csv`
- **Finding**: High volume of missing data in both columns (800 missing emails, 300 missing age groups).
- **Dataset**: [Coursework_dataset/customers.csv](Coursework_dataset/customers.csv)
- **Impact**: Limits marketing segmentation and customer outreach capabilities.

### 3. Duplicate Primary Key: `order_id` in `orders.csv`
- **Finding**: 500 duplicate `order_id` values found.
- **Dataset**: [Coursework_dataset/orders.csv](Coursework_dataset/orders.csv)
- **Impact**: Violates primary key integrity and causes double-counting in joins.

### 4. Orphan Records: Orders without Customers
- **Finding**: 1,202 orders reference a `customer_id` that does not exist.
- **Dataset**: [Coursework_dataset/orders.csv](Coursework_dataset/orders.csv) $\rightarrow$ [Coursework_dataset/customers.csv](Coursework_dataset/customers.csv)
- **Impact**: Transactions cannot be linked to customer demographics.

### 5. Orphan Records: Order Items without Products
- **Finding**: 250 records reference a `product_id` missing from the products table.
- **Dataset**: [Coursework_dataset/order_items.csv](Coursework_dataset/order_items.csv) $\rightarrow [Coursework_dataset/products.csv](Coursework_dataset/products.csv)
- **Impact**: Inventory and product-level sales analysis will be inaccurate.

### 6. Orphan Records: Reviews without Products
- **Finding**: 74 reviews are linked to non-existent `product_id` values.
- **Dataset**: [Coursework_dataset/reviews.csv](Coursework_dataset/reviews.csv) $\rightarrow [Coursework_dataset/products.csv](Coursework_dataset/products.csv)
- **Impact**: Reviews for non-existent products indicate data leakage or ghost records.

### 7. Orphan Records: Reviews without Orders
- **Finding**: Certain reviews cannot be traced back to valid `order_id`s in the system.
- **Dataset**: [Coursework_dataset/reviews.csv](Coursework_dataset/reviews.csv) $\rightarrow [Coursework_dataset/orders.csv](Coursework_dataset/orders.csv)
- **Impact**: Ghost reviews that cannot be verified against a purchase history.

### 8. Review Score Range Violation (0-6 vs 0-5)
- **Finding**: 600 records have a `review_score` of 6.0, exceeding the standard 0-5 scale.
- **Dataset**: [Coursework_dataset/reviews.csv](Coursework_dataset/reviews.csv)
- **Impact**: Skews product rating averages and reporting.

### 9. Invalid Email Format (Spaces)
- **Finding**: 175 customer records contain emails with spaces (e.g., "user name@email.com").
- **Dataset**: [Coursework_dataset/customers.csv](Coursework_dataset/customers.csv)
- **Impact**: Prevents automated communication and validation.

### 10. Temporal Logic: Review Date before Order Date
- **Finding**: 180 reviews were posted on dates earlier than the actual `order_date`.
- **Dataset**: [Coursework_dataset/reviews.csv](Coursework_dataset/reviews.csv) vs [Coursework_dataset/orders.csv](Coursework_dataset/orders.csv)
- **Impact**: Logically impossible; indicates errors in date logging.

### 11. Calculated Field Mismatch: Line Total Consistency
- **Finding**: 400 records where `quantity * unit_price_at_sale` does not equal `line_total`.
- **Dataset**: [Coursework_dataset/order_items.csv](Coursework_dataset/order_items.csv)
- **Impact**: Indicates logic errors in payment processing or order logging.

### 12. Calculated Field Mismatch: Discount Application
- **Finding**: Widespread mismatch where final totals do not match the expected formula `(gross_total * (1 - discount_pct))`.
- **Dataset**: [Coursework_dataset/order_items.csv](Coursework_dataset/order_items.csv)
- **Impact**: Inconsistent discount recording across the dataset.

### 13. Integrity Violation: Review before Registration
- **Finding**: 62 reviews exist for products where the customer's `registration_date` is later than the `review_date`.
- **Dataset**: [Coursework_dataset/reviews.csv](Coursework_dataset/reviews.csv) vs [Coursework_dataset/customers.csv](Coursework_dataset/customers.csv)
- **Impact**: Suggests data corruption (customers reviewing before registering).

### 14. Pricing Outlier: Sale Price vs List Price
- **Finding**: 5,412 records where `unit_price_at_sale` is significantly higher than the standard `unit_price`.
- **Dataset**: [Coursework_dataset/order_items.csv](Coursework_dataset/order_items.csv) vs [Coursework_dataset/products.csv](Coursework_dataset/products.csv)
- **Impact**: Potential pricing errors or unrecorded surcharges.
