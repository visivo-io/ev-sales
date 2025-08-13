import pandas as pd
import duckdb
import os

excel_file = 'ev_data_iea.xlsx'
xl = pd.ExcelFile(excel_file, engine='openpyxl')

print("Available sheets in the Excel file:")
for sheet in xl.sheet_names:
    print(f"  - {sheet}")

sales_df = pd.read_excel(excel_file, sheet_name='EV sales', engine='openpyxl')
stock_df = pd.read_excel(excel_file, sheet_name='EV stock', engine='openpyxl')
share_df = pd.read_excel(excel_file, sheet_name='EV sales share', engine='openpyxl')

print("\n=== EV Sales Data ===")
print(f"Shape: {sales_df.shape}")
print(f"Columns: {list(sales_df.columns)}")
print(f"First few rows:\n{sales_df.head()}")

print("\n=== EV Stock Data ===")
print(f"Shape: {stock_df.shape}")
print(f"Columns: {list(stock_df.columns)}")
print(f"First few rows:\n{stock_df.head()}")

print("\n=== EV Sales Share Data ===")
print(f"Shape: {share_df.shape}")
print(f"Columns: {list(share_df.columns)}")
print(f"First few rows:\n{share_df.head()}")

os.makedirs('data', exist_ok=True)

sales_df.to_csv('data/ev_sales.csv', index=False)
stock_df.to_csv('data/ev_stock.csv', index=False)
share_df.to_csv('data/ev_sales_share.csv', index=False)

print("\n✅ CSV files saved to data/ directory")

conn = duckdb.connect('ev_data.duckdb')

conn.execute("""
    CREATE OR REPLACE TABLE ev_sales AS 
    SELECT * FROM read_csv_auto('data/ev_sales.csv')
""")

conn.execute("""
    CREATE OR REPLACE TABLE ev_stock AS 
    SELECT * FROM read_csv_auto('data/ev_stock.csv')
""")

conn.execute("""
    CREATE OR REPLACE TABLE ev_sales_share AS 
    SELECT * FROM read_csv_auto('data/ev_sales_share.csv')
""")

print("\n✅ Data loaded into DuckDB")

result = conn.execute("SELECT COUNT(*) as rows FROM ev_sales").fetchone()
print(f"EV sales table: {result[0]} rows")

result = conn.execute("SELECT COUNT(*) as rows FROM ev_stock").fetchone()
print(f"EV stock table: {result[0]} rows")

result = conn.execute("SELECT COUNT(*) as rows FROM ev_sales_share").fetchone()
print(f"EV sales share table: {result[0]} rows")

conn.close()