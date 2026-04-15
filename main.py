import streamlit as st
from modules.processor import process_data

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

# Filter the dataframe based on the selected time range
df['date'] = pd.to_datetime(df['date'])  # Ensure 'date' column is datetime

if time_range == "Last 7 Days":
    df = df[df['date'] >= (pd.Timestamp.today() - pd.Timedelta(days=7))]
elif time_range == "Last 30 Days":
    df = df[df['date'] >= (pd.Timestamp.today() - pd.Timedelta(days=30))]

# Compute metrics from the filtered data
average_steps = df['Steps'].mean()
average_sleep_hours = df['Sleep_Hours'].mean()
average_recovery_score = df['Recovery_Score'].mean()

# Create a 3-column layout for metrics
t_col1, t_col2, t_col3 = st.columns(3)

# Display metrics in respective columns
t_col1.metric(label="Average Steps", value=f"{average_steps:.0f}", delta=None)
t_col2.metric(label="Average Sleep Hours", value=f"{average_sleep_hours:.1f}", delta=None)
t_col3.metric(label="Average Recovery Score", value=f"{average_recovery_score:.1f}", delta=None)

# Display the processed data
st.dataframe(df)

# Placeholder for future interactive widgets and visualizations
st.header("Overview")

st.markdown(
    """
    Welcome to **FitSync**, your personal health analytics dashboard.
    Here you can visualize and track your health metrics including steps, sleep hours, heart rate, and recovery scores.
    Stay tuned for more interactive features and insights.
    """
)

# Future enhancements could include charts, metrics, and interactive elements

