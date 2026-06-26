import pandas as pd
import numpy as np
import os

def profile_and_clean_data():
    raw_path = r"C:\Users\rkvig\Downloads\Joshi\task1_wrangling\cleaned_retail.csv"
    output_dir = r"C:\Users\rkvig\Downloads\Joshi\task1_wrangling"
    output_path = os.path.join(output_dir, "cleaned_retail.csv")
    
    print("=== Step 1: Loading raw data ===")
    # Load using ISO-8859-1 to handle 0xa3 and other encoding issues
    df = pd.read_csv(raw_path, encoding='ISO-8859-1')
    total_raw_rows = len(df)
    print(f"Loaded {total_raw_rows:,} rows and {len(df.columns)} columns.")
    
    print("\n=== Step 2: Initial Profiling ===")
    print("Missing values count and percentage:")
    missing = df.isnull().sum()
    for col in df.columns:
        pct = (missing[col] / total_raw_rows) * 100
        print(f"  {col}: {missing[col]:,} nulls ({pct:.2f}%)")
        
    duplicates_count = df.duplicated().sum()
    print(f"Duplicate rows count: {duplicates_count:,} ({duplicates_count/total_raw_rows*100:.2f}%)")
    
    print("\nValue ranges for Quantity and UnitPrice:")
    print(f"  Quantity: min={df['Quantity'].min()}, max={df['Quantity'].max()}")
    print(f"  UnitPrice: min={df['UnitPrice'].min()}, max={df['UnitPrice'].max()}")
    
    # Analyze negative values
    neg_quantity = (df['Quantity'] <= 0).sum()
    neg_price = (df['UnitPrice'] < 0).sum()
    zero_price = (df['UnitPrice'] == 0).sum()
    print(f"  Negative Quantity rows: {neg_quantity:,}")
    print(f"  Negative UnitPrice rows: {neg_price:,}")
    print(f"  Zero UnitPrice rows: {zero_price:,}")
    
    print("\n=== Step 3: Cleaning Data ===")
    
    # 1. Drop duplicates
    print(f"Dropping {duplicates_count:,} duplicate rows...")
    df = df.drop_duplicates()
    
    # 2. Clean text fields (Description)
    print("Cleaning Description field...")
    df['Description'] = df['Description'].fillna("UNKNOWN PRODUCT")
    df['Description'] = df['Description'].astype(str).str.strip().str.upper()
    
    # 3. Handle CustomerID
    print("Handling CustomerID field...")
    # Store indicator for guest checkouts
    df['IsGuest'] = df['CustomerID'].isnull().astype(int)
    # Cast CustomerID to string to allow placeholder guest IDs, handling PyArrow null representations safely
    df['CustomerID'] = df['CustomerID'].fillna('nan').astype(str)
    # Clean up standard floats like 17850.0 -> 17850
    df['CustomerID'] = df['CustomerID'].apply(lambda x: str(x).split('.')[0] if '.' in str(x) else str(x))
    # Fill nan/nan values with Guest_<InvoiceNo> to preserve individual guest transaction identities
    df.loc[df['CustomerID'] == 'nan', 'CustomerID'] = 'Guest_' + df.loc[df['CustomerID'] == 'nan', 'InvoiceNo'].astype(str)
    
    # 4. Standardize InvoiceDate to standard datetime
    print("Standardizing InvoiceDate format...")
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], errors='coerce')
    
    # Drop rows where InvoiceDate parsing failed
    null_dates = df['InvoiceDate'].isnull().sum()
    if null_dates > 0:
        print(f"Dropping {null_dates} rows with unparseable InvoiceDate.")
        df = df.dropna(subset=['InvoiceDate'])
        
    # 5. Handle Quantity and UnitPrice outliers/anomalies
    print("Filtering anomalies in UnitPrice and Quantity...")
    
    # If UnitPrice is negative, it's an accounting adjustment/bad debt. Filter it out.
    df = df[df['UnitPrice'] >= 0]
    
    # Let's add a column to identify cancellations
    df['IsCancelled'] = df['InvoiceNo'].astype(str).str.startswith('C').astype(int)
    
    # Note: Quantity can be negative for cancellations, which is valid and reflects returns.
    # However, if Quantity is negative and NOT a cancellation, these are usually inventory adjustments/damages (often UnitPrice=0).
    # Let's filter out non-cancellation transactions with Quantity <= 0
    valid_cancellations = (df['IsCancelled'] == 1) & (df['Quantity'] < 0)
    valid_purchases = (df['IsCancelled'] == 0) & (df['Quantity'] > 0)
    
    before_filter = len(df)
    df = df[valid_cancellations | valid_purchases]
    filtered_rows = before_filter - len(df)
    print(f"Filtered out {filtered_rows:,} rows representing invalid transactions (negative/zero quantity without cancellation).")
    
    # Also filter out transactions with UnitPrice = 0 (like free gifts or manual entries) to keep revenue calculations clean
    zero_price_rows = (df['UnitPrice'] == 0).sum()
    df = df[df['UnitPrice'] > 0]
    print(f"Filtered out {zero_price_rows:,} rows with zero UnitPrice.")
    
    # 6. Feature Engineering
    print("Performing feature engineering...")
    # Calculate LineTotal
    df['LineTotal'] = df['Quantity'] * df['UnitPrice']
    
    # Extract temporal components
    df['InvoiceYear'] = df['InvoiceDate'].dt.year
    df['InvoiceMonth'] = df['InvoiceDate'].dt.month
    df['InvoiceDay'] = df['InvoiceDate'].dt.day
    df['InvoiceHour'] = df['InvoiceDate'].dt.hour
    df['DayOfWeek'] = df['InvoiceDate'].dt.dayofweek # 0=Monday, 6=Sunday
    
    # 7. Final profiling and saving
    cleaned_rows = len(df)
    print(f"\nCleaned dataset has {cleaned_rows:,} rows ({cleaned_rows/total_raw_rows*100:.2f}% of raw).")
    print(f"Cleaned columns: {df.columns.tolist()}")
    
    # Check for missing values in final df
    final_nulls = df.isnull().sum().sum()
    print(f"Missing values in cleaned dataset: {final_nulls}")
    
    print(f"Saving cleaned dataset to {output_path}...")
    df.to_csv(output_path, index=False, encoding='utf-8')
    print("Data cleaning complete!")

if __name__ == "__main__":
    profile_and_clean_data()