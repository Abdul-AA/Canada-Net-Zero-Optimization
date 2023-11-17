import streamlit as st
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
# Set page config
st.set_page_config(page_title="Net Zero Emissions Dashboard", page_icon="🌍", layout="wide")

def create_dataframe():
    data_2025 = {
        'Year': [2025] * 8,
        'Source': ['Wind', 'Solar', 'Oil', 'Nuclear', 'Hydro', 'Natural Gas', 'Coal & Coke', 'Biomass & Geothermal'],
        'Generation (GWh)': [64389.48, 12184.23, 1379.91, 78631.37, 402575.9, 100603.82, 0.0, 8281.2],
        'Emissions (MTCO2e)': [0.0, 0.0, 0.5105667, 0.0, 0.0, 37.223413472479834, 0.0, 0.0],
        'Cost (USD)': [3798979320.0, 1827634470.6162817, 62095950.0, 5111039050.0, 8856669800.0, 7142871233.908293, 0.0, 496872000.00000006]
    }

    data_2030 = {
        'Year': [2030] * 8,
        'Source': ['Wind', 'Solar', 'Oil', 'Nuclear', 'Hydro', 'Natural Gas', 'Coal & Coke', 'Biomass & Geothermal'],
        'Generation (GWh)': [151989.48, 0.0, 1379.91, 174991.37, 402575.9, 30810.47, 0.0, 8281.2],
        'Emissions (MTCO2e)': [0.0, 0.0, 0.5105667, 0.0, 0.0, 11.399873899999957, 0.0, 0.0],
        'Cost (USD)': [8967379320.000002, 0.0, 62095950.0, 11374439050.0, 8856669800.0, 2187543369.999992, 0.0, 496872000.00000006]
    }

    data_2035 = {
        'Year': [2035] * 8,
        'Source': ['Wind', 'Solar', 'Oil', 'Nuclear', 'Hydro', 'Natural Gas', 'Coal & Coke', 'Biomass & Geothermal'],
        'Generation (GWh)': [195789.48, 8357.67, 0.0, 271351.37, 402575.9, 0.0, 0.0, 8281.2],
        'Emissions (MTCO2e)': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        'Cost (USD)': [11551579320.0, 1253650499.9999976, 0.0, 17637839050.0, 8856669800.0, 0.0, 0.0, 496872000.00000006]
    }

    # Combine all data into one DataFrame
    df_2025 = pd.DataFrame(data_2025)
    df_2030 = pd.DataFrame(data_2030)
    df_2035 = pd.DataFrame(data_2035)

    combined_df = pd.concat([pd.DataFrame(data) for data in [data_2025, data_2030, data_2035]], ignore_index=True)
    combined_df['Year'] = pd.to_datetime(combined_df['Year'], format='%Y')
    return combined_df

df = create_dataframe()

# Set page config
st.set_page_config(page_title="Net Zero Emissions Dashboard", page_icon="🌍", layout="wide")

# Dashboard title
st.title("Net Zero Emissions Dashboard")

# Sidebar for filters
year_filter = st.sidebar.selectbox("Select the Year", pd.to_datetime(df['Year'].dt.year.unique(), format='%Y'))

# Filter the dataframe
filtered_df = df[df['Year'].dt.year == year_filter.year]

# KPIs
total_emission = filtered_df['Emissions (MTCO2e)'].sum()
total_cost = filtered_df['Cost (USD)'].sum()

# Layout using containers and columns
kpi1, kpi2 = st.columns(2)
kpi1.metric("Total Emissions (MTCO2e)", f"{total_emission:.2f}")
kpi2.metric("Total Cost (USD)", f"${total_cost:,.2f}")

# Charts layout
chart1, chart2, chart3 = st.columns(3)
with chart1:
    st.markdown("### Generation by Source")
    fig1 = px.bar(filtered_df, x='Source', y='Generation (GWh)', color='Source')
    st.plotly_chart(fig1)

with chart2:
    st.markdown("### Emissions by Source")
    fig2 = px.bar(filtered_df, x='Source', y='Emissions (MTCO2e)', color='Source')
    st.plotly_chart(fig2)

with chart3:
    st.markdown("### Cost by Source")
    fig3 = px.bar(filtered_df, x='Source', y='Cost (USD)', color='Source')
    st.plotly_chart(fig3)

# Detailed Data View
st.markdown("### Detailed Data View")
filtered_df.set_index('Year', inplace=True)
st.dataframe(filtered_df)
