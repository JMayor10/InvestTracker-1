from src.ingest import load_holdings_csv
from src.prices import fetch_historical_prices
from src.metrics import calculate_portfolio_value, get_performance_summary
from src.charts import plot_performance

def main():
    # 1. Ingest Data
    holdings = load_holdings_csv("data/sample_portfolio.csv")
    tickers = list(holdings.keys())
    
    # 2. Fetch Prices
    prices_df = fetch_historical_prices(tickers, period="1y")
    
    # 3. Calculate Metrics
    portfolio_value = calculate_portfolio_value(prices_df, holdings)
    summary = get_performance_summary(portfolio_value)
    
    print("\n--- Portfolio Summary ---")
    print(f"Starting Value:  ${summary['Start Value']:,.2f}")
    print(f"Ending Value:    ${summary['End Value']:,.2f}")
    print(f"Total Return:     {summary['Total Return'] * 100:.2f}%")
    print(f"Max Drawdown:     {summary['Max Drawdown'] * 100:.2f}%")
    print(f"Annual Volatility:{summary['Annual Volatility'] * 100:.2f}%")
    print("-------------------------\n")
    
    # 4. Generate Output
    plot_performance(portfolio_value, save_path="portfolio_chart.png")

if __name__ == "__main__":
    main()
