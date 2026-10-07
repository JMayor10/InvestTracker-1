"""Entry point: CSV -> prices -> metrics -> charts + report."""
import argparse
from pathlib import Path

from src import charts, metrics, report
from src.ingest import load_holdings_csv
from src.prices import fetch_prices


def parse_args(argv=None):
    p = argparse.ArgumentParser(description="Investment portfolio tracker")
    p.add_argument("--input", default="data/sample_portfolio.csv", help="Holdings CSV")
    p.add_argument("--period", default="5y",
                   choices=["1y", "2y", "5y", "10y", "max"], help="History to analyze")
    p.add_argument("--benchmark", default="SPY", help="Benchmark ticker")
    p.add_argument("--risk-free", type=float, default=0.0,
                   help="Annual risk-free rate for Sharpe, e.g. 0.04")
    p.add_argument("--output-dir", default="output", help="Where to save results")
    return p.parse_args(argv)


def run(argv=None) -> int:
    args = parse_args(argv)
    out = Path(args.output_dir)
    benchmark = args.benchmark.upper()

    holdings = load_holdings_csv(args.input)
    tickers = holdings["ticker"].tolist()

    all_prices = fetch_prices(tickers + [benchmark], period=args.period)
    prices, bench_prices = all_prices[tickers], all_prices[benchmark]

    holding_values = metrics.calculate_holding_values(prices, holdings)
    portfolio = metrics.calculate_portfolio_value(holding_values)
    class_values = metrics.calculate_class_values(holding_values, holdings)

    summary = metrics.performance_summary(portfolio, args.risk_free)
    bench_summary = metrics.performance_summary(bench_prices, args.risk_free)
    table = metrics.returns_table(portfolio, bench_prices, benchmark, class_values)
    allocation = metrics.allocation_by_class(class_values)
    risk = metrics.risk_contribution_by_class(class_values)
    insights = report.build_insights(summary, bench_summary, benchmark,
                                     table, allocation, risk)

    print("\n--- Portfolio Summary (what-if: current holdings over the period) ---")
    print(f"Start value:       ${summary['start_value']:,.2f}")
    print(f"End value:         ${summary['end_value']:,.2f}")
    print(f"Total return:      {summary['total_return'] * 100:.2f}%")
    print(f"CAGR:              {summary['cagr'] * 100:.2f}%")
    print(f"Annual volatility: {summary['volatility'] * 100:.2f}%")
    print(f"Sharpe ratio:      {summary['sharpe']:.2f}")
    print(f"Max drawdown:      {summary['max_drawdown'] * 100:.2f}%")
    print("\nInsights:")
    for line in insights:
        print(f"  - {line}")
    print()

    charts.plot_performance(portfolio, bench_prices, benchmark, args.period,
                            out / "performance.png")
    charts.plot_allocation_vs_risk(allocation, risk, out / "allocation_vs_risk.png")
    charts.plot_drawdown(metrics.calculate_drawdown(portfolio), out / "drawdown.png")
    report.write_report(out / "summary.md", summary, bench_summary, benchmark,
                        table, allocation, risk, insights, args.period)
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
