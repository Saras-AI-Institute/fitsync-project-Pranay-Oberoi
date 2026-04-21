import streamlit as st
from modules.processor import process_data
import pandas as pd
import plotly.express as px

# Set the page configuration
st.set_page_config(layout="wide", page_title="FitSync")

# Title of the dashboard
st.title("FitSync - Personal Health Analytics")

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

# Compute metrics from the filtered data
average_steps = filtered_df['Steps'].mean()
average_sleep_hours = filtered_df['Sleep_Hours'].mean()
average_recovery_score = filtered_df['Recovery_Score'].mean()

# Create a 3-column layout for metrics
t_col1, t_col2, t_col3 = st.columns(3)

# Display metrics in respective columns
t_col1.metric(label="Average Steps", value=f"{average_steps:.0f}", delta=None)
t_col2.metric(label="Average Sleep Hours", value=f"{average_sleep_hours:.1f}", delta=None)
t_col3.metric(label="Average Recovery Score", value=f"{average_recovery_score:.1f}", delta=None)

# Create two columns for the first set of charts
left_col, right_col = st.columns(2)

# Left column: Dual line chart for recovery score and sleep trend
dual_line_chart = px.line(
    filtered_df, x='date', 
    y=['Recovery_Score', 'Sleep_Hours'],
    title='Recovery Score and Sleep Trend'
)
left_col.plotly_chart(dual_line_chart, use_container_width=True)

# Right column: Scatter plot of recovery score vs steps
scatter_plot = px.scatter(
    filtered_df, x='Steps', y='Recovery_Score', 
    color='Sleep_Hours',
    title='Recovery Score for Daily Steps'
)
right_col.plotly_chart(scatter_plot, use_container_width=True)

# Create two columns for the second set of charts
lower_left_col, lower_right_col = st.columns(2)

# Lower left column: Scatter plot of recovery score vs heart rate
recovery_vs_heart_rate = px.scatter(
    filtered_df, x='Heart_Rate_bpm', y='Recovery_Score',
    title='Recovery Score vs Resting Heart Rate'
)
lower_left_col.plotly_chart(recovery_vs_heart_rate, use_container_width=True)

# Lower right column: Line chart for calories burned trend
daily_calories_burned_trend = px.line(
    filtered_df, x='date', y='Calories_Burned',
    title='Daily Calories Burned Trend'
)
lower_right_col.plotly_chart(daily_calories_burned_trend, use_container_width=True)

# Existing text and placeholders
# ...
