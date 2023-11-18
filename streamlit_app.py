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
    st.title("Canada Net Zero")
    
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
    kpi1.metric("Total Emissions (MTCO2e)", f"{total_emission:.2f}",delta=None, delta_color="inverse")
    kpi2.metric("Total Cost (CAD)", f"${total_cost:,.2f}",delta=None, delta_color="inverse")
    
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





def main():
    tab2 = st.container()
    
    with tab2:
        st.title("Power Plant Decisions and Impacts")

        # Year filter with 'All' option
        year_options = ['All', 2025, 2030, 2035]
        selected_year = st.selectbox("Select Year", options=year_options)

        # Data setup for capacity increase decisions and capacities added
        capacity_decision = {
            'Wind': [(0.0, 0.0), (1.0, 1.0), (1.0, 1.0)],
            'Solar': [(0.0, 0.0), (0.0, 0.0), (0.0, 0.0)],
            'Nuclear': [(0.0, 0.0), (1.0, 0.0), (0.0, 0.0)]
        }
        capacity_added = {
            'Wind': [0.0, 87600.0*2, 87600.0*2],
            'Solar': [0.0, 0.0, 0.0],
            'Nuclear': [0.0, 48180.0, 0.0]
        }
        cost_per_unit = {
            'Wind': [0.0, 1000.0, 1000.0],
            'Solar': [0.0, 0.0, 0.0],
            'Nuclear': [0.0, 2000.0, 2000.0]
        }

        # Display the results using columns and metrics
        col1, col2 = st.columns(2)
        for source in ['Wind', 'Solar', 'Nuclear']:
            for idx, year in enumerate(year_options[1:]):  # Exclude 'All'
                decision_1, decision_2 = capacity_decision[source][idx]
                total_capacity = capacity_added[source][idx]
                total_cost = total_capacity * cost_per_unit[source][idx]

                with col1:
                    st.metric(label=f"{year} {source} Decisions", value=f"{'Yes' if decision_1 else 'No'} & {'Yes' if decision_2 else 'No'}")
                    st.metric(label=f"Total Capacity Added (GWh)", value=f"{total_capacity}")
                
                with col2:
                    st.metric(label=f"Total Cost (CAD)", value=f"${total_cost:,.2f}")

        # Emission Deviations using metrics
        st.markdown("## Emission Deviations from Goals")
        for idx, year in enumerate(year_options[1:]):
            st.metric(label=f"{year} Emission Deviation", value=f"{emission_deviations[idx]} MTCO2e")

if __name__ == '__main__':
    main()

    file_name='dashboard_data.csv',
    mime='text/csv',
)

