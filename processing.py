import pandas as pd
from scipy.stats import zscore

def map_mood_to_num(df: pd.DataFrame, mood_dict: dict) -> pd.DataFrame:
    """
    Maps moods to numerical values in the dataframe.
    
    Parameters:
    - df (pd.DataFrame): The dataframe containing the raw data
    - mood_dict (dict): A dictionary mapping moods to numerical values
    
    Returns:
    - pd.DataFrame: The modified dataframe with a new column for mood_num
    """
    df["mood_num"] = df["mood"].map(mood_dict)
    return df

def calculate_zscore(df: pd.DataFrame,column: str) -> pd.DataFrame:
    """
    Calculates the zscore for the mood_num column in the dataframe.
    
    Parameters:
    - df (pd.DataFrame): The dataframe containing the mood_num column
    - column: the column name on which to calculate the zscore
    Returns:
    - pd.DataFrame: The modified dataframe with a new column for zscore
    """
    df["zscore"] = zscore(df[column])
    return df

def calculate_rolling_average(df: pd.DataFrame, window: int) -> pd.DataFrame:
    """
    Calculates the rolling average for the zscore column in the dataframe.
    
    Parameters:
    - df (pd.DataFrame): The dataframe containing the zscore column
    - window (int): The window size for the rolling average
    
    Returns:
    - pd.DataFrame: The modified dataframe with a new column for zscore_smooth
    """
    df["zscore_smooth"] = df["zscore"].rolling(window, min_periods=int(window*0.55)).mean()
    return df

def set_datetimeindex(df: pd.DataFrame,date_col: str) -> pd.DataFrame:
        # set the date column as index
       
    df.index = pd.to_datetime(df[date_col], format='%Y-%m-%d')
    
    return df

def get_daily_mean_data(df):
    """
    Resamples the given DataFrame to calculate the daily mean and fills any missing values using forward filling.
    
    Args:
        df (pd.DataFrame): The DataFrame to be resampled.
        
    Returns:
        pd.DataFrame: The resampled DataFrame with daily mean values.
    """
    df_daily_mean = df.resample('D').mean().ffill()
    return df_daily_mean


   
def process_data(shows: pd.DataFrame, mood_dict: dict, window: int) -> pd.DataFrame:
    """
    Processes the data and adds additional columns to the dataframe.
    
    Parameters:
    - shows (pd.DataFrame): The dataframe containing the raw data
    - mood_dict (dict): A dictionary mapping moods to numerical values
    - window (int): The window size for the rolling average
    
    Returns:
    - pd.DataFrame: The processed dataframe containing additional columns for mood_num, zscore, and zscore_smooth
    """
    # make a copy of the input dataframe
    processed_data = shows.copy()
    
    processed_data = set_datetimeindex(processed_data,date_col="full_date")
    # map moods to numerical values
    processed_data = map_mood_to_num(processed_data, mood_dict)
    
    # calculate zscore
    processed_data = calculate_zscore(processed_data,column='mood_num')
    
    # calculate rolling average
    processed_data = calculate_rolling_average(processed_data, window)
    return processed_data
