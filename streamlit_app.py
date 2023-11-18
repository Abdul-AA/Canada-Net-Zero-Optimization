import streamlit as st
import plotly.express as px
import pandas as pd

# Set page config
st.set_page_config(page_title="Net Zero Emissions Dashboard", page_icon="🌍", layout="wide")

# Function to create and preprocess DataFrame
def create_dataframe():
    # Data for the years 2025, 2030, and 2035
    data = {
        # Data for the year 2025
        2025: {
            'Source': ['Wind', 'Solar', 'Oil', 'Nuclear', 'Hydro', 'Natural Gas', 'Coal & Coke', 'Biomass & Geothermal'],
            'Generation (GWh)': [64389.48, 12184.23, 1379.91, 78631.37, 402575.9, 100603.82, 0.0, 8281.2],
            'Emissions (MTCO2e)': [0.0, 0.0, 0.5105667, 0.0, 0.0, 37.223413472479834, 0.0, 0.0],
            'Cost (USD)': [3798979320.0, 1827634470.6162817, 62095950.0, 5111039050.0, 8856669800.0, 7142871233.908293, 0.0, 496872000.00000006],
            'Emission Deviation': 2.5439801724798365
        },
        # Data for the year 2030
        2030: {
            'Source': ['Wind', 'Solar', 'Oil', 'Nuclear', 'Hydro', 'Natural Gas', 'Coal & Coke', 'Biomass & Geothermal'],
            'Generation (GWh)': [151989.48, 0.0, 1379.91, 174991.37, 402575.9, 30810.47, 0.0, 8281.2],
            'Emissions (MTCO2e)': [0.0, 0.0, 0.5105667, 0.0, 0.0, 11.399873899999957, 0.0, 0.0],
            'Cost (USD)': [8967379320.000002, 0.0, 62095950.0, 11374439050.0, 8856669800.0, 2187543369.999992, 0.0, 496872000.00000006],
            'Emission Deviation': 0.0
        },
        # Data for the year 2035
        2035: {
            'Source': ['Wind', 'Solar', 'Oil', 'Nuclear', 'Hydro', 'Natural Gas', 'Coal & Coke', 'Biomass & Geothermal'],
            'Generation (GWh)': [195789.48, 8357.67, 0.0, 271351.37, 402575.9, 0.0, 0.0, 8281.2],
            'Emissions (MTCO2e)': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            'Cost (USD)': [11551579320.0, 1253650499.9999976, 0.0, 17637839050.0, 8856669800.0, 0.0, 0.0, 496872000.00000006],
            'Emission Deviation': 0.0
        }
    }

    frames = []
    for year, year_data in data.items():
        df_year = pd.DataFrame(year_data)
        df_year['Year'] = year
        frames.append(df_year)

    return pd.concat(frames, ignore_index=True)

df = create_dataframe()





# Adding a tab structure for multiple pages
tab1, tab2 = st.tabs(["Emissions & Costs", "Capacity Decisions"])

with tab1:
    # First Page: Emissions & Costs
    year_filter = st.selectbox("Select the Year", options=['All'] + sorted(df['Year'].unique().tolist()))
    if year_filter == 'All':
        filtered_df = df
    else:
        filtered_df = df[df['Year'] == int(year_filter)]

    # KPIs
    total_emission = filtered_df['Emissions (MTCO2e)'].sum()
    total_cost = filtered_df['Cost (USD)'].sum()

    # Layout using containers and columns
    kpi1, kpi2 = st.columns(2)
    kpi1.metric("Total Emissions (MTCO2e)", f"{total_emission:.2f}")
    kpi2.metric("Total Cost (USD)", f"${total_cost:,.2f}")

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
        fig3 = px.bar(filtered_df, x='Source', y='Cost (USD)', color='Source')
        st.plotly_chart(fig3)

    with col2:
        st.markdown("### Detailed Data View")
        st.dataframe(filtered_df)

with tab2:
    # Second Page: Capacity Decisions
    st.markdown("## Capacity Increase Decisions and Emission Deviations")

    # Capacity increase costs and amounts
    Increase_Cost = {
        'Nuclear': [7e9, 7e9, 7e9],
        'Solar': [9.4e9, 9.4e9, 9.4e9],
        'Wind': [3e9, 3e9, 3e9]
    }

    Capacity_Added = {
        'Nuclear': [48180, 48180, 48180],
        'Solar': [139809.6, 139809.6, 139809.6],
        'Wind': [43800, 43800, 43800]
    }

    for year in [2025, 2030, 2035]:
        st.markdown(f"### Year: {year}")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### Emission Deviations")
            deviation_color = "green" if df[df['Year'] == year]['Emission Deviation'].iloc[0] == 0 else "red"
            st.metric("Emission Deviation (MTCO2e)", df[df['Year'] == year]['Emission Deviation'].iloc[0], delta_color=deviation_color)

        with col2:
            st.markdown("#### Capacity Increase Decisions")
            for source in ['Wind', 'Solar', 'Nuclear']:
                decisions = df[df['Year'] == year]['Capacity Increase Decisions'].iloc[0][source]
                total_capacity_added = sum(Capacity_Added[source][i] * decision for i, decision in enumerate(decisions))
                total_cost = sum(Increase_Cost[source][i] * decision for i, decision in enumerate(decisions))

                st.metric(f"{source} - Total Capacity Added", f"{total_capacity_added} GWh")
                st.metric(f"{source} - Total Cost", f"${total_cost:,.2f}", delta_color="inverse")
