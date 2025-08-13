import pandas as pd
import duckdb
import random

# Create comprehensive EV data based on real trends
countries = ['China', 'United States', 'Germany', 'France', 'United Kingdom', 
             'Norway', 'Netherlands', 'Sweden', 'Canada', 'Japan', 'South Korea',
             'India', 'Italy', 'Spain', 'Australia', 'Brazil', 'Mexico', 'Denmark',
             'Belgium', 'Switzerland']

years = list(range(2015, 2025))

# Real-world inspired data
ev_sales_data = []
ev_stock_data = []
market_share_data = []
charging_stations_data = []

# Base sales (in thousands) for 2015
base_sales = {
    'China': 188.7, 'United States': 115.2, 'Germany': 23.5, 'France': 17.3,
    'United Kingdom': 14.1, 'Norway': 25.8, 'Netherlands': 9.4, 'Sweden': 7.9,
    'Canada': 5.2, 'Japan': 10.5, 'South Korea': 2.9, 'India': 0.5,
    'Italy': 2.3, 'Spain': 1.5, 'Australia': 0.7, 'Brazil': 0.3, 'Mexico': 0.2,
    'Denmark': 4.5, 'Belgium': 3.2, 'Switzerland': 3.8
}

# Growth rates (annual)
growth_rates = {
    'China': 1.45, 'United States': 1.35, 'Germany': 1.40, 'France': 1.38,
    'United Kingdom': 1.42, 'Norway': 1.25, 'Netherlands': 1.35, 'Sweden': 1.38,
    'Canada': 1.30, 'Japan': 1.20, 'South Korea': 1.50, 'India': 1.60,
    'Italy': 1.35, 'Spain': 1.40, 'Australia': 1.35, 'Brazil': 1.45, 'Mexico': 1.50,
    'Denmark': 1.33, 'Belgium': 1.36, 'Switzerland': 1.34
}

stock = {country: 0 for country in countries}
charging_stations = {country: 100 for country in countries}  # Base charging stations

for year in years:
    for country in countries:
        if year == 2015:
            sales = base_sales[country]
        else:
            years_passed = year - 2015
            sales = base_sales[country] * (growth_rates[country] ** years_passed)
        
        # Add some variation
        random.seed(hash(f"{country}{year}"))
        sales = sales * (0.9 + random.random() * 0.2)
        
        # Calculate stock (cumulative with 95% retention rate)
        stock[country] = stock[country] * 0.95 + sales
        
        # Calculate market share (as percentage of total vehicle sales)
        if country == 'Norway':
            market_share = min(10 + (year - 2015) * 8, 92)
        elif country == 'China':
            market_share = min(1.5 + (year - 2015) * 5, 50)
        elif country in ['Netherlands', 'Sweden', 'Denmark']:
            market_share = min(2 + (year - 2015) * 4, 45)
        else:
            market_share = min(0.5 + (year - 2015) * 2.5, 35)
        
        # Calculate charging stations (growing with EV stock)
        charging_stations[country] = charging_stations[country] * 1.25 + sales * 10
        
        ev_sales_data.append({
            'Country': country,
            'Year': year,
            'EV_Sales': round(sales * 1000),  # Convert to units
            'Vehicle_Type': 'Total'
        })
        
        # Add BEV and PHEV breakdown
        bev_ratio = 0.6 + (year - 2015) * 0.03  # BEV share increases over time
        ev_sales_data.append({
            'Country': country,
            'Year': year,
            'EV_Sales': round(sales * 1000 * bev_ratio),
            'Vehicle_Type': 'BEV'
        })
        
        ev_sales_data.append({
            'Country': country,
            'Year': year,
            'EV_Sales': round(sales * 1000 * (1 - bev_ratio)),
            'Vehicle_Type': 'PHEV'
        })
        
        ev_stock_data.append({
            'Country': country,
            'Year': year,
            'EV_Stock': round(stock[country] * 1000),
            'Vehicle_Type': 'Total'
        })
        
        market_share_data.append({
            'Country': country,
            'Year': year,
            'Market_Share': round(market_share, 2),
            'Total_Vehicle_Sales': round(sales * 1000 * 100 / market_share) if market_share > 0 else 0
        })
        
        charging_stations_data.append({
            'Country': country,
            'Year': year,
            'Public_Charging_Points': round(charging_stations[country]),
            'Fast_Chargers': round(charging_stations[country] * 0.25),
            'Slow_Chargers': round(charging_stations[country] * 0.75)
        })

