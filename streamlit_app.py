import streamlit as st
import plotly.express as px
import pandas as pd

# Set page config
st.set_page_config(page_title="Net Zero Emissions Dashboard", page_icon="🌍", layout="wide")

# Function to create and preprocess DataFrame
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


# Model results for capacity decisions
capacity_decisions = {
    2025: {'Wind': [False, False], 'Solar': [False, False], 'Nuclear': [False, False]},
    2030: {'Wind': [True, True], 'Solar': [False, False], 'Nuclear': [True, True]},
    2035: {'Wind': [True, False], 'Solar': [False, False], 'Nuclear': [True, True]}
}

# Emission Deviations
emission_deviation = {
    2025: 2.5439801724798365,
    2030: 0.0,
    2035: 0.0
}

# Dashboard title
st.title("Net Zero Emissions Dashboard")

# Multi-page layout
page = st.sidebar.selectbox("Choose a Page", ["Summary", "Detailed Analysis"])

if page == "Summary":
    # Summary page
    st.header("Summary")

    # KPIs
    total_emission = df['Emissions (MTCO2e)'].sum()
    total_cost = df['Cost (USD)'].sum()

    # Layout using containers and columns
    kpi1, kpi2 = st.columns(2)
    kpi1.metric("Total Emissions (MTCO2e)", f"{total_emission:.2f}")
    kpi2.metric("Total Cost (USD)", f"${total_cost:,.2f}")

    # Charts layout
    chart1, chart2, chart3 = st.columns(3)
    with chart1:
        st.markdown("### Generation by Source")
        fig1 = px.bar(df, x='Source', y='Generation (GWh)', color='Source')
        st.plotly_chart(fig1)

    with chart2:
        st.markdown("### Emissions by Source")
        fig2 = px.bar(df, x='Source', y='Emissions (MTCO2e)', color='Source')
        st.plotly_chart(fig2)

    with chart3:
        st.markdown("### Cost by Source")
        fig3 = px.bar(df, x='Source', y='Cost (USD)', color='Source')
        st.plotly_chart(fig3)

elif page == "Detailed Analysis":
    # Detailed Analysis page
    st.header("Detailed Analysis")

    # Year selection
    year = st.selectbox("Select Year", [2025, 2030, 2035])

    # Display capacity decisions and costs
    st.subheader(f"Capacity Increase Decisions for {year}")
    for source, decisions in capacity_decisions[year].items():
        for i, decision in enumerate(decisions):
            plant_status = "Opened" if decision else "Not Opened"
            color = "green" if decision else "red"
            st.markdown(f"<span style='color: {color};'>**{source} Power Plant {i+1}:** {plant_status}</span>", unsafe_allow_html=True)

    # Display total capacity and cost
    st.subheader("Total Costs and Emissions")
    total_emission_year = df[df['Year'] == year]['Emissions (MTCO2e)'].sum()
    total_cost_year = df[df['Year'] == year]['Cost (USD)'].sum()
    emission_color = "green" if emission_deviation[year] == 0 else "red"
    st.markdown(f"<span style='color: {emission_color};'>**Total Emissions in {year} (MTCO2e):** {total_emission_year:.2f}</span>", unsafe_allow_html=True)
    st.markdown(f"**Total Cost in {year} (USD):** ${total_cost_year:,.2f}")

    # Emission deviation
    deviation_color = "green" if emission_deviation[year] == 0 else "red"
    st.markdown(f"<span style='color: {deviation_color};'>**Emission Deviation in {year}:** {emission_deviation[year]}</span>", unsafe_allow_html=True)

# Run the app
st.run()
