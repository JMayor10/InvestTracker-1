"""Load and validate portfolio holdings.

Today this reads a CSV. A Ghostfolio client can later return the same
DataFrame shape (ticker, asset_class, shares), so nothing downstream changes.
"""
from pathlib import Path

import pandas as pd

VALID_ASSET_CLASSES = {"stock", "bond", "fund"}
REQUIRED_COLUMNS = ["ticker", "asset_class", "shares"]


def load_holdings_csv(filepath) -> pd.DataFrame:
    """Return a DataFrame with columns: ticker, asset_class, shares."""
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Could not find data file at {path}")

    df = pd.read_csv(path)
    df.columns = [c.strip().lower() for c in df.columns]

    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(
            f"CSV is missing required column(s): {', '.join(missing)}. "
            f"Expected: {', '.join(REQUIRED_COLUMNS)}"
        )

    df = df[REQUIRED_COLUMNS].dropna().copy()
    df["ticker"] = df["ticker"].astype(str).str.strip().str.upper()
    df["asset_class"] = df["asset_class"].astype(str).str.strip().str.lower()
    df["shares"] = pd.to_numeric(df["shares"], errors="raise")

    bad_classes = sorted(set(df["asset_class"]) - VALID_ASSET_CLASSES)
    if bad_classes:
        raise ValueError(
            f"Unknown asset_class value(s): {', '.join(bad_classes)}. "
            f"Use one of: {', '.join(sorted(VALID_ASSET_CLASSES))}"
        )
    if (df["shares"] <= 0).any():
        raise ValueError("All share counts must be greater than zero.")

    # Combine repeated rows for the same ticker (e.g. several lots).
    df = df.groupby(["ticker", "asset_class"], as_index=False)["shares"].sum()
    if df["ticker"].duplicated().any():
        dupes = df.loc[df["ticker"].duplicated(), "ticker"].tolist()
        raise ValueError(f"Ticker(s) listed under multiple asset classes: {dupes}")

    if df.empty:
        raise ValueError("The holdings file contains no usable rows.")
    return df.reset_index(drop=True)
