import yfinance as yf
import pandas as pd

def fetch_historical_prices(tickers: list, period: str = "1y") -> pd.DataFrame:
    """Fetches historical closing prices for a list of tickers."""
    print(f"Fetching {period} of historical data for: {', '.join(tickers)}...")
    data = yf.download(tickers, period=period)["Close"]
    
    # Handle single ticker edge case where yfinance returns a Series instead of DataFrame
    if isinstance(data, pd.Series):
        data = data.to_frame(name=tickers[0])
        
    return data.dropna()
