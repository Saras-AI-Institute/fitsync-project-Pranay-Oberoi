import streamlit as st
from modules.processor import process_data
import pandas as pd
import plotly.express as px

# Set the page configuration
st.set_page_config(layout="wide", page_title="FitSync - Trends & Insights")

# Title of the page
st.title("Trends & Insights")

# Sidebar for dynamic time filtering
st.sidebar.header("Filters")
time_range = st.sidebar.selectbox(
    "Select Time Range",
    options=["Last 7 Days", "Last 30 Days", "All Time"],
    index=2
)

# Load and process data
df = process_data()

df['date'] = pd.to_datetime(df['date'])  # Ensure 'date' column is datetime

# Filter the dataframe based on the selected time range
if time_range == "Last 7 Days":
    filtered_df = df[df['date'] >= (pd.Timestamp.today() - pd.Timedelta(days=7))]
elif time_range == "Last 30 Days":
    filtered_df = df[df['date'] >= (pd.Timestamp.today() - pd.Timedelta(days=30))]
else:
    filtered_df = df

# Calculate summary statistics
summary_stats = filtered_df.agg({
    'Recovery_Score': ['mean', 'min', 'max'],
    'Sleep_Hours': ['mean', 'min', 'max'],
    'Steps': ['mean', 'min', 'max'],
    'Calories_Burned': ['mean', 'min', 'max']
})

# Display summary statistics
st.subheader("Summary Statistics")
st.write("Below are the summary statistics of your selected time range:")
st.dataframe(summary_stats.transpose())

# Line chart for average Recovery Score month-wise
filtered_df['month'] = filtered_df['date'].dt.to_period('M')
monthly_avg_recovery = filtered_df.groupby('month')['Recovery_Score'].mean().reset_index()
line_chart = px.line(monthly_avg_recovery, x='month', y='Recovery_Score',
                     title='Average Recovery Score by Month')
st.plotly_chart(line_chart, use_container_width=True)

# Histogram for the distribution of metrics
st.subheader("Distribution of Metrics")
metrics = ['Steps', 'Calories_Burned', 'Recovery_Score', 'Sleep_Hours']
for metric in metrics:
    histogram = px.histogram(filtered_df, x=metric, nbins=30, title=f'Distribution of {metric}')
    st.plotly_chart(histogram, use_container_width=True)