# Dashboard for World minerals outlook to 2029

# import libraries
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# page configuration
st.set_page_config(page_title="Rare Earth Minerals Outlook Dashboard", layout="wide")

st.title("Rare Earth Minerals Outlook Dashboard")

# You can add introductory text or instructions here
st.markdown(
    """
    Welcome to the Rare Earth Minerals Outlook Dashboard.  
    Explore production and capacity trends for critical mineral commodities through 2029.
    """
)

# load data
@st.cache_data
def load_data(file_path):
    df = pd.read_csv(file_path)
    # Drop unnecessary columns (example)
    cols_to_drop = [c for c in df.columns if c.startswith('Unnamed') or c in ['Figure_Use', 'Data Sources']]
    df = df.drop(columns=cols_to_drop, errors='ignore')
    # Standardize column names
    df.columns = df.columns.str.strip().str.replace(' ', '_')
    # Rename main column
    df = df.rename(columns={'Mineral_Commodity': 'Commodity'})
    # Convert numeric types
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
    df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')
    # Drop rows with essential missing values
    df = df.dropna(subset=['Commodity', 'Quantity', 'Geographic_Region'])
    return df
    
file_path = "rare_earths_outlook_to_2029.csv"
df = load_data(file_path)

st.write("Data loaded and cleaned!")

# Sidebar filters
st.sidebar.header("Filter Options")

# Year slider
# Sidebar filters
st.sidebar.header("Filter Options")

# Year slider
min_year = int(df['Year'].min())
max_year = int(df['Year'].max())
selected_year = st.sidebar.slider(
    "Year", min_value=min_year, max_value=max_year, value=(min_year, max_year)
)

# Commodity multiselect with default "Cobalt"
commodities = df['Commodity'].unique()
default_commodity = ['Cobalt'] if 'Cobalt' in commodities else commodities
selected_commodities = st.sidebar.multiselect(
    "Commodity", options=commodities, default=default_commodity
)

# Geographic Region multiselect with default "World"
regions = df['Geographic_Region'].unique()
default_region = ['World'] if 'World' in regions else regions
selected_regions = st.sidebar.multiselect(
    "Geographic Region", options=regions, default=default_region
)

# Note multiselect with default "estimated"
notes = df['Note'].dropna().unique()
default_note = ['estimated'] if 'estimated' in notes else notes
selected_notes = st.sidebar.multiselect(
    "Note", options=notes, default=default_note
)

# Filter data based on selections
filtered_df = df[
    (df['Year'] >= selected_year[0]) & (df['Year'] <= selected_year[1]) &
    (df['Commodity'].isin(selected_commodities)) &
    (df['Geographic_Region'].isin(selected_regions)) &
    (df['Note'].isin(selected_notes))
]

st.write(f"Filtered data contains {len(filtered_df)} records.")

# Calculate metrics
total_quantity = filtered_df['Quantity'].sum()
unique_commodities = filtered_df['Commodity'].nunique()
latest_year = int(filtered_df['Year'].max())

# Create 3 columns for display
col1, col2, col3 = st.columns(3)

# Display metrics side-by-side
col1.metric("Total Quantity", f"{total_quantity:,.0f}")
col2.metric("Number of Commodities", unique_commodities)
col3.metric("Most Recent Year", latest_year)

# table expander
with st.expander("View raw data"):
    st.dataframe(df)

import streamlit as st
import plotly.express as px

# Define plot function
def plot_choropleth(data):
    fig = px.choropleth(
        data,
        locations="Geographic_Region",
        locationmode="country names",
        color="Quantity",
        hover_name="Commodity",
        animation_frame="Year",
        color_continuous_scale="Viridis",  # Changed to perceptually better scale
        title="Global Distribution of Rare Earth Mineral Quantities (2000–2029)",
        labels={"Quantity": "Quantity", "Geographic_Region": "Country", "Year": "Year"}
    )
    fig.update_layout(
        coloraxis_colorbar=dict(title="Quantity"),
        margin=dict(l=0, r=0, t=40, b=0),
        geo=dict(showcoastlines=True, coastlinecolor="RebeccaPurple")
    )
    return fig

# Precompute figures for all tabs
fig_map = plot_choropleth(filtered_df)

pivot_df = filtered_df.pivot_table(
    index='Commodity', columns='Year', values='Quantity', aggfunc='sum').fillna(0)

fig_heatmap = px.imshow(
    pivot_df.values,
    labels=dict(x="Year", y="Commodity", color="Quantity"),
    x=pivot_df.columns.astype(str),
    y=pivot_df.index,
    color_continuous_scale='Blues',
    aspect='auto',
    title="Heatmap of Quantities by Commodity and Year"
)
fig_heatmap.update_layout(yaxis=dict(autorange="reversed"), margin=dict(l=50, r=20, t=50, b=50))

agg = filtered_df.groupby('Commodity', as_index=False)['Quantity'].sum().sort_values('Quantity', ascending=False)

bar_fig = px.bar(
    agg,
    x='Commodity',
    y='Quantity',
    color='Commodity',
    color_discrete_sequence=px.colors.qualitative.Set2,
    title="Total Quantity by Commodity (2018–2029)",
    labels={"Quantity": "Total Quantity", "Commodity": "Commodity"}
)

pie_fig = px.pie(
    agg,
    names='Commodity',
    values='Quantity',
    color_discrete_sequence=px.colors.qualitative.Set3,
    title="Proportion of Quantity by Commodity"
)

line_fig = px.line(
    filtered_df,
    x='Year',
    y='Quantity',
    color='Commodity',
    markers=True,
    title="Quantity Trend Over Time by Commodity",
    labels={"Quantity": "Quantity", "Year": "Year"}
)

# Tabs with visualizations
tab1, tab2, tab3, tab4 = st.tabs(["Map", "Heatmap", "Charts", "All Plots"])

with tab1:
    st.header("Map")
    st.plotly_chart(fig_map, use_container_width=True, key="fig_map_tab1")

with tab2:
    st.header("Heatmap of Quantities by Commodity and Year")
    st.plotly_chart(fig_heatmap, use_container_width=True, key="fig_heatmap_tab2")

with tab3:
    st.header("Charts")
    st.plotly_chart(bar_fig, use_container_width=True, key="bar_fig_tab3")
    st.plotly_chart(pie_fig, use_container_width=True, key="pie_fig_tab3")
    st.plotly_chart(line_fig, use_container_width=True, key="line_fig_tab3")

with tab4:
    st.header("All Plots")

    st.subheader("Global Distribution Map")
    st.plotly_chart(fig_map, use_container_width=True, key="fig_map_tab4")

    st.subheader("Heatmap of Quantities by Commodity and Year")
    st.plotly_chart(fig_heatmap, use_container_width=True, key="fig_heatmap_tab4")

    st.subheader("Total Quantity by Commodity")
    st.plotly_chart(bar_fig, use_container_width=True, key="bar_fig_tab4")

    st.subheader("Proportion of Quantity by Commodity")
    st.plotly_chart(pie_fig, use_container_width=True, key="pie_fig_tab4")

    st.subheader("Quantity Trend Over Time by Commodity")
    st.plotly_chart(line_fig, use_container_width=True, key="line_fig_tab4")














