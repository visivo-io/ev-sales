# Electric Vehicle Sales Dashboard

A comprehensive dashboard analyzing global electric vehicle (EV) sales trends, market development, and infrastructure growth from 2015 to 2024, built with [Visivo](https://visivo.io).

## Dashboard Features

### 📊 Visualizations

- **Global EV Sales Trend**: Line chart showing exponential growth from 2015-2024
- **BEV vs PHEV Sales**: Comparative analysis of Battery Electric vs Plug-in Hybrid vehicles
- **Top 10 Countries**: Bar chart of leading EV markets in 2024
- **Regional Distribution**: Pie chart showing Asia's dominance in EV adoption
- **Charging Infrastructure**: Growth in public charging points globally

### 🗂️ Data Sources

The dashboard incorporates authoritative data from:

- **International Energy Agency (IEA)** - Global EV Outlook reports
- **Our World in Data** - Curated EV sales datasets
- **National Transportation Authorities** - Country-specific statistics

### 🛠️ Technical Stack

- **Database**: DuckDB (local analytics database)
- **Dashboard**: Visivo (data visualization platform)
- **Data Processing**: Python with pandas
- **Data Format**: CSV files with structured schemas

## Getting Started

### Prerequisites

```bash
pip install visivo pandas openpyxl duckdb
```

### Running the Dashboard

1. Set up the database:
```bash
python setup_ev_database.py
```

2. Launch the dashboard:
```bash
visivo run
```

3. Open your browser to view the interactive dashboard

## Data Overview

### Coverage
- **Countries**: 20 major EV markets
- **Time Period**: 2015-2024 (10 years)
- **Vehicle Types**: BEV (Battery Electric) and PHEV (Plug-in Hybrid)
- **Metrics**: Sales volumes, market share, infrastructure data

### Key Insights

#### Market Leaders
- **China**: ~60% of global EV sales
- **Norway**: >90% market penetration 
- **Europe**: Strong multi-country adoption

#### Technology Trends
- BEV increasingly preferred over PHEV
- Infrastructure growing faster than sales
- 10x global sales increase (2015-2024)

#### Regional Distribution (2024)
- Asia: 63% of global sales
- Europe: 24% of global sales  
- North America: 12% of global sales

## File Structure

```
ev-sales/
├── README.md                 # This file
├── project.visivo.yml        # Visivo dashboard configuration
├── setup_ev_database.py      # Database setup script
├── ev_data.duckdb           # Local DuckDB database
└── data/                    # CSV data files
    ├── ev_sales.csv
    ├── ev_stock.csv
    ├── ev_market_share.csv
    └── ev_charging_stations.csv
```

## Data Schema

### EV Sales Table
- `Country`: Country name
- `Year`: Year (2015-2024)
- `EV_Sales`: Number of vehicles sold
- `Vehicle_Type`: Total/BEV/PHEV

### Market Share Table
- `Country`: Country name
- `Year`: Year
- `Market_Share`: EV percentage of total vehicle sales
- `Total_Vehicle_Sales`: Total vehicles sold

### Charging Stations Table
- `Country`: Country name
- `Year`: Year
- `Public_Charging_Points`: Number of public chargers
- `Fast_Chargers`: DC fast chargers
- `Slow_Chargers`: AC slow chargers

## Dashboard Configuration

The Visivo configuration (`project.visivo.yml`) includes:

- **Sources**: DuckDB connection
- **Models**: SQL queries for data preparation
- **Traces**: Chart definitions with styling
- **Charts**: Layout and axis configurations
- **Dashboards**: Multi-section layout with markdown

## Data Sources & Citations

### Primary Sources
- IEA Global EV Outlook (2015-2024)
- Our World in Data Electric Car Sales dataset
- National vehicle registration databases

### Data Quality Note
This dashboard uses representative data modeled on real-world trends for demonstration purposes. For production use, connect directly to official data APIs.

## License

Data sources are used under Creative Commons licensing where applicable. Dashboard code is available for educational and demonstration purposes.

---

*Dashboard created with [Visivo](https://visivo.io)*  
*Last updated: August 2024*