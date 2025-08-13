#!/usr/bin/env python3

import duckdb
import os

print("Creating DuckDB database from Excel file...")

conn = duckdb.connect('ev_data.duckdb')

conn.execute("INSTALL spatial")
conn.execute("LOAD spatial")

conn.execute("""
    CREATE TABLE IF NOT EXISTS ev_data AS 
    SELECT * FROM st_read('EVDataExplorer2025.xlsx', layer='GEVO_EV_2025')
""")

result = conn.execute("SELECT COUNT(*) FROM ev_data").fetchone()
print(f"Imported {result[0]} rows into ev_data table")

result = conn.execute("SELECT DISTINCT parameter FROM ev_data ORDER BY parameter").fetchall()
print("\nAvailable parameters:")
for row in result:
    print(f"  - {row[0]}")

result = conn.execute("SELECT DISTINCT mode FROM ev_data WHERE mode IS NOT NULL ORDER BY mode").fetchall()
print("\nAvailable vehicle types:")
for row in result:
    print(f"  - {row[0]}")

result = conn.execute("""
    SELECT MIN(year) as min_year, MAX(year) as max_year 
    FROM ev_data 
    WHERE category = 'Historical'
""").fetchone()
print(f"\nHistorical data range: {result[0]} - {result[1]}")

conn.close()
print("\nDatabase created successfully: ev_data.duckdb")