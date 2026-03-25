import numpy as np
import pandas as pd
from datetime import timedelta, date

# Function to generate a year's worth of fitness data
def generate_fitness_data(start_date: str, num_days: int = 365):
    # Define date range
    dates = pd.date_range(start=start_date, periods=num_days)
    
    # Generate data using normal distributions
    steps = np.random.normal(loc=8500, scale=2000, size=num_days).clip(3000, 18000)
    sleep_hours = np.random.normal(loc=7, scale=1, size=num_days).clip(4.5, 9.5)
    heart_rate_bpm = np.random.normal(loc=68, scale=10, size=num_days).clip(48, 110)
    calories_burned = np.random.uniform(low=1800, high=4200, size=num_days)
    active_minutes = np.random.uniform(low=20, high=180, size=num_days)

    # Create DataFrame
    data = pd.DataFrame({
        'Date': dates,
        'Steps': steps,
        'Sleep_Hours': sleep_hours,
        'Heart_Rate_bpm': heart_rate_bpm,
        'Calories_Burned': calories_burned,
        'Active_Minutes': active_minutes
    })

    # Introduce 5% missing values (NaN) into each column
    nan_indices = np.random.choice(data.index, size=int(0.05 * num_days), replace=False)
    for column in data.columns:
        data.loc[nan_indices, column] = np.nan

    return data

# Generate data starting from 2025-01-01
fitness_data = generate_fitness_data('2025-01-01')

# Save to a CSV file
fitness_data.to_csv('data/fitness_data.csv', index=False)

# If you need to print the data, uncomment the following line:
# print(fitness_data.head())
