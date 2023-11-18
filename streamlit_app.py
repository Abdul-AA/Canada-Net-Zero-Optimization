import streamlit as st
import plotly.express as px
import pandas as pd

# Set page config
st.set_page_config(page_title="Canada Net Zero", page_icon="🌍", layout="wide")

import pandas as pd

# Function to create and preprocess DataFrame with updated data
def create_dataframe_updated():
    data_2025 = {
        'Year': [2025] * 8,
        'Source': ['Wind', 'Solar', 'Oil', 'Nuclear', 'Hydro', 'Natural Gas', 'Coal & Coke', 'Biomass & Geothermal'],
        'Generation (GWh)': [64389.48, 0.0, 1379.91, 78631.37, 402575.9, 48364.54, 8184.54, 8281.2],
        'Emissions (MTCO2e)': [0.0, 0.0, 0.5105667, 0.0, 0.0, 17.8948798, 6.2202504, 0.0],
        'Cost (CAD)': [5204601668.4, 0.0, 85071451.5, 7002123498.5, 12133637626.0, 4704418805.8, 683982007.8, 680714640.0]
    }

    data_2030 = {
        'Year': [2030] * 8,
        'Source': ['Wind', 'Solar', 'Oil', 'Nuclear', 'Hydro', 'Natural Gas', 'Coal & Coke', 'Biomass & Geothermal'],
        'Generation (GWh)': [151989.48, 0.0, 1379.91, 126811.37, 402575.9, 3368.82, 0.0, 8281.2],
        'Emissions (MTCO2e)': [0.0, 0.0, 0.5105667, 0.0, 0.0, 1.2464634, 0.0, 0.0],
        'Cost (CAD)': [12285309668.4, 0.0, 85071451.5, 11292552498.5, 12133637626.0, 327685121.4, 0.0, 680714640.0]
    }

    data_2035 = {
        'Year': [2035] * 8,
        'Source': ['Wind', 'Solar', 'Oil', 'Nuclear', 'Hydro', 'Natural Gas', 'Coal & Coke', 'Biomass & Geothermal'],
        'Generation (GWh)': [239589.48, 10583.16, 0.0, 126811.37, 402575.9, 0.0027, 0.0, 8281.2],
        'Emissions (MTCO2e)': [0.0, 0.0, 0.0, 0.0, 0.0, 1e-06, 0.0, 0.0],
        'Cost (CAD)': [19366017668.4, 2174838824.54, 0.0, 11292552498.5, 12133637626.0, 262.92, 0.0, 680714640.0]
    }

    # Combine all data into one DataFrame
    df_2025 = pd.DataFrame(data_2025)
    df_2030 = pd.DataFrame(data_2030)
    df_2035 = pd.DataFrame(data_2035)

    return pd.concat([df_2025, df_2030, df_2035], ignore_index=True)

# Use the updated function to create the DataFrame
df = create_dataframe_updated()


tab1, tab2 = st.tabs([" Optimal Allocations", "Capacity Decisions & Emissions"])
with tab1:
# Dashboard title
    st.title("Net Zero Emissions Dashboard")
    
    # Sidebar for filters
    year_options = ['All'] + sorted(df['Year'].unique().tolist())
    year_filter = st.selectbox("Select the Year", options=year_options)
    if year_filter == 'All':
        filtered_df = df
    else:
        filtered_df = df[df['Year'] == year_filter]
    
    # KPIs
    total_emission = filtered_df['Emissions (MTCO2e)'].sum()
    total_cost = filtered_df['Cost (CAD)'].sum()
    
    # Layout using containers and columns
    kpi1, kpi2 = st.columns(2)
    kpi1.metric("Total Emissions (MTCO2e)", f"{total_emission:.2f}")
    kpi2.metric("Total Cost (CAD)", f"${total_cost:,.2f}")
    
    # Charts layout
    chart1, chart2 = st.columns(2)
    with chart1:
        st.markdown("### Generation by Source")
        fig1 = px.bar(filtered_df, x='Source', y='Generation (GWh)', color='Source')
        st.plotly_chart(fig1)
    
    with chart2:
        st.markdown("### Emissions by Source")
        fig2 = px.bar(filtered_df, x='Source', y='Emissions (MTCO2e)', color='Source')
        st.plotly_chart(fig2)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Cost by Source")
        fig3 = px.bar(filtered_df, x='Source', y='Cost (CAD)', color='Source')
        st.plotly_chart(fig3)
    with col2:
        st.markdown("### Detailed Data View")
        st.dataframe(filtered_df)


# Second page of the app
import streamlit as st

# Second page of the app
with tab2:
    st.title("Power Plant Decisions and Impacts")

    # Top containers for binary decisions and added capacities
    container1, container2 = st.columns(2)

    with container1:
        st.subheader("Power Plant Opening Decisions")
        # Display binary decisions
        decisions_2025 = {'Wind': 'No', 'Solar': 'No', 'Nuclear': 'No'}
        decisions_2030 = {'Wind': 'Yes', 'Solar': 'No', 'Nuclear': 'Yes'}
        decisions_2035 = {'Wind': 'Yes', 'Solar': 'No', 'Nuclear': 'No'}
        years_decisions = {2025: decisions_2025, 2030: decisions_2030, 2035: decisions_2035}

        for year, decisions in years_decisions.items():
            st.markdown(f"#### Year {year}")
            for source, opened in decisions.items():
                st.markdown(f"{source} Power Plant Opened: {opened}")

    with container2:
        st.subheader("Added Capacities")
        # Display added capacities
        capacities_2030 = {'Wind': 43800, 'Solar': 0, 'Nuclear': 48180}
        capacities_2035 = {'Wind': 43800, 'Solar': 0, 'Nuclear': 0}
        years_capacities = {2030: capacities_2030, 2035: capacities_2035}

        for year, capacities in years_capacities.items():
            st.markdown(f"#### Year {year}")
            for source, capacity in capacities.items():
                st.markdown(f"{source} Added Capacity: {capacity} GWh")

    # Bottom containers for costs and emission deviation
    container3, container4 = st.columns(2)

    with container3:
        st.subheader("Associated Costs")
        # Display costs
        costs_2030 = {'Wind': 8220000000, 'Nuclear': 9590000000}
        costs_2035 = {'Wind': 8220000000}
        years_costs = {2030: costs_2030, 2035: costs_2035}

        for year, costs in years_costs.items():
            st.markdown(f"#### Year {year}")
            for source, cost in costs.items():
                st.markdown(f"{source} Cost: {cost} CAD")

    with container4:
        st.subheader("Emission Deviations")
        # Display emission deviations
        deviations = {2025: 0.0, 2030: 0.0, 2035: 1e-06}
        for year, deviation in deviations.items():
            st.markdown(f"Emission Deviation for {year}: {deviation} MTCO2e")

# Ensure the rest of your Streamlit app code is appropriately placed
