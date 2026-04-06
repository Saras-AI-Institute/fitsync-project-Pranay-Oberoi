import pandas as pd

# Load the CSV file
data_path = 'data/fitness_data.csv'
health_data = pd.read_csv(data_path)

# Print first 5 rows
print('First 5 rows of the dataset:')
print(health_data.head())

# Print number of missing values in each column
print('\nNumber of missing values in each column:')
print(health_data.isnull().sum())