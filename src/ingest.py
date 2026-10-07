import pandas as pd
import os

def load_holdings_csv(filepath: str) -> dict:
    """Loads a CSV of Ticker/Shares into a dictionary."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Could not find data file at {filepath}")
    
    df = pd.read_csv(filepath)
    # Convert to a dictionary of {Ticker: Shares}
    return dict(zip(df['Ticker'], df['Shares']))
