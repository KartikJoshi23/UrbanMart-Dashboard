"""
UrbanMart Sales Analysis - Console Application
================================================
This script performs basic data loading, exploration, and CLI-based analytics
for UrbanMart retail transaction data.

Author: MAIB Student
Course: Python Programming with Streamlit
"""

import csv
import pandas as pd
from datetime import datetime


# =============================================================================
# PART 1: BASIC PYTHON & DATA LOADING
# =============================================================================

def display_welcome_message():
    """Display a welcome message using variables and f-strings."""
    store_name = "UrbanMart"
    version = "1.0"
    print("=" * 60)
    print(f"   Welcome to {store_name} Sales Analysis System v{version}")
    print("=" * 60)
    print()


def load_data_with_csv_module(filepath):
    """
    Load CSV data using Python's built-in csv module.
    
    Args:
        filepath (str): Path to the CSV file
        
    Returns:
        list: List of dictionaries containing transaction data
    """
    data = []
    try:
        with open(filepath, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                row['quantity'] = int(row['quantity'])
                row['unit_price'] = float(row['unit_price'])
                row['discount_applied'] = float(row['discount_applied'])
                data.append(row)
        print(f"✓ Successfully loaded {len(data)} records using csv module.")
        return data
    except FileNotFoundError:
        print(f"✗ Error: File '{filepath}' not found.")
        return []
    except Exception as e:
        print(f"✗ Error loading file: {e}")
        return []


def load_data_with_pandas(filepath):
    """
    Load CSV data using pandas (preferred method).
    
    Args:
        filepath (str): Path to the CSV file
        
    Returns:
        pandas.DataFrame: DataFrame containing transaction data
    """
    try:
        df = pd.read_csv(filepath)
        print(f"✓ Successfully loaded {len(df)} records using pandas.")
        return df
    except FileNotFoundError:
        print(f"✗ Error: File '{filepath}' not found.")
        return pd.DataFrame()
    except Exception as e:
        print(f"✗ Error loading file: {e}")
        return pd.DataFrame()


def perform_sanity_checks(df):
    """
    Perform basic sanity checks on the loaded data.
    
    Args:
        df (pandas.DataFrame): The loaded DataFrame
    """
    print("\n" + "-" * 40)
    print("DATA SANITY CHECKS")
    print("-" * 40)
    
    print(f"• Total number of rows: {len(df)}")
    
    unique_stores = df['store_id'].unique().tolist()
    print(f"• Unique Store IDs: {unique_stores}")
    
    df['date'] = pd.to_datetime(df['date'])
    min_date = df['date'].min().strftime('%Y-%m-%d')
    max_date = df['date'].max().strftime('%Y-%m-%d')
    print(f"• Date Range: {min_date} to {max_date}")
    
    unique_customers = df['customer_id'].nunique()
    print(f"• Unique Customers: {unique_customers}")
    
    unique_products = df['product_id'].nunique()
    print(f"• Unique Products: {unique_products}")
    print()


def demonstrate_data_structures(data_list):
    """
    Demonstrate use of lists, tuples, and dictionaries.
    
    Args:
        data_list (list): List of dictionaries from CSV
    """
    print("\n" + "-" * 40)
    print("DATA STRUCTURES DEMONSTRATION")
    print("-" * 40)
    
    # List of product categories
    product_categories = []
    for row in data_list:
        category = row['product_category']
        if category not in product_categories:
            product_categories.append(category)
    
    print(f"\n• Product Categories (List):")
    print(f"  {product_categories}")
    
    # Dictionary: store_id → store_location
    store_mapping = {}
    for row in data_list:
        store_id = row['store_id']
        store_location = row['store_location']
        if store_id not in store_mapping:
            store_mapping[store_id] = store_location
    
    print(f"\n• Store ID → Location Mapping (Dictionary):")
    for store_id, location in store_mapping.items():
        print(f"  {store_id}: {location}")
    
    # Tuple of payment methods
    payment_methods = tuple(set(row['payment_method'] for row in data_list))
    print(f"\n• Payment Methods (Tuple):")
    print(f"  {payment_methods}")
    
    # Count Online vs In-store using loop
    online_count = 0
    instore_count = 0
    
    for row in data_list:
        if row['channel'] == 'Online':
            online_count += 1
        elif row['channel'] == 'In-store':
            instore_count += 1
    
    print(f"\n• Channel Distribution (Manual Count):")
    print(f"  Online transactions: {online_count}")
    print(f"  In-store transactions: {instore_count}")
    print()


# =============================================================================
# PART 2: FUNCTIONS & SIMPLE KPIs
# =============================================================================

def compute_total_revenue(df):
    """Calculate total revenue."""
    df['line_revenue'] = (df['quantity'] * df['unit_price']) - df['discount_applied']
    total_revenue = df['line_revenue'].sum()
    return round(total_revenue, 2)


def compute_revenue_by_store(df):
    """Calculate revenue breakdown by store."""
    df['line_revenue'] = (df['quantity'] * df['unit_price']) - df['discount_applied']
    revenue_by_store = df.groupby('store_location')['line_revenue'].sum()
    return revenue_by_store.round(2).to_dict()


def compute_revenue_by_category(df):
    """Calculate revenue breakdown by product category."""
    df['line_revenue'] = (df['quantity'] * df['unit_price']) - df['discount_applied']
    revenue_by_category = df.groupby('product_category')['line_revenue'].sum()
    return revenue_by_category.sort_values(ascending=False).round(2).to_dict()


def compute_top_n_products(df, n=5):
    """Get top N products by revenue."""
    df['line_revenue'] = (df['quantity'] * df['unit_price']) - df['discount_applied']
    top_products = df.groupby('product_name')['line_revenue'].sum()
    top_products = top_products.sort_values(ascending=False).head(n)
    return top_products.round(2)


def compute_top_n_customers(df, n=5):
    """Get top N customers by revenue."""
    df['line_revenue'] = (df['quantity'] * df['unit_price']) - df['discount_applied']
    top_customers = df.groupby('customer_id')['line_revenue'].sum()
    top_customers = top_customers.sort_values(ascending=False).head(n)
    return top_customers.round(2)


def display_menu():
    """Display the CLI menu options."""
    print("\n" + "=" * 40)
    print("       UrbanMart Analytics Menu")
    print("=" * 40)
    print("  1. Show Total Revenue")
    print("  2. Show Revenue by Store")
    print("  3. Show Revenue by Category")
    print("  4. Show Top 5 Products")
    print("  5. Show Top 5 Customers")
    print("  6. Exit")
    print("=" * 40)


def run_cli_menu(df):
    """Run the interactive CLI menu."""
    while True:
        display_menu()
        
        try:
            choice = input("\nEnter your choice (1-6): ").strip()
            
            if choice == '1':
                total_revenue = compute_total_revenue(df.copy())
                print(f"\n📊 Total Revenue: ${total_revenue:,.2f}")
                
            elif choice == '2':
                revenue_by_store = compute_revenue_by_store(df.copy())
                print("\n📊 Revenue by Store Location:")
                print("-" * 30)
                for store, revenue in revenue_by_store.items():
                    print(f"  {store}: ${revenue:,.2f}")
                    
            elif choice == '3':
                revenue_by_category = compute_revenue_by_category(df.copy())
                print("\n📊 Revenue by Product Category:")
                print("-" * 35)
                for category, revenue in revenue_by_category.items():
                    print(f"  {category}: ${revenue:,.2f}")
                    
            elif choice == '4':
                top_products = compute_top_n_products(df.copy(), n=5)
                print("\n📊 Top 5 Products by Revenue:")
                print("-" * 40)
                for i, (product, revenue) in enumerate(top_products.items(), 1):
                    print(f"  {i}. {product}: ${revenue:,.2f}")
                    
            elif choice == '5':
                top_customers = compute_top_n_customers(df.copy(), n=5)
                print("\n📊 Top 5 Customers by Revenue:")
                print("-" * 30)
                for i, (customer, revenue) in enumerate(top_customers.items(), 1):
                    print(f"  {i}. {customer}: ${revenue:,.2f}")
                    
            elif choice == '6':
                print("\n👋 Thank you for using UrbanMart Analytics. Goodbye!")
                break
                
            else:
                print("\n⚠️  Invalid choice. Please enter a number between 1 and 6.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Program interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n⚠️  An error occurred: {e}")


# =============================================================================
# PART 3: PREPARE DATA FOR DASHBOARD
# =============================================================================

def prepare_data_for_dashboard(df):
    """Prepare and transform data for dashboard use."""
    df = df.copy()
    df['date'] = pd.to_datetime(df['date'])
    df['line_revenue'] = (df['quantity'] * df['unit_price']) - df['discount_applied']
    df['day_of_week'] = df['date'].dt.day_name()
    df['month'] = df['date'].dt.strftime('%Y-%m')
    return df


def filter_data(df, start_date=None, end_date=None, stores=None, channel=None, categories=None):
    """Filter DataFrame based on provided parameters."""
    filtered_df = df.copy()
    
    if start_date is not None:
        filtered_df = filtered_df[filtered_df['date'] >= pd.to_datetime(start_date)]
    
    if end_date is not None:
        filtered_df = filtered_df[filtered_df['date'] <= pd.to_datetime(end_date)]
    
    if stores is not None and len(stores) > 0:
        filtered_df = filtered_df[filtered_df['store_location'].isin(stores)]
    
    if channel is not None and channel != 'All':
        filtered_df = filtered_df[filtered_df['channel'] == channel]
    
    if categories is not None and len(categories) > 0:
        filtered_df = filtered_df[filtered_df['product_category'].isin(categories)]
    
    return filtered_df


def generate_summary_tables(df):
    """Generate summary tables for dashboard."""
    summaries = {}
    
    summaries['revenue_by_category'] = df.groupby('product_category')['line_revenue'].sum().sort_values(ascending=False)
    summaries['revenue_by_store'] = df.groupby('store_location')['line_revenue'].sum().sort_values(ascending=False)
    summaries['revenue_by_channel'] = df.groupby('channel')['line_revenue'].sum()
    
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    summaries['revenue_by_day'] = df.groupby('day_of_week')['line_revenue'].sum().reindex(day_order)
    
    summaries['top_customers'] = df.groupby('customer_id')['line_revenue'].sum().sort_values(ascending=False).head(10)
    summaries['top_products'] = df.groupby('product_name')['line_revenue'].sum().sort_values(ascending=False).head(10)
    
    return summaries


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """Main function to run the UrbanMart analysis script."""
    
    display_welcome_message()
    
    filepath = "urbanmart_sales.csv"
    
    print("Loading data with csv module...")
    data_list = load_data_with_csv_module(filepath)
    
    if not data_list:
        print("Failed to load data. Exiting.")
        return
    
    demonstrate_data_structures(data_list)
    
    print("\nLoading data with pandas...")
    df = load_data_with_pandas(filepath)
    
    if df.empty:
        print("Failed to load data. Exiting.")
        return
    
    perform_sanity_checks(df.copy())
    
    print("-" * 40)
    print("PREPARING DATA FOR DASHBOARD")
    print("-" * 40)
    df_prepared = prepare_data_for_dashboard(df)
    print("✓ Created 'line_revenue' column")
    print("✓ Created 'day_of_week' column")
    print("✓ Created 'month' column")
    
    summaries = generate_summary_tables(df_prepared)
    print("✓ Generated summary tables")
    
    run_cli_menu(df)


if __name__ == "__main__":
    main()
