import streamlit as st
import plotly.express as px
import pandas as pd

# Data Preparation
def create_dataframe():
    data = {
        'Year': [2025] * 8 + [2030] * 8 + [2035] * 8,
        'Source': ['Wind', 'Solar', 'Oil', 'Nuclear', 'Hydro', 'Natural Gas', 'Coal & Coke', 'Biomass & Geothermal'] * 3,
        'Generation (GWh)': [64389.48, 12184.23, 1379.91, 78631.37, 402575.9, 100603.82, 0.0, 8281.2,
                             151989.48, 0.0, 1379.91, 174991.37, 402575.9, 30810.47, 0.0, 8281.2,
                             195789.48, 8357.67, 0.0, 271351.37, 402575.9, 0.0, 0.0, 8281.2],
        'Emissions (MTCO2e)': [0.0, 0.0, 0.5105667, 0.0, 0.0, 37.223413472479834, 0.0, 0.0,
                               0.0, 0.0, 0.5105667, 0.0, 0.0, 11.399873899999957, 0.0, 0.0,
                               0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        'Generation Cost (USD)': [3798979320.0, 1827634470.6162817, 62095950.0, 5111039050.0, 8856669800.0, 7142871233.908293, 0.0, 496872000.00000006,
                                  8967379320.000002, 0.0, 62095950.0, 11374439050.0, 8856669800.0, 2187543369.999992, 0.0, 496872000.00000006,
                                  11551579320.0, 1253650499.9999976, 0.0, 17637839050.0, 8856669800.0, 0.0, 0.0, 496872000.00000006]
    }
    return pd.DataFrame(data)

df = create_dataframe()

# Function to plot data in a given container
def plot_data(container, filtered_df, y_column, title):
    fig = px.bar(filtered_df, x='Source', y=y_column, color='Source', title=title)
    container.plotly_chart(fig, use_container_width=True)

# Main function to run the Streamlit app
def main():
    st.title("Canada's Electricity Sector Transition to Net Zero: Model Results")

    # Sidebar for user inputs
    year_filter = st.sidebar.selectbox('Select Year', df['Year'].unique())
    filtered_df = df[df['Year'] == year_filter]

    # Layout using containers and columns
    col1, col2 = st.columns(2)

    with col1:
        plot_data(st, filtered_df, 'Generation (GWh)', 'Generation by Source (GWh)')

    with col2:
        plot_data(st, filtered_df, 'Emissions (MTCO2e)', 'Emissions by Source (MTCO2e)')

    col3, col4 = st.columns(2)

    with col3:
        plot_data(st, filtered_df, 'Generation Cost (USD)', 'Generation Cost by Source (USD)')

    # Add additional charts or content in columns as needed

if __name__ == "__main__":
    main()
