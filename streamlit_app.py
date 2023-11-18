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
        'Generation (GWh)': [64389.48, 0.0, 1379.91, 50079.20, 402575.9, 76916.71, 8184.54, 8281.2],
        'Emissions (MTCO2e)': [0.0, 0.0, 0.5105667, 0.0, 0.0, 28.4591829, 6.2202504, 0.0],
        'Generation Cost (CAD)': [5204601668.4, 0.0, 85071451.5, 4459552711.86, 12133637626.0, 7481688434.28, 683982007.8, 680714640.0],
        'Capacity Investment Cost (CAD)': [0, 0, 0, 0, 0, 0, 0, 0]
    }
    
    data_2030 = {
        'Year': [2030] * 8,
        'Source': ['Wind', 'Solar', 'Oil', 'Nuclear', 'Hydro', 'Natural Gas', 'Coal & Coke', 'Biomass & Geothermal'],
        'Generation (GWh)': [151989.48, 0.0, 1379.91, 53479.02, 402575.9, 76701.17, 0.0, 8281.2],
        'Emissions (MTCO2e)': [0.0, 0.0, 0.5105667, 0.0, 0.0, 28.3794333, 0.0, 0.0],
        'Generation Cost (CAD)': [12285309668.4, 0.0, 85071451.5, 4762306634.73, 12133637626.0, 7460722911.06, 0.0, 680714640.0],
        'Capacity Investment Cost (CAD)': [8220000000.0, 0, 0, 9590000000.0, 0, 0, 0, 0]
    }
    
    data_2035 = {
        'Year': [2035] * 8,
        'Source': ['Wind', 'Solar', 'Oil', 'Nuclear', 'Hydro', 'Natural Gas', 'Coal & Coke', 'Biomass & Geothermal'],
        'Generation (GWh)': [239589.48, 10583.16, 0.0, 126811.37, 402575.9, 0.0027, 0.0, 8281.2],
        'Emissions (MTCO2e)': [0.0, 0.0, 0.0, 0.0, 0.0, 1e-06, 0.0, 0.0],
        'Generation Cost (CAD)': [19366017668.4, 2174838824.54, 0.0, 11292552498.5, 12133637626.0, 262.92, 0.0, 680714640.0],
        'Capacity Investment Cost (CAD)': [8220000000.0, 0, 0, 0, 0, 0, 0, 0]
    }

# Combine all data into one DataFrame
    df_2025 = pd.DataFrame(data_2025)
    df_2030 = pd.DataFrame(data_2030)
    df_2035 = pd.DataFrame(data_2035)
    
    

    return pd.concat([df_2025, df_2030, df_2035], ignore_index=True)

# Use the updated function to create the DataFrame
df = create_dataframe_updated()
df['Cost (CAD)']=df['Generation Cost (CAD)']+df['Capacity Investment Cost (CAD)']

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
        fig1 = px.bar(filtered_df.sort_values('Generation (GWh)', ascending=False), x='Source', y='Generation (GWh)', color='Source')
        #fig1.update_layout(showlegend=False)
        st.plotly_chart(fig1)
    
    with chart2:
        st.markdown("### Emissions by Source")
        fig2 = px.bar(filtered_df.sort_values('Emissions (MTCO2e)', ascending=False), x='Source', y='Emissions (MTCO2e)', color='Source')
        st.plotly_chart(fig2)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Cost by Source")
        fig3 = px.bar(filtered_df.sort_values('Cost (CAD)', ascending=False), x='Source', y='Cost (CAD)', color='Source')
        #fig3.update_layout(showlegend=False)
        st.plotly_chart(fig3)
    with col2:
        st.markdown("### Detailed Data View")
        st.dataframe(filtered_df)



def format_decision(decision):
    color = 'green' if decision == 'Yes' else 'red'
    return f"<span style='color: {color};'>{decision}</span>"







