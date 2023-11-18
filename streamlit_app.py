import streamlit as st
import pandas as pd
import plotly.express as px

# Set page config
st.set_page_config(page_title="Net Zero Emissions Dashboard", page_icon="🌍", layout="wide")

# Function to create and preprocess DataFrame
def create_dataframe():
    # Your data for each year
    data = {
        2025: {
            'Wind': [64389.48, 0.0, 5204601668.4, False, False],
            'Solar': [0.0, 0.0, 0.0, False, False],
            'Oil': [1379.91, 0.5105667, 85071451.5],
            'Nuclear': [78631.37, 0.0, 7002123498.5, False, False],
            'Hydro': [402575.9, 0.0, 12133637626.0],
            'Natural Gas': [100603.82, 37.223413472479834, 7142871233.908293],
            'Coal & Coke': [0.0, 0.0, 0.0],
            'Biomass & Geothermal': [8281.2, 0.0, 496872000.0],
            'Emission Deviation': 2.5439801724798365
        },
        2030: {
            'Wind': [151989.48, 0.0, 12285309668.4, True, True],
            'Solar': [0.0, 0.0, 0.0, False, False],
            'Oil': [1379.91, 0.5105667, 85071451.5],
            'Nuclear': [174991.37, 0.0, 11374439050.0, True, True],
            'Hydro': [402575.9, 0.0, 12133637626.0],
            'Natural Gas': [30810.47, 11.399873899999957, 2187543369.999992],
            'Coal & Coke': [0.0, 0.0, 0.0],
            'Biomass & Geothermal': [8281.2, 0.0, 496872000.0],
            'Emission Deviation': 0.0
        },
        2035: {
            'Wind': [195789.48, 0.0, 19366017668.4, True, False],
            'Solar': [8357.67, 0.0, 1253650499.9999976, False, False],
            'Oil': [0.0, 0.0, 0.0],
            'Nuclear': [271351.37, 0.0, 17637839050.0, True, True],
            'Hydro': [402575.9, 0.0, 12133637626.0],
            'Natural Gas': [0.0, 0.0, 0.0],
            'Coal & Coke': [0.0, 0.0, 0.0],
            'Biomass & Geothermal': [8281.2, 0.0, 496872000.0],
            'Emission Deviation': 1e-06
        }
    }

    # Flattening data for DataFrame
    flat_data = []
    for year, sources in data.items():
        for source, values in sources.items():
            if source != 'Emission Deviation':
                generation, emissions, cost, *decisions = values
                flat_data.append([year, source, generation, emissions, cost] + decisions)
            else:
                flat_data.append([year, 'Emission Deviation', '', '', '', values, ''])

    # Create DataFrame
    df = pd.DataFrame(flat_data, columns=['Year', 'Source', 'Generation (GWh)', 'Emissions (MTCO2e)', 'Cost (CAD)', 'First Plant', 'Second Plant'])
    return df

df = create_dataframe()

# Streamlit App with Tabs
tab1, tab2 = st.tabs(["General Data", "Capacity Decisions & Emissions"])

with tab1:
    # Code for the first page (General Data)
    year_filter = st.selectbox("Select the Year", options=df['Year'].unique())
    filtered_df = df[df['Year'] == year_filter]

    # Display KPIs and data for selected year
    total_emission = filtered_df['Emissions (MTCO2e)'].sum()
    total_cost = filtered_df['Cost (CAD)'].sum()
    emission_deviation = filtered_df[filtered_df['Source'] == 'Emission Deviation']['First Plant'].iloc[0]
    deviation_color = "green" if emission_deviation == 0 else "red"

    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Total Emissions (MTCO2e)", f"{total_emission:.2f}")
    kpi2.metric("Total Cost (CAD)", f"${total_cost:,.2f}")
    kpi3.metric("Emission Deviation", f"{emission_deviation}", delta_color=deviation_color)

    # Display charts
    chart1, chart2 = st.columns(2)
    with chart1:
        fig1 = px.bar(filtered_df, x='Source', y='Generation (GWh)', color='Source', title='Generation by Source')
        st.plotly_chart(fig1)

    with chart2:
        fig2 = px.bar(filtered_df, x='Source', y='Emissions (MTCO2e)', color='Source', title='Emissions by Source')
        st.plotly_chart(fig2)

    st.write("### Detailed Data View")
    st.dataframe(filtered_df[filtered_df['Source'] != 'Emission Deviation'])

with tab2:
    # Code for the second page (Capacity Decisions & Emissions)
    year_filter = st.selectbox("Select the Year", options=df['Year'].unique(), key='year2')
    filtered_df = df[df['Year'] == year_filter]

    # Capacity Increase Decisions, Costs, and Emissions
    st.write("### Capacity Increase Decisions, Costs, and Emissions")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.write("#### Capacity Increase Decisions")
        st.write(filtered_df[['Source', 'First Plant', 'Second Plant']])

    with col2:
        st.write("#### Costs & Added Capacity")
        # Calculate the costs and added capacity based on decisions
        capacity_increase_data = []
        for index, row in filtered_df.iterrows():
            if row['Source'] in ['Wind', 'Solar', 'Nuclear']:
                first_plant = 'Yes' if row['First Plant'] else 'No'
                second_plant = 'Yes' if row['Second Plant'] else 'No'
                total_capacity_added = (1 if row['First Plant'] else 0) + (1 if row['Second Plant'] else 0)
                capacity_increase_data.append([row['Source'], first_plant, second_plant, total_capacity_added])
        capacity_df = pd.DataFrame(capacity_increase_data, columns=['Source', 'First Plant', 'Second Plant', 'Total Capacity Added'])
        st.write(capacity_df)

    with col3:
        st.write("#### Emission Deviations")
        st.metric("Emission Deviation", f"{emission_deviation}", delta_color=deviation_color)

# [Insert any additional code or features as required]
