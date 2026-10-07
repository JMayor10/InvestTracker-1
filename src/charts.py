"""Matplotlib visualizations. Uses the headless Agg backend (works in CI)."""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import PercentFormatter

CLASS_LABELS = {"stock": "Stocks", "bond": "Bonds", "fund": "Funds"}


def _save(fig, save_path) -> Path:
    path = Path(save_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"Chart saved to {path}")
    return path


def plot_performance(portfolio_value, benchmark_prices, benchmark_name, period, save_path):
    """Portfolio vs benchmark, both rebased to 100 at the start."""
    plt.style.use("ggplot")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(portfolio_value.index, portfolio_value / portfolio_value.iloc[0] * 100,
            linewidth=2, label="Portfolio (what-if)")
    ax.plot(benchmark_prices.index, benchmark_prices / benchmark_prices.iloc[0] * 100,
            linewidth=2, linestyle="--", label=benchmark_name)
    ax.set_title(f"Portfolio vs {benchmark_name} ({period}, rebased to 100)",
                 fontsize=14, fontweight="bold")
    ax.set_ylabel("Growth of 100")
    ax.set_xlabel("Date")
    ax.legend()
    return _save(fig, save_path)


def plot_allocation_vs_risk(allocation, risk, save_path):
    """Grouped bars: share of money vs share of risk, per asset class."""
    plt.style.use("ggplot")
    labels = [CLASS_LABELS.get(c, c) for c in allocation.index]
    x = np.arange(len(labels))
    width = 0.38
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(x - width / 2, allocation.values, width, label="Share of portfolio value")
    ax.bar(x + width / 2, risk.reindex(allocation.index).values, width,
           label="Share of portfolio risk")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.yaxis.set_major_formatter(PercentFormatter(1.0))
    ax.set_title("Where the money is vs where the risk comes from",
                 fontsize=14, fontweight="bold")
    ax.legend()
    return _save(fig, save_path)


def plot_drawdown(drawdown, save_path):
    plt.style.use("ggplot")
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.fill_between(drawdown.index, drawdown.values, 0, alpha=0.5, color="tab:red")
    ax.yaxis.set_major_formatter(PercentFormatter(1.0))
    ax.set_title("Portfolio drawdown from peak", fontsize=14, fontweight="bold")
    return _save(fig, save_path)
