import pandas as pd
import os

base_path = "/home/saag/Documents/BigDataCW/Coursework_dataset"

def check_inconsistencies():
    print("Checking for inconsistencies...")
    
    # 1. Load data
    customers = pd.read_csv(os.path.join(base_path, "customers.csv"))
    orders = pd.read_csv(os.path.join(base_path, "orders.csv"))
    order_items = pd.read_csv(os.path.join(base_path, "order_items.csv"))
    products = pd.read_csv(os.path.join(base_path, "products.csv"))
    reviews = pd.read_csv(os.path.join(base_path, "reviews.csv"))
    suppliers = pd.read_csv(os.path.join(base_path, "suppliers.csv"))

    # A. Missing Values
    print("\n[Missing Values Check]")
    # Single column missing - discount
    if 'discount_pct' in orders.columns:
        missing_discount = orders['discount_pct'].isnull().sum()
        print(f"Missing 'discount_pct' in orders: {missing_discount}")
    
    # Multi column missing - email & age group
    # Let's check which columns exist first
    print(f"Customer columns: {customers.columns.tolist()}")
    if 'email' in customers.columns and 'age_group' in customers.columns:
        multi_missing = customers[customers['email'].isnull() & customers['age_group'].isnull()]
        print(f"Customers with both 'email' and 'age_group' missing: {len(multi_missing)}")

    # B. Duplicates
    print("\n[Duplicates Check]")
    # Single duplicate - order_id
    order_id_duplicates = orders['order_id'].duplicated().sum()
    print(f"Duplicate 'order_id' in orders: {order_id_duplicates}")

    # C. Review Score Inconsistency
    print("\n[Review Score Check]")
    if 'review_score' in reviews.columns:
        # Check range 0-6 vs 0-5
        score_range = sorted(reviews['review_score'].dropna().unique())
        print(f"Unique review scores: {score_range}")
        out_of_range = reviews[reviews['review_score'] > 5]
        print(f"Reviews with score > 5: {len(out_of_range)}")

    # D. Invalid Emails (Spaces)
    print("\n[Invalid Email Check]")
    if 'email' in customers.columns:
        email_with_spaces = customers['email'].fillna('').astype(str).str.contains(' ').sum()
        print(f"Emails with spaces: {email_with_spaces}")

    # E. Orphan Records
    print("\n[Orphan Records Check]")
    # Orders without customers
    orphans_orders = orders[~orders['customer_id'].isin(customers['customer_id'])]
    print(f"Orders without matching customer: {len(orphans_orders)}")
    
    # Order items without orders
    orphans_items = order_items[~order_items['order_id'].isin(orders['order_id'])]
    print(f"Order items without matching order: {len(orphans_items)}")
    
    # Order items without products
    orphans_products = order_items[~order_items['product_id'].isin(products['product_id'])]
    print(f"Order items without matching product: {len(orphans_products)}")
    
    # Reviews without products
    orphans_reviews_prod = reviews[~reviews['product_id'].isin(products['product_id'])]
    print(f"Reviews without matching product: {len(orphans_reviews_prod)}")

    # Reviews without orders
    orphans_reviews_order = reviews[~reviews['order_id'].isin(orders['order_id'])]
    print(f"Reviews without matching order: {len(orphans_reviews_order)}")

    # Products without suppliers
    orphans_suppliers = products[~products['supplier_id'].isin(suppliers['supplier_id'])]
    print(f"Products without matching supplier: {len(orphans_suppliers)}")

if __name__ == "__main__":
    check_inconsistencies()
