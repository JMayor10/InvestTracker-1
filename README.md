# 📈 Investment Portfolio Tracker

Track, visualize, and compare the performance of **stocks, bonds, and mutual funds** with Python, Pandas, and Matplotlib. Feed it a simple CSV of holdings and it produces charts, risk metrics, benchmark comparisons, and plain-English insights.

![tests](https://github.com/<your-username>/portfolio-tracker/actions/workflows/tests.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)

<!-- After your first run, copy the PNGs from output/ into docs/images/ -->
<p align="center">
  <img src="docs/images/performance.png" width="48%" alt="Portfolio vs benchmark">
  <img src="docs/images/allocation_vs_risk.png" width="48%" alt="Allocation vs risk by asset class">
</p>

## What it does

- **Asset-class tracking:** stocks, funds (mutual funds/ETFs), and bonds (use bond ETFs like `BND` or `AGG`, or any mutual fund ticker Yahoo Finance supports)
- **Benchmark comparison:** portfolio vs. a benchmark (default `SPY`), rebased to 100
- **Trailing returns:** 1M / 6M / 1Y / 5Y for the portfolio, the benchmark, and each asset class
- **Risk metrics:** annualized volatility, max drawdown (with date), Sharpe ratio, CAGR
- **Allocation vs. risk:** how much of the portfolio each asset class is vs. how much of the risk it drives
- **Auto-generated insights:** plain-English findings saved to `output/summary.md`

## Quick start

```bash
git clone https://github.com/JMayor10/portfolio-tracker.git
cd portfolio-tracker

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python main.py
```

Results are written to `output/`: `performance.png`, `allocation_vs_risk.png`, `drawdown.png`, and `summary.md`.

### Options

```bash
python main.py --input data/my_portfolio.csv --period 2y --benchmark QQQ --risk-free 0.04
```

| Flag | Default | Description |
|------|---------|-------------|
| `--input` | `data/sample_portfolio.csv` | Holdings CSV |
| `--period` | `5y` | History to analyze: `1y`, `2y`, `5y`, `10y`, `max` |
| `--benchmark` | `SPY` | Benchmark ticker |
| `--risk-free` | `0.0` | Annual risk-free rate used for Sharpe (e.g. `0.04`) |
| `--output-dir` | `output` | Where results are saved |

## Input format

```csv
ticker,asset_class,shares
AAPL,stock,40
FXAIX,fund,50
BND,bond,120
```

`asset_class` must be `stock`, `fund`, or `bond`. Repeated tickers are combined. See [`data/sample_portfolio.csv`](data/sample_portfolio.csv).

## ⚠️ Important: this is a "what-if" analysis

The tool assumes **today's share counts were held for the entire period**. It answers "how would this exact portfolio have performed?", not "what did I actually earn?". Real performance needs purchase dates and transactions (see the roadmap).

## How metrics are calculated

| Metric | Method |
|--------|--------|
| Total return | `end value / start value − 1` |
| CAGR | `(1 + total return)^(1 / years) − 1` |
| Annualized volatility | `std(daily returns) × √252` |
| Sharpe ratio | `(mean daily return × 252 − risk-free) / annualized volatility` |
| Max drawdown | Largest peak-to-trough decline of portfolio value |
| Share of risk | Each asset class's covariance with portfolio return ÷ portfolio variance (shares sum to 100%) |

Prices are split- and dividend-adjusted closes from Yahoo Finance via `yfinance`. If one holding has a shorter history, the whole analysis is trimmed to the overlapping dates and a warning is printed.

## Project structure

```
portfolio-tracker/
├── main.py                  # CLI entry point
├── src/
│   ├── ingest.py            # CSV loading + validation
│   ├── prices.py            # yfinance price fetching
│   ├── metrics.py           # returns, volatility, drawdown, Sharpe, risk shares
│   ├── charts.py            # Matplotlib charts
│   └── report.py            # insights + Markdown report
├── data/sample_portfolio.csv
├── tests/                   # pytest (no network needed)
└── .github/workflows/tests.yml
```

## Tests

```bash
pytest
```

Tests cover the metric math, CSV validation, and a full end-to-end run on synthetic prices, so they work offline and in CI.

## Roadmap

- [ ] Ghostfolio integration: pull holdings and transactions from a self-hosted instance (it's a companion tool, not a plugin that runs inside Ghostfolio)
- [ ] Real performance using purchase dates and prices (money-weighted return / XIRR)
- [ ] Dividend and contribution tracking
- [ ] Correlation heatmap and Monte Carlo projection
- [ ] PDF export of the report

## Disclaimer

For educational purposes only. Not financial advice. Past performance does not guarantee future results, and third-party market data may be delayed or inaccurate.

## License

MIT. Add a `LICENSE` file before publishing.
