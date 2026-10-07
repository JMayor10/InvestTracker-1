"""Performance and risk calculations.

Important: the portfolio is modelled as a *what-if* - today's share counts
are assumed to have been held for the entire period. It is not your actual
historical performance (that needs transaction dates; see the roadmap).
"""
import numpy as np
import pandas as pd

TRADING_DAYS = 252

PERIOD_OFFSETS = {
    "1M": pd.DateOffset(months=1),
    "6M": pd.DateOffset(months=6),
    "1Y": pd.DateOffset(years=1),
    "5Y": pd.DateOffset(years=5),
}


def calculate_holding_values(prices: pd.DataFrame, holdings: pd.DataFrame) -> pd.DataFrame:
    """Dollar value of each holding over time (price x shares)."""
    shares = holdings.set_index("ticker")["shares"]
    return prices[shares.index] * shares


def calculate_portfolio_value(holding_values: pd.DataFrame) -> pd.Series:
    return holding_values.sum(axis=1)


def calculate_class_values(holding_values: pd.DataFrame, holdings: pd.DataFrame) -> pd.DataFrame:
    """Dollar value of each asset class over time."""
    classes = holdings.set_index("ticker")["asset_class"]
    return holding_values.T.groupby(classes).sum().T


def calculate_drawdown(value: pd.Series) -> pd.Series:
    """Percentage decline from the running peak (0 at peaks, negative below)."""
    return value / value.cummax() - 1


def period_return(value: pd.Series, offset: pd.DateOffset) -> float:
    """Return over the trailing window, or NaN if history is too short."""
    end_date = value.index[-1]
    start_date = end_date - offset
    if start_date < value.index[0] - pd.Timedelta(days=5):
        return np.nan
    start_value = value.asof(start_date)
    if pd.isna(start_value):  # start date fell just before the first row
        start_value = value.iloc[0]
    return value.iloc[-1] / start_value - 1


def returns_table(portfolio: pd.Series, benchmark: pd.Series,
                  benchmark_name: str, class_values: pd.DataFrame) -> pd.DataFrame:
    """Trailing returns (1M/6M/1Y/5Y) for portfolio, benchmark and each class."""
    rows = {"Portfolio": portfolio, benchmark_name: benchmark}
    for cls in class_values.columns:
        rows[cls] = class_values[cls]
    data = {
        name: {label: period_return(series, off) for label, off in PERIOD_OFFSETS.items()}
        for name, series in rows.items()
    }
    return pd.DataFrame(data).T[list(PERIOD_OFFSETS)]


def performance_summary(value: pd.Series, risk_free: float = 0.0) -> dict:
    """Key metrics. Sharpe uses the arithmetic annualized mean return."""
    daily = value.pct_change().dropna()
    years = (value.index[-1] - value.index[0]).days / 365.25
    total_return = value.iloc[-1] / value.iloc[0] - 1
    cagr = (1 + total_return) ** (1 / years) - 1 if years > 0 else np.nan
    volatility = daily.std() * np.sqrt(TRADING_DAYS)
    ann_return = daily.mean() * TRADING_DAYS
    sharpe = (ann_return - risk_free) / volatility if volatility > 0 else np.nan
    drawdown = calculate_drawdown(value)
    return {
        "start_value": value.iloc[0],
        "end_value": value.iloc[-1],
        "total_return": total_return,
        "cagr": cagr,
        "volatility": volatility,
        "sharpe": sharpe,
        "max_drawdown": drawdown.min(),
        "max_drawdown_date": drawdown.idxmin(),
    }


def allocation_by_class(class_values: pd.DataFrame) -> pd.Series:
    """Share of current portfolio value held in each asset class."""
    latest = class_values.iloc[-1]
    return latest / latest.sum()


def risk_contribution_by_class(class_values: pd.DataFrame) -> pd.Series:
    """Share of portfolio variance attributable to each asset class.

    Each class's daily contribution to portfolio return is its dollar change
    divided by yesterday's portfolio value. These sum exactly to the portfolio
    return, so the covariance-based shares below sum to 1.
    """
    total = class_values.sum(axis=1)
    contrib = class_values.diff().div(total.shift(1), axis=0).dropna()
    portfolio_ret = contrib.sum(axis=1)
    variance = portfolio_ret.var()
    if variance == 0 or np.isnan(variance):
        return pd.Series(np.nan, index=class_values.columns)
    return contrib.apply(lambda c: c.cov(portfolio_ret)) / variance
