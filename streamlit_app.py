import streamlit as st
import plotly.express as px
import pandas as pd

# Set page config
st.set_page_config(page_title="Canada Net Zero", page_icon="🌍", layout="wide")


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



def format_decision(decision):
    color = 'green' if decision == 'Yes' else 'red'
    return f"<span style='color: {color};'>{decision}</span>"

# Function to format source name with color
def format_source(source):
    colors = {'Wind': 'blue', 'Solar': 'orange', 'Nuclear': 'purple'}
    return f"<span style='color: {colors[source]}; font-weight:bold;'>{source}</span>"

# Function to format values with color
def format_value(value, color='black'):
    return f"<span style='color: {color};'>{value}</span>"

# Function to aggregate data across all years
def aggregate_data(capacities, costs):
    agg_capacities = {source: sum(years.get(source, 0) for years in capacities.values()) for source in ['Wind', 'Solar', 'Nuclear']}
    agg_costs = {source: sum(years.get(source, 0) for years in costs.values()) for source in ['Wind', 'Solar', 'Nuclear']}
    return agg_capacities, agg_costs

# Initialize data (placeholders for actual data)
decisions = {
    2025: {'Wind': 'No', 'Solar': 'No', 'Nuclear': 'No'},
    2030: {'Wind': 'Yes', 'Solar': 'No', 'Nuclear': 'Yes'},
    2035: {'Wind': 'Yes', 'Solar': 'No', 'Nuclear': 'No'}
}
capacities = {
    2030: {'Wind': 43800, 'Solar': 0, 'Nuclear': 48180},
    2035: {'Wind': 43800, 'Solar': 0, 'Nuclear': 0}
}
costs = {
    2030: {'Wind': 8220000000, 'Nuclear': 9590000000},
    2035: {'Wind': 8220000000}
}
deviations = {2025: 0.0, 2030: 0.0, 2035: 1e-06}



# Tab 2 Content
with tab2:
    st.title("Power Plant Decisions and Impacts")

    # Year filter with 'All' option
    year_options = ['All', 2025, 2030, 2035]
    selected_year = st.selectbox("Select Year", options=year_options)

    # Display aggregated data for 'All' years
    if selected_year == 'All':
        agg_capacities, agg_costs = aggregate_data(capacities, costs)
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Aggregated Added Capacities Across All Years")
            for source, capacity in agg_capacities.items():
                st.markdown(f"{format_source(source)} Total Added Capacity: {format_value(capacity, 'blue')} GWh", unsafe_allow_html=True)

        with col2:
            st.subheader("Aggregated Associated Costs Across All Years")
            for source, cost in agg_costs.items():
                st.markdown(f"{format_source(source)} Total Cost: {format_value(cost, 'blue')} CAD", unsafe_allow_html=True)

        for year, year_decisions in decisions.items():
            with st.container():
                st.subheader(f"Power Plant Opening Decisions in {year}")
                for source, opened in year_decisions.items():
                    st.markdown(f"{format_source(source)} Power Plant Opened: {format_decision(opened)}", unsafe_allow_html=True)

    # Display data for a specific year
    else:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader(f"Power Plant Opening Decisions in {selected_year}")
            for source, opened in decisions.get(selected_year, {}).items():
                st.markdown(f"{format_source(source)} Power Plant Opened: {format_decision(opened)}", unsafe_allow_html=True)

            st.subheader(f"Added Capacities in {selected_year}")
            year_capacities = capacities.get(selected_year, {})
            for source, capacity in year_capacities.items():
                st.markdown(f"{format_source(source)} Added Capacity: {format_value(capacity, 'blue')} GWh", unsafe_allow_html=True)

        with col2:
            st.subheader(f"Associated Costs in {selected_year}")
            year_costs = costs.get(selected_year, {})
            for source, cost in year_costs.items():
                st.markdown(f"{format_source(source)} Cost: {format_value(cost, 'blue')} CAD", unsafe_allow_html=True)

            st.subheader(f"Emission Deviations in {selected_year}")
            st.markdown(f"Emission Deviation: {format_value(deviations.get(selected_year, 'N/A'), 'red')} MTCO2e", unsafe_allow_html=True)