with tab2:
    st.title("Power Plant Decisions and Impacts")

    # Year filter with 'All' option
    year_options = ['All', '2025', '2030', '2035']
    selected_year = st.selectbox("Select Year", options=year_options)

    # Cost per unit for each increase
    increase_cost = {
        'Nuclear': 9.59e9, 
        'Solar': 12.878e9, 
        'Wind': 4.11e9
    }

    # Capacity increase amounts for each power plant type (GWh)
    capacity_added = {
        'Nuclear': 48180, 
        'Solar': 139809.6, 
        'Wind': 43800
    }

    # Capacity increase decisions adjusted as per your description
    capacity_decision = {
        'Wind': [0, 2, 2],  # Two plants in 2030 and two more in 2035
        'Solar': [0, 0, 0],  # No plants
        'Nuclear': [0, 1, 0]  # One plant in 2030
    }

    # Emission deviations
    emission_deviations = [0.0, 0.0, 1.0001e-06]

    # Logic for individual years
    if selected_year != 'All':
        idx = year_options.index(selected_year) - 1
        col1, col2 = st.columns(2)
    
        total_yearly_expenditure = 0  # Initialize total expenditure for the year
    
        for source in ['Wind', 'Solar', 'Nuclear']:
            num_decisions = capacity_decision[source][idx]
            if num_decisions > 0:  # Only display non-zero metrics
                total_capacity = capacity_added[source] * num_decisions
                total_cost = increase_cost[source] * num_decisions
                total_yearly_expenditure += total_cost  # Accumulate total expenditure
    
                with col1:
                    st.metric(label=f"Additional {source} Power Plants in {selected_year} ", value=f"{num_decisions}")
                    st.metric(label=f"Total Capacity Added for {source} (GWh)", value=f"{total_capacity}")
    
                with col2:
                    st.metric(label=f"Total Cost {source} (CAD)", value=f"${total_cost:,.2f}")
        with col2: 
            st.metric(label=f"Total Expenditure for {selected_year} (CAD)", value=f"${total_yearly_expenditure:,.2f}")



        emission_deviation = emission_deviations[idx]
        st.metric(label=f"{selected_year} Emission Deviation", value=f"{emission_deviation} MTCO2e")

    # Logic for 'All' option
    else:
        total_expenditure = 0
        total_deviation = sum(emission_deviations)
        total_capacity = 0
        plants_built = {'Wind': 0, 'Solar': 0, 'Nuclear': 0}

        for year_idx, year in enumerate(year_options[1:]):  # Skip 'All'
            for source in ['Wind', 'Solar', 'Nuclear']:
                num_decisions = capacity_decision[source][year_idx]
                if num_decisions > 0:  # Consider only non-zero decisions
                    total_expenditure += increase_cost[source] * num_decisions
                    total_capacity += capacity_added[source] * num_decisions
                    plants_built[source] += num_decisions

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(label="Total Expenditure (CAD)", value=f"${total_expenditure:,.2f}")
            st.metric(label="Total Capacity Added (GWh)", value=f"{total_capacity}")

        with col2:
            for source, count in plants_built.items():
                if count > 0:  # Display only if plants were actually built
                    st.metric(label=f"Total {source} Plants Built", value=f"{count}")

        with col3:
            st.metric(label="Total Emission Deviation", value=f"{total_deviation} MTCO2e")
            
@st.cache
def convert_df_to_csv(df):
    return df.to_csv().encode('utf-8')

csv = convert_df_to_csv(filtered_df)  # Assuming 'filtered_df' is your DataFrame
col1,col2=st.columns(2)
with col1:
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='dashboard_data.csv',
        mime='text/csv',
    )
with col2:
    st.markdown(
        """
        For more details, check out our [Emissions Optimization Model on GitHub](
        https://github.com/Abdul-AA/Canada-Net-Zero-Optimization/blob/ab3119a7f5e75549d755cf47834c20b60925d91d/Emissions%20Optimization%20Model.ipynb).
        """
    )

# Run the Streamlit app (uncomment this line if running the script directly)
# st.run()
