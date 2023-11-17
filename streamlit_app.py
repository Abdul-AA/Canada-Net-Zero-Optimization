import streamlit as st
import plotly.express as px
import pandas as pd

# Sample data: Replace with your actual data
data = {
    'Year': [2025, 2030, 2035],
    'Source': ['Wind', 'Solar', 'Oil', 'Nuclear', 'Hydro', 'Natural Gas', 'Coal & Coke', 'Biomass & Geothermal'],
    'Generation (GWh)': [64389.48, 12184.23, 1379.91, 78631.37, 402575.9, 100603.82, 0.0, 8281.2],
    'Emissions (MTCO2e)': [0.0, 0.0, 0.5105667, 0.0, 0.0, 37.223413472479834, 0.0, 0.0],
    'Generation Cost (USD)': [3798979320.0, 1827634470.6162817, 62095950.0, 5111039050.0, 8856669800.0, 7142871233.908293, 0.0, 496872000.00000006]
}

# Convert the data into a DataFrame
df = pd.DataFrame(data)

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

# Run the main function
if __name__ == "__main__":
    main()
