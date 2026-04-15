import pandas as pd


def load_data():
    """
    Load and clean the health data from CSV file.

    Steps:
    1. Read the CSV file from the data folder.
    2. Handle missing values intelligently:
       - Fill missing 'Steps' with the median value of the column.
       - Fill missing 'Sleep_Hours' with 7.0 as a reasonable default.
       - Fill missing 'Heart_Rate_bpm' with 68, which is a typical resting heart rate.
       - Fill other columns with their respective median values.
    3. Convert the 'date' column to datetime objects for better date manipulation.
    4. Return the cleaned pandas DataFrame.
    """
    
    # Load the CSV file
    data_path = 'data/health_data.csv'
    df = pd.read_csv(data_path)
    
    # Handle missing values
    df['Steps'].fillna(df['Steps'].median(), inplace=True)
    df['Sleep_Hours'].fillna(7.0, inplace=True)
    df['Heart_Rate_bpm'].fillna(68, inplace=True)
    
    # Fill other numerical columns with their median
    for column in df.columns:
        if df[column].dtype in ['float64', 'int64']:
            df[column].fillna(df[column].median(), inplace=True)
    
    # Convert the 'date' column to datetime objects
    df['date'] = pd.to_datetime(df['date'])
    
    return df

def calculate_recovery_score(df):
    """
    Calculate a Recovery Score for each row in the DataFrame.

    The score ranges from 0 to 100 and indicates how well the person's body has recovered.

    Logic:
    - Good sleep (7+ hours) increases the score significantly.
    - Poor sleep (less than 6 hours) decreases the score heavily.
    - A lower resting heart rate is better for recovery and increases the score.
    - High step count is generally good but may decrease the score slightly due to potential strain.
    """
    def clip(value, lower, upper):
        """Ensures the value stays within the specified bounds (lower, upper)."""
        return max(lower, min(value, upper))

    recovery_scores = []
    for index, row in df.iterrows():
        sleep_score = 0
        heart_rate_score = 0
        steps_score = 0

        # Determine sleep score
        if row['Sleep_Hours'] >= 7:
            sleep_score = 40  # Good sleep adds to recovery
        elif row['Sleep_Hours'] >= 6:
            sleep_score = 20  # Average sleep
        else:
            sleep_score = 0   # Poor sleep deducts from recovery

        # Determine heart rate score (lower is better)
        heart_rate_score = clip((95 - row['Heart_Rate_bpm']) / 45 * 30, 0, 30)

        # Determine steps score
        if row['Steps'] < 12000:
            steps_score = 30  # Moderate activity adds to recovery
        elif row['Steps'] < 16000:
            steps_score = 20  # High activity can cause slight strain
        else:
            steps_score = 10  # Very high activity causes more strain

        # Aggregate overall recovery score
        total_score = sleep_score + heart_rate_score + steps_score

        # Ensure the score is within 0 to 100
        recovery_scores.append(clip(total_score, 0, 100))

    # Add the new 'Recovery_Score' column to the dataframe
    df['Recovery_Score'] = recovery_scores
    return df

def process_data():
    """
    Main processing function for the Streamlit dashboard.

    This function loads and cleans the data, calculates the Recovery Score,
    and returns the final processed DataFrame.

    Returns:
        pd.DataFrame: Processed data with Recovery Score.
    """
    # Load the cleaned data
    df = load_data()

    # Calculate the Recovery Score
    df = calculate_recovery_score(df)

    return df

