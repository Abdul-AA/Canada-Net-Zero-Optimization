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

# Function to plot the data
def plot_data(filtered_df):
    # Plotting Generation (GWh)
    fig = px.bar(filtered_df, x='Source', y='Generation (GWh)', color='Source', title='Generation by Source')
    st.plotly_chart(fig)

    # Plotting Emissions (MTCO2e)
    fig = px.bar(filtered_df, x='Source', y='Emissions (MTCO2e)', color='Source', title='Emissions by Source')
    st.plotly_chart(fig)

    # Plotting Generation Cost (USD)
    fig = px.bar(filtered_df, x='Source', y='Generation Cost (USD)', color='Source', title='Generation Cost by Source')
    st.plotly_chart(fig)

# Main function to run the Streamlit app
def main():
    st.title("Canada's Electricity Sector Transition to Net Zero: Model Results")

    year_filter = st.selectbox('Select Year', df['Year'].unique())
    filtered_df = df[df['Year'] == year_filter]

    st.header(f"Model Results for {year_filter}")
    plot_data(filtered_df)

if __name__ == "__main__":
    main()
