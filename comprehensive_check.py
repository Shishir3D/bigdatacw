import pandas as pd
import os
from datetime import datetime

base_path = "/home/saag/Documents/BigDataCW/Coursework_dataset"

def check_inconsistencies():
    print("--- COMPREHENSIVE DATA ANALYSIS ---")
    
    # 1. Load data
    customers = pd.read_csv(os.path.join(base_path, "customers.csv"))
    orders = pd.read_csv(os.path.join(base_path, "orders.csv"))
    order_items = pd.read_csv(os.path.join(base_path, "order_items.csv"))
    products = pd.read_csv(os.path.join(base_path, "products.csv"))
    reviews = pd.read_csv(os.path.join(base_path, "reviews.csv"))
    suppliers = pd.read_csv(os.path.join(base_path, "suppliers.csv"))
    date_dim = pd.read_csv(os.path.join(base_path, "date_dim_helper.csv"))

    # today's date "2026-04-13"
    today = datetime(2026, 4, 13)

    # 1. Missing discount_pct (Known)
    missing_discount = orders['discount_pct'].isna().sum()
    print(f"1. Missing 'discount_pct' in orders: {missing_discount}")

    # 2. Duplicate order_id (Known)
    dup_orders = orders['order_id'].duplicated().sum()
    print(f"2. Duplicate 'order_id' in orders: {dup_orders}")

    # 3. Orphan orders -> customers (Known)
    orphan_o_c = orders[~orders['customer_id'].isin(customers['customer_id'])]
    print(f"3. Orphan orders -> customers: {len(orphan_o_c)}")

    # 4. Orphan order_items -> products (Known)
    orphan_oi_p = order_items[~order_items['product_id'].isin(products['product_id'])]
    print(f"4. Orphan order_items -> products: {len(orphan_oi_p)}")

    # 5. Orphan reviews -> products (Known)
    orphan_r_p = reviews[~reviews['product_id'].isin(products['product_id'])]
    print(f"5. Orphan reviews -> products: {len(orphan_r_p)}")

    # 6. Review score > 5 (Known)
    score_gt5 = reviews[reviews['review_score'] > 5]
    print(f"6. Review score > 5: {len(score_gt5)}")

    print("\n[Debugging Multi-missing]")
    print(f"Customer columns: {customers.columns.tolist()}")
    print(f"Customer head:\n{customers.head(1)}")

    # 7. Invalid emails with spaces (Known)
    email_spaces = customers['email'].fillna('').astype(str).str.contains(' ').sum()
    print(f"7. Emails with spaces: {email_spaces}")

    # 8. Both email and age group missing - check strings "null", "none", "nan"
    # we already did this, but maybe they are empty strings?
    # Let's print the counts of 'email' and 'age_group' being empty
    email_empty = customers['email'].isna() | (customers['email'].astype(str).str.strip() == '')
    age_empty = customers['age_group'].isna() | (customers['age_group'].astype(str).str.strip() == '')
    print(f"DEBUG: empty email count: {email_empty.sum()}")
    print(f"DEBUG: empty age count: {age_empty.sum()}")
    both_missing = customers[email_empty & age_empty]
    print(f"8. Both email and age group missing: {len(both_missing)}")

    # 18. BS Year vs AD Year inconsistency
    # bs_year should be ~56-57 years ahead of AD year in date_dim_helper
    if 'bs_year' in date_dim.columns and 'year' in date_dim.columns:
        diff = date_dim['bs_year'] - date_dim['year']
        wrong_bs = date_dim[~diff.isin([56, 57])]
        print(f"18. Inconsistent BS Year in date_dim: {len(wrong_bs)}")

    # 19. Reviews with score 0-5 but user says 0-6?
    # we found score > 5 is 600. Let's see unique values > 5
    print(f"Unique scores > 5: {reviews[reviews['review_score'] > 5]['review_score'].unique()}")

    # 20. Negative Price in Products
    neg_p = products[products['unit_price'] < 0]
    print(f"20. Negative price in products: {len(neg_p)}")

    # 21. Units in stock < 0
    if 'units_in_stock' in products.columns:
        neg_stock = products[products['units_in_stock'] < 0]
        print(f"21. Negative units_in_stock: {len(neg_stock)}")

    # 22. Discount > 100% or < 0%?
    bad_disc = orders[(orders['discount_pct'] < 0) | (orders['discount_pct'] > 1)]
    print(f"22. Discount out of bounds (0-1): {len(bad_disc)}")

    # 23. Review date before order date?
    merged_ro = reviews.merge(orders[['order_id', 'order_date']], on='order_id', how='left')
    merged_ro['review_date'] = pd.to_datetime(merged_ro['review_date'], errors='coerce')
    merged_ro['order_date'] = pd.to_datetime(merged_ro['order_date'], errors='coerce')
    rev_before_ord = merged_ro[merged_ro['review_date'] < merged_ro['order_date']]
    print(f"23. Review date before order date: {len(rev_before_ord)}")

    # 24. Orphan: order_items -> orders
    orphan_oi_o = order_items[~order_items['order_id'].isin(orders['order_id'])]
    print(f"24. Orphan order_items -> orders: {len(orphan_oi_o)}")

    # 25. Orphan: orders -> date_dim (on order_date)
    # date_dim has 'date' column string?
    if 'order_date' in orders.columns and 'date' in date_dim.columns:
        # assume both are YYYY-MM-DD
        orphan_date = orders[~orders['order_date'].astype(str).isin(date_dim['date'].astype(str))]
        print(f"25. Orders with dates NOT in date_dim: {len(orphan_date)}")

    # 34. Custom Orphan Check: Suppliers -> Products
    orphan_p_s = products[~products['supplier_id'].isin(suppliers['supplier_id'])]
    print(f"34. Orphan products (invalid supplier_id): {len(orphan_p_s)}")

    # 35. Price logic: line_total != (quantity * unit_price_at_sale) * (1 - discount_pct) ?
    # Let's check if the formula holds
    merged_all = order_items.merge(orders[['order_id', 'discount_pct']], on='order_id', how='left')
    merged_all['discount_pct'] = merged_all['discount_pct'].fillna(0)
    expected_total = (merged_all['quantity'] * merged_all['unit_price_at_sale']) * (1 - merged_all['discount_pct'])
    logic_error = merged_all[abs(merged_all['line_total'] - expected_total) > 0.05]
    print(f"35. Line Total doesn't match Qty * Price * (1-Disc): {len(logic_error)}")

    # 36. Review Score = 0
    print(f"36. Review scores = 0: {len(reviews[reviews['review_score'] == 0])}")

    # 37. Unit Price at Sale < List Price (is it because of discount? but discount is often separate)
    # Actually, let's just look for any orphans again
    print(f"37. Orphan reviews -> products: {len(reviews[~reviews['product_id'].isin(products['product_id'])])}")

    # 38. Registration date AFTER review date?
    merged_rc = reviews.merge(orders[['order_id', 'customer_id']], on='order_id', how='left')
    merged_rc = merged_rc.merge(customers[['customer_id', 'registration_date']], on='customer_id', how='left')
    merged_rc['review_date'] = pd.to_datetime(merged_rc['review_date'], errors='coerce')
    merged_rc['registration_date'] = pd.to_datetime(merged_rc['registration_date'], errors='coerce')
    bad_reg_rev = merged_rc[merged_rc['registration_date'] > merged_rc['review_date']]
    print(f"38. Review before Registration: {len(bad_reg_rev)}")

    # 39. Empty state_province in customers? 
    empty_state = customers['state_province'].isna().sum()
    print(f"39. Customers with missing state_province: {empty_state}")

    # 40. Duplicate product_id?
    dup_prod = products['product_id'].duplicated().sum()
    print(f"40. Duplicate product_id: {dup_prod}")

if __name__ == "__main__":
    check_inconsistencies()
