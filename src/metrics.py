import pandas as pd
import numpy as np

def calculate_portfolio_value(prices_df: pd.DataFrame, holdings: dict) -> pd.Series:
    """Calculates total portfolio value over time based on static holdings."""
    portfolio_value = pd.Series(0.0, index=prices_df.index)
    for ticker, shares in holdings.items():
        if ticker in prices_df.columns:
            portfolio_value += prices_df[ticker] * shares
    return portfolio_value

def calculate_drawdown(portfolio_value: pd.Series) -> pd.Series:
    """Calculates the percentage drawdown from the peak."""
    rolling_max = portfolio_value.cummax()
    drawdown = (portfolio_value - rolling_max) / rolling_max
    return drawdown

def get_performance_summary(portfolio_value: pd.Series) -> dict:
    """Returns key performance metrics."""
    start_value = portfolio_value.iloc[0]
    end_value = portfolio_value.iloc[-1]
    
    total_return = (end_value - start_value) / start_value
    daily_returns = portfolio_value.pct_change().dropna()
    
    # Annualized volatility (assuming 252 trading days)
    volatility = daily_returns.std() * np.sqrt(252)
    max_drawdown = calculate_drawdown(portfolio_value).min()
    
    return {
        "Start Value": start_value,
        "End Value": end_value,
        "Total Return": total_return,
        "Annual Volatility": volatility,
        "Max Drawdown": max_drawdown
    }
