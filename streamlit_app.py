import streamlit as st
import plotly.express as px
import pandas as pd

# Set page config
st.set_page_config(page_title="Net Zero Emissions Dashboard", page_icon="🌍", layout="wide")

# Prepare the data
def create_dataframe():
    years = [2025, 2030, 2035]
    sources = ['Wind', 'Solar', 'Oil', 'Nuclear', 'Hydro', 'Natural Gas', 'Coal & Coke', 'Biomass & Geothermal']
    generation = [64389.48, 12184.23, 1379.91, 78631.37, 402575.9, 100603.82, 0.0, 8281.2, 
                  151989.48, 0.0, 1379.91, 174991.37, 402575.9, 30810.47, 0.0, 8281.2,
                  195789.48, 8357.67, 0.0, 271351.37, 402575.9, 0.0, 0.0, 8281.2]
    emissions = [0.0, 0.0, 0.5105667, 0.0, 0.0, 37.223413472479834, 0.0, 0.0,
                 0.0, 0.0, 0.5105667, 0.0, 0.0, 11.399873899999957, 0.0, 0.0,
                 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    costs = [3798979320.0, 1827634470.6162817, 62095950.0, 5111039050.0, 8856669800.0, 7142871233.908293, 0.0, 496872000.00000006,
             8967379320.000002, 0.0, 62095950.0, 11374439050.0, 8856669800.0, 2187543369.999992, 0.0, 496872000.00000006,
             11551579320.0, 1253650499.9999976, 0.0, 17637839050.0, 8856669800.0, 0.0, 0.0, 496872000.00000006]

    data = {'Year': years * 3, 'Source': sources * 3, 'Generation (GWh)': generation, 'Emissions (MTCO2e)': emissions, 'Cost (USD)': costs}
    return pd.DataFrame(data)

df = create_dataframe()

# Dashboard title
st.title("Net Zero Emissions Dashboard")

# Sidebar for filters
year_filter = st.sidebar.selectbox("Select the Year", df['Year'].unique())
source_filter = st.sidebar.multiselect("Select Energy Sources", df['Source'].unique(), default=df['Source'].unique())

# Filter the dataframe
filtered_df = df[(df['Year'] == year_filter) & (df['Source'].isin(source_filter))]

# KPIs
total_emission = filtered_df['Emissions (MTCO2e)'].sum()
total_cost = filtered_df['Cost (USD)'].sum()

# Layout using containers and columns
kpi1, kpi2 = st.columns(2)

kpi1.metric("Total Emissions (MTCO2e)", f"{total_emission:.2f}")
kpi2.metric("Total Cost (USD)", f"${total_cost:,.2f}")

# Chart: Generation by Source
fig = px.bar(filtered_df, x='Source', y='Generation (GWh)', title='Generation by Source')
st.plotly_chart(fig)

# Chart: Emissions by Source
fig = px.bar(filtered_df, x='Source', y='Emissions (MTCO2e)', title='Emissions by Source')
st.plotly_chart(fig)

# Chart: Cost by Source
fig = px.bar(filtered_df, x='Source', y='Cost (USD)', title='Cost by Source')
st.plotly_chart(fig)

# Display the filtered data table
st.dataframe(filtered_df)
