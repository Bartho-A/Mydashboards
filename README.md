# Rare Earth Minerals Outlook Dashboard (to 2029)

This interactive dashboard provides insights into the production and capacity trends of rare earth minerals and critical commodities globally, projecting trends up to 2029. It allows users to explore, filter, and visualize mineral data using multiple charts and interactive maps.

# Data Source
The dataset used in this dashboard is publicly available from the US Geological Survey. World Rare Earth Minerals Outlook to 2029: 
```bash
Download the dataset
wget https://www.sciencebase.gov/catalog/file/get/67b8b168d34e1a2e835b7e6c
```

# Features
Interactive Map: Global distribution of mineral quantities by year.
Heatmap: Compare quantities across commodities and years.
Charts:
Bar chart for total quantities by commodity.
Pie chart showing proportion of quantities by commodity.
Line chart to track trends over time.
Filters: Customize the data by year range, commodity, geographic region, and notes.
Raw Data Viewer: Expandable table to inspect the dataset.
Metrics Overview: Total quantity, number of commodities, and most recent year displayed at a glance.

# Technologies Used
Python 3
Streamlit￼ – For the interactive dashboard
Pandas￼ – Data manipulation and cleaning
NumPy￼ – Numerical operations
Matplotlib￼ – Basic plotting (optional)
Seaborn￼ – Statistical visualizations (optional)
Plotly￼ – Interactive charts and maps

# Running the App
streamlit run streamlitapp.py

# Future Improvements
Add forecast modeling for mineral demand and production.
Include additional data sources for better coverage.
Enable user-uploaded datasets.
Add download functionality for filtered data and charts
