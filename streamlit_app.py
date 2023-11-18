import streamlit as st
import pandas as pd
import plotly.express as px

# Set page config
st.set_page_config(page_title="Net Zero Emissions Dashboard", page_icon="🌍", layout="wide")

# Function to create and preprocess DataFrame
def create_dataframe():
    # Data for 2025
    data_2025 = {
        'Year': 2025,
        'Source': ['Wind', 'Solar', 'Oil', 'Nuclear', 'Hydro', 'Natural Gas', 'Coal & Coke', 'Biomass & Geothermal'],
        'Generation (GWh)': [64389.48, 0.0, 1379.91, 78631.37, 402575.9, 48364.54, 8184.54, 8281.2],
        'Emissions (MTCO2e)': [0.0, 0.0, 0.5105667, 0.0, 0.0, 17.894879799999963, 6.2202504, 0.0],
        'Cost (CAD)': [5204601668.400001, 0.0, 85071451.5, 7002123498.5, 12133637626.0, 4704418805.79999, 683982007.8, 680714640.0000001],
        'Emission Deviation': 0.0
    }

    # Data for 2030
    data_2030 = {
        'Year': 2030,
        'Source': ['Wind', 'Solar', 'Oil', 'Nuclear', 'Hydro', 'Natural Gas', 'Coal & Coke', 'Biomass & Geothermal'],
        'Generation (GWh)': [151989.48, 0.0, 1379.91, 126811.37, 402575.9, 3368.82, 0.0, 8281.2],
        'Emissions (MTCO2e)': [0.0, 0.0, 0.5105667, 0.0, 0.0, 1.2464633999999655, 0.0, 0.0],
        'Cost (CAD)': [12285309668.400003, 0.0, 85071451.5, 11292552498.5, 12133637626.0, 327685121.399991, 0.0, 680714640.0000001],
        'Emission Deviation': 0.0
    }

    # Data for 2035
    data_2035 = {
        'Year': 2035,
        'Source': ['Wind', 'Solar', 'Oil', 'Nuclear', 'Hydro', 'Natural Gas', 'Coal & Coke', 'Biomass & Geothermal'],
        'Generation (GWh)': [239589.48, 10583.16, 0.0, 126811.37, 402575.9, 0.0027, 0.0, 8281.2],
        'Emissions (MTCO2e)': [0.0, 0.0, 0.0, 0.0, 0.0, 1.0001e-06, 0.0, 0.0],
        'Cost (CAD)': [19366017668.4, 2174838824.54, 0.0, 11292552498.5, 12133637626.0, 262.9181810810811, 0.0, 680714640.0000001],
        'Emission Deviation': 1.0001e-06
    }

    df_2025 = pd.DataFrame(data_2025)
    df_2030 = pd.DataFrame(data_2030)
    df_2035 = pd.DataFrame(data_2035)

    return pd.concat([df_2025, df_2030, df_2035], ignore_index=True)

df = create_dataframe()

# Cost and capacity for each power source
cost_per_source = {'Nuclear': 9.59e9, 'Solar': 12.878e9, 'Wind': 4.11e9}
capacity_per_source = {'Nuclear': 48180, 'Solar': 139809.6, 'Wind': 43800}

# Decisions for each year
decisions_2025 = {'Wind': [False, False], 'Solar': [False, False], 'Nuclear': [False, False]}
decisions_2030 = {'Wind': [True, True], 'Solar': [False, False], 'Nuclear': [True, False]}
decisions_2035 = {'Wind': [True, True], 'Solar': [False, False], 'Nuclear': [False, False]}
decisions = {2025: decisions_2025, 2030: decisions_2030, 2035: decisions_2035}

# Streamlit App with Tabs
tab1, tab2 = st.tabs(["General Data", "Capacity Decisions & Emissions"])

with tab1:
    # General Data
    year_filter = st.selectbox("Select the Year", options=df['Year'].unique())
    filtered_df = df[df['Year'] == year_filter]

    # Display charts and data for selected year
    fig1 = px.bar(filtered_df, x='Source', y='Generation (GWh)', color='Source', title='Generation by Source')
    st.plotly_chart(fig1)

    fig2 = px.bar(filtered_df, x='Source', y='Emissions (MTCO2e)', color='Source', title='Emissions by Source')
    st.plotly_chart(fig2)

    fig3 = px.bar(filtered_df, x='Source', y='Cost (CAD)', color='Source', title='Cost by Source')
    st.plotly_chart(fig3)

    st.write("### Detailed Data View")
    st.dataframe(filtered_df[['Source', 'Generation (GWh)', 'Emissions (MTCO2e)', 'Cost (CAD)']])

    # Total emission deviation KPI
    deviation = filtered_df['Emission Deviation'].iloc[0]
    deviation_color = "green" if deviation == 0 else "red"
    st.metric("Total Emission Deviation", f"{deviation:.2f}", delta_color=deviation_color)

with tab2:
    # Capacity Decisions & Emissions
    year_filter = st.selectbox("Select the Year", options=df['Year'].unique(), key='year2')
    decision_year = decisions[year_filter]

    st.write("### Capacity Increase Decisions & Emissions")

    # Layout for decisions
    col1, col2, col3 = st.columns(3)

    with col1:
        st.write("#### Capacity Increase Decisions")
        for source, decision in decision_year.items():
            st.write(f"{source}: {decision}")

    with col2:
        st.write("#### Associated Costs")
        for source, decision in decision_year.items():
            num_plants = sum(decision)
            cost = num_plants * cost_per_source[source]
            st.write(f"{source}: {num_plants} plants, Cost: ${cost:,.2f} CAD")

    with col3:
        st.write("#### Added Capacity (GWh)")
        for source, decision in decision_year.items():
            num_plants = sum(decision)
            capacity = num_plants * capacity_per_source[source]
            st.write(f"{source}: {capacity} GWh")

# Color coding and visual emphasis as required
