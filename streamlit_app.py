import streamlit as st
import plotly.express as px
import pandas as pd

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

    return pd.concat([df_2025, df_2030, df_2035], ignore_index=True)

df = create_dataframe()
# Dashboard title
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

# Charts layout
chart1, chart2, chart3 = st.columns(3)
with chart1:
    st.markdown("### Generation by Source")
    fig1 = px.bar(filtered_df, x='Source', y='Generation (GWh)')
    st.plotly_chart(fig1)

with chart2:
    st.markdown("### Emissions by Source")
    fig2 = px.bar(filtered_df, x='Source', y='Emissions (MTCO2e)')
    st.plotly_chart(fig2)

with chart3:
    st.markdown("### Cost by Source")
    fig3 = px.bar(filtered_df, x='Source', y='Cost (USD)')
    st.plotly_chart(fig3)

# Detailed Data View
st.markdown("### Detailed Data View")
st.dataframe(filtered_df)
This revised code organizes the dashboard into columns, making it more compact and fitting the content into a single view. The error was likely due to the DataFrame not being defined before it was used in the sidebar filters. The create_dataframe function is now correctly invoked before the filters are set up, ensuring that df is defined and can be used for filtering.

User
Have the option to view total across the three time periods
ChatGPT
To add the option to view totals across all three time periods, we can introduce a checkbox in the sidebar. When this checkbox is selected, the dashboard will display totals for all years, irrespective of the year filter selected.

Here's the modified code to include this feature:

python
Copy code
import streamlit as st
import plotly.express as px
import pandas as pd

# Set page config
st.set_page_config(page_title="Net Zero Emissions Dashboard", page_icon="🌍", layout="wide")

# Function to create DataFrame
def create_dataframe():
    # Your data_2025, data_2030, and data_2035 definitions
    # ...

    # Combine all data into one DataFrame
    df_2025 = pd.DataFrame(data_2025)
    df_2030 = pd.DataFrame(data_2030)
    df_2035 = pd.DataFrame(data_2035)

    return pd.concat([df_2025, df_2030, df_2035], ignore_index=True)

df = create_dataframe()

# Dashboard title
st.title("Net Zero Emissions Dashboard")

# Sidebar for filters
year_filter = st.sidebar.selectbox("Select the Year", ['All Years'] + list(df['Year'].unique()))
view_all_years = year_filter == 'All Years'
source_filter = st.sidebar.multiselect("Select Energy Sources", df['Source'].unique(), default=df['Source'].unique())

# Filter the dataframe
if not view_all_years:
    filtered_df = df[(df['Year'] == year_filter) & (df['Source'].isin(source_filter))]
else:
    filtered_df = df[df['Source'].isin(source_filter)]

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
    fig1 = px.bar(filtered_df, x='Source', y='Generation (GWh)', color='Year')
    st.plotly_chart(fig1)

with chart2:
    st.markdown("### Emissions by Source")
    fig2 = px.bar(filtered_df, x='Source', y='Emissions (MTCO2e)', color='Year')
    st.plotly_chart(fig2)

with chart3:
    st.markdown("### Cost by Source")
    fig3 = px.bar(filtered_df, x='Source', y='Cost (USD)', color='Year')
    st.plotly_chart(fig3)

# Detailed Data View
st.markdown("### Detailed Data View")
st.dataframe(filtered_df)
