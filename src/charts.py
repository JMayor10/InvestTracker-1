import matplotlib.pyplot as plt
import pandas as pd

def plot_performance(portfolio_value: pd.Series, save_path: str = "performance.png"):
    """Plots the portfolio value over time."""
    plt.style.use('ggplot')
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.plot(portfolio_value.index, portfolio_value.values, color='tab:blue', linewidth=2)
    ax.set_title("Portfolio Performance (1Y)", fontsize=14, fontweight='bold')
    ax.set_ylabel("Total Value (USD)")
    ax.set_xlabel("Date")
    
    # Format Y-axis with dollar signs
    ax.yaxis.set_major_formatter('${x:,.0f}')
    
    plt.tight_layout()
    plt.savefig(save_path)
    print(f"Chart saved to {save_path}")
    plt.close()
