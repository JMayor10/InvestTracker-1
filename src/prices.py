"""Market data fetching (Yahoo Finance via yfinance)."""
import pandas as pd
import yfinance as yf


def fetch_prices(tickers: list, period: str = "5y") -> pd.DataFrame:
    """Return adjusted daily closing prices, one column per ticker.

    Raises a clear error if any ticker has no data, and warns when the
    shortest price history limits the date range of the whole portfolio.
    """
    tickers = list(dict.fromkeys(tickers))  # de-duplicate, keep order
    print(f"Fetching {period} of price data for: {', '.join(tickers)} ...")

    raw = yf.download(tickers, period=period, auto_adjust=True, progress=False)
    if raw is None or raw.empty:
        raise ValueError("No price data returned. Check your connection and tickers.")

    close = raw["Close"]
    if isinstance(close, pd.Series):  # single-ticker edge case
        close = close.to_frame(name=tickers[0])

    missing = [t for t in tickers if t not in close.columns or close[t].isna().all()]
    if missing:
        raise ValueError(f"No price data found for: {', '.join(missing)}")

    close = close[tickers]
    first_valid = close.apply(pd.Series.first_valid_index)
    limiting_ticker = first_valid.idxmax()

    aligned = close.dropna()
    if aligned.empty:
        raise ValueError("The tickers share no overlapping trading days.")

    if aligned.index[0] > first_valid.min() + pd.Timedelta(days=7):
        print(
            f"Warning: history starts {aligned.index[0].date()} because "
            f"{limiting_ticker} has the shortest price history."
        )
    return aligned
