Copy code
import streamlit as st
import pandas as pd
import plotly.express as px

# Set page config
st.set_page_config(page_title="Net Zero Emissions Dashboard", page_icon="🌍", layout="wide")

# Data for each year
data = {
    2025: {'Source': ['Wind', 'Solar', 'Oil', 'Nuclear', 'Hydro', 'Natural Gas', 'Coal & Coke', 'Biomass & Geothermal'],
           'Generation (GWh)': [64389.48, 12184.23, 1379.91, 78631.37, 402575.9, 100603.82, 0.0, 8281.2],
           'Emissions (MTCO2e)': [0.0, 0.0, 0.5105667, 0.0, 0.0, 37.223413472479834, 0.0, 0.0],
           'Cost (USD)': [3798979320.0, 1827634470.6162817, 62095950.0, 5111039050.0, 8856669800.0, 7142871233.908293, 0.0, 496872000.00000006],
           'Emission Deviation': 2.5439801724798365},
    2030: {'Source': ['Wind', 'Solar', 'Oil', 'Nuclear', 'Hydro', 'Natural Gas', 'Coal & Coke', 'Biomass & Geothermal'],
           'Generation (GWh)': [151989.48, 0.0, 1379.91, 174991.37, 402575.9, 30810.47, 0.0, 8281.2],
           'Emissions (MTCO2e)': [0.0, 0.0, 0.5105667, 0.0, 0.0, 11.399873899999957, 0.0, 0.0],
           'Cost (USD)': [8967379320.000002, 0.0, 62095950.0, 11374439050.0, 8856669800.0, 2187543369.999992, 0.0, 496872000.00000006],
           'Emission Deviation': 0.0},
    2035: {'Source': ['Wind', 'Solar', 'Oil', 'Nuclear', 'Hydro', 'Natural Gas', 'Coal & Coke', 'Biomass & Geothermal'],
           'Generation (GWh)': [195789.48, 8357.67, 0.0, 271351.37, 402575.9, 0.0, 0.0, 8281.2],
           'Emissions (MTCO2e)': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
           'Cost (USD)': [11551579320.0, 1253650499.9999976, 0.0, 17637839050.0, 8856669800.0, 0.0, 0.0, 496872000.00000006],
           'Emission Deviation': 0.0}
}

# Capacity increase decisions
capacity_increase_decisions = {
    2025: {'Wind': [False, False], 'Solar': [False, False], 'Nuclear': [False, False]},
    2030: {'Wind': [True, True], 'Solar': [False, False], 'Nuclear': [True, True]},
    2035: {'Wind': [True, False], 'Solar': [False, False], 'Nuclear': [True, True]}
}

# Capacity increase costs and amounts for each power plant type
increase_cost = {'Nuclear': 7e9, 'Solar': 9.4e9, 'Wind': 3e9}
capacity_added = {'Nuclear': 48180, 'Solar': 139809.6, 'Wind': 43800}

# Function to create and preprocess DataFrame
def create_dataframe():
    all_data = []
    for year, year_data in data.items():
        df_year = pd.DataFrame(year_data)
        df_year['Year'] = year

        # Calculate the total capacity added and total cost for each source
        for source in ['Wind', 'Solar', 'Nuclear']:
            decisions = capacity_increase_decisions[year][source]
            total_added = sum(decisions) * capacity_added[source]
            total_cost = sum(decisions) * increase_cost[source]
            df_year[f'{source} Capacity Added (GWh)'] = total_added
            df_year[f'{source} Capacity Cost (USD)'] = total_cost

        all_data.append(df_year)

    return pd.concat(all_data, ignore_index=True)

# Create the DataFrame
df = create_dataframe()

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

    fig3 = px.bar(filtered_df, x='Source', y='Cost (USD)', color='Source', title='Cost by Source')
    st.plotly_chart(fig3)

    st.write("### Detailed Data View")
    st.dataframe(filtered_df[['Source', 'Generation (GWh)', 'Emissions (MTCO2e)', 'Cost (USD)']])

with tab2:
    # Capacity Decisions & Emissions
    year_filter = st.selectbox("Select the Year", options=df['Year'].unique(), key='year2')
    filtered_df = df[df['Year'] == year_filter]

    st.write("### Capacity Increase Decisions & Emissions")

    # Layout
    col1, col2, col3 = st.columns(3)

    with col1:
        st.write("#### Capacity Increase Decisions")
        for source in ['Wind', 'Solar', 'Nuclear']:
            st.write(f"{source}: {capacity_increase_decisions[year_filter][source]}")

    with col2:
        st.write("#### Associated Costs & Added Capacity")
        for source in ['Wind', 'Solar', 'Nuclear']:
            st.write(f"{source} Capacity Added: {filtered_df[f'{source} Capacity Added (GWh)'].iloc[0]} GWh")
            st.write(f"{source} Capacity Cost: ${filtered_df[f'{source} Capacity Cost (USD)'].iloc[0]:,.2f}")

    with col3:
        st.write("#### Emission Deviations")
        deviation = filtered_df['Emission Deviation'].iloc[0]
        deviation_color = "green" if deviation <= 0 else "red"
        st.metric("Emission Deviation (MTCO2e)", f"{deviation:.2f}", delta_color=deviation_color)
