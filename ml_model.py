import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

#temporary code because I don't have the dataset just yet
def load_dataset(file_path):
    """Loads the emissions dataset into a pandas DataFrame."""
    try:
        df = pd.read_csv(file_path)
        print("Dataset loaded successfully!")
        return df
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return None