# Create DataFrames
sales_df = pd.DataFrame(ev_sales_data)
stock_df = pd.DataFrame(ev_stock_data)
share_df = pd.DataFrame(market_share_data)
charging_df = pd.DataFrame(charging_stations_data)

# Save to CSV
sales_df.to_csv('data/ev_sales.csv', index=False)
stock_df.to_csv('data/ev_stock.csv', index=False)
share_df.to_csv('data/ev_market_share.csv', index=False)
charging_df.to_csv('data/ev_charging_stations.csv', index=False)

print("✅ Created EV data CSV files")

# Create DuckDB database
conn = duckdb.connect('ev_data.duckdb')

# Create tables
conn.execute("""
    CREATE OR REPLACE TABLE ev_sales AS 
    SELECT * FROM read_csv_auto('data/ev_sales.csv')
""")

conn.execute("""
    CREATE OR REPLACE TABLE ev_stock AS 
    SELECT * FROM read_csv_auto('data/ev_stock.csv')
""")

conn.execute("""
    CREATE OR REPLACE TABLE ev_market_share AS 
    SELECT * FROM read_csv_auto('data/ev_market_share.csv')
""")

conn.execute("""
    CREATE OR REPLACE TABLE ev_charging_stations AS 
    SELECT * FROM read_csv_auto('data/ev_charging_stations.csv')
""")

# Create analytical views
conn.execute("""
    CREATE OR REPLACE VIEW ev_sales_by_year AS
    SELECT 
        Year,
        SUM(CASE WHEN Vehicle_Type = 'Total' THEN EV_Sales ELSE 0 END) as Total_Sales,
        SUM(CASE WHEN Vehicle_Type = 'BEV' THEN EV_Sales ELSE 0 END) as BEV_Sales,
        SUM(CASE WHEN Vehicle_Type = 'PHEV' THEN EV_Sales ELSE 0 END) as PHEV_Sales
    FROM ev_sales
    GROUP BY Year
    ORDER BY Year
""")

conn.execute("""
    CREATE OR REPLACE VIEW top_countries_latest AS
    SELECT 
        Country,
        EV_Sales,
        ROUND(EV_Sales * 100.0 / SUM(EV_Sales) OVER (), 2) as Percentage
    FROM ev_sales
    WHERE Year = 2024 AND Vehicle_Type = 'Total'
    ORDER BY EV_Sales DESC
    LIMIT 10
""")

conn.execute("""
    CREATE OR REPLACE VIEW country_growth AS
    SELECT 
        Country,
        MIN(CASE WHEN Year = 2015 THEN EV_Sales END) as Sales_2015,
        MAX(CASE WHEN Year = 2024 THEN EV_Sales END) as Sales_2024,
        ROUND((MAX(CASE WHEN Year = 2024 THEN EV_Sales END) * 1.0 / 
               MIN(CASE WHEN Year = 2015 THEN EV_Sales END)) - 1, 2) * 100 as Growth_Percentage
    FROM ev_sales
    WHERE Vehicle_Type = 'Total'
    GROUP BY Country
    HAVING Sales_2015 IS NOT NULL AND Sales_2024 IS NOT NULL
    ORDER BY Growth_Percentage DESC
""")

print("✅ Data loaded into DuckDB with analytical views")

# Test queries
print("\n=== Database Summary ===")
result = conn.execute("SELECT COUNT(DISTINCT Country) as countries, COUNT(DISTINCT Year) as years FROM ev_sales").fetchone()
print(f"Countries: {result[0]}, Years: {result[1]}")

result = conn.execute("SELECT Year, Total_Sales FROM ev_sales_by_year ORDER BY Year DESC LIMIT 3").fetchall()
print("\nRecent global sales:")
for row in result:
    print(f"  {row[0]}: {row[1]:,} vehicles")

result = conn.execute("SELECT Country, EV_Sales, Percentage FROM top_countries_latest LIMIT 5").fetchall()
print("\nTop 5 countries in 2024:")
for row in result:
    print(f"  {row[0]}: {row[1]:,} vehicles ({row[2]}%)")

conn.close()

print("\n✅ Database ready for Visivo dashboard!")