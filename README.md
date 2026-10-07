# 📈 Investment Portfolio Tracker

Track, visualize, and compare the performance of **stocks, bonds, and mutual funds** using Python, Pandas, and Matplotlib. Works with a simple CSV file or as a companion analytics tool for a self-hosted [Ghostfolio](https://ghostfol.io) instance.

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Tests](https://img.shields.io/badge/tests-passing-brightgreen)

<!-- Replace these with your own screenshots (save them in /docs/images) -->
<p align="center">
  <img src="docs/images/cumulative_return.png" width="48%" alt="Cumulative return vs benchmark">
  <img src="docs/images/allocation.png" width="48%" alt="Asset allocation">
</p>

---

## ✨ Features

- **Multi-asset tracking:** stocks, ETFs, mutual funds, and bonds (via bond ETFs such as BND or AGG)
- **Performance charts:** cumulative return, rolling returns, allocation breakdown
- **Risk metrics:** annualized volatility, max drawdown, Sharpe ratio
- **Past return comparison:** portfolio vs. benchmark (e.g. S&P 500) and by asset class over 1M, 6M, 1Y, and 5Y
- **Auto-generated insights:** plain-English summaries of what drove your returns and risk
- **Flexible input:** CSV file or the Ghostfolio API

## 🧠 Sample Insights

> Replace these with real output from your sample portfolio.

- Equities were **78%** of the portfolio but drove **91%** of its volatility.
- The portfolio returned **X%** over 1Y vs. **Y%** for the S&P 500.
- Maximum drawdown was **-Z%**, reached in *[month, year]*.
- Bonds reduced overall volatility by roughly **N%** compared to an all-equity mix.

## 🚀 Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/<your-username>/portfolio-tracker.git
cd portfolio-tracker

# 2. Install dependencies
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 3. Run on the included sample data
python -m src.report --input data/sample_portfolio.csv --benchmark SPY
```

Charts and the summary report are saved to the `output/` folder.

## 📂 Input Format (CSV)

| Column | Description | Example |
|--------|-------------|---------|
| `ticker` | Ticker symbol | `AAPL` |
| `asset_class` | `stock`, `bond`, or `fund` | `stock` |
| `shares` | Number of shares/units held | `25` |
| `purchase_date` | Date bought (YYYY-MM-DD) | `2021-03-15` |
| `purchase_price` | Price per share at purchase | `121.03` |

See [`data/sample_portfolio.csv`](data/sample_portfolio.csv) for a working example.

## 👻 Ghostfolio Integration (Optional)

This tool is a **companion** to Ghostfolio, not a plugin that runs inside it. It reads your data from your Ghostfolio instance and produces extra analytics and charts.

```bash
cp .env.example .env
# Edit .env and set:
#   GHOSTFOLIO_URL=http://localhost:3333
#   GHOSTFOLIO_TOKEN=<your-security-token>

python -m src.report --source ghostfolio --benchmark SPY
```

Endpoints and authentication can change between Ghostfolio versions, so check the [Ghostfolio docs](https://github.com/ghostfolio/ghostfolio) if the connection fails.

## 🗂 Project Structure

```
portfolio-tracker/
├── src/
│   ├── ingest.py       # CSV loader + Ghostfolio API client
│   ├── prices.py       # Price data via yfinance
│   ├── metrics.py      # Returns, volatility, drawdown, Sharpe
│   ├── charts.py       # Matplotlib visualizations
│   └── report.py       # Insights summary + report generation
├── data/
│   └── sample_portfolio.csv
├── notebooks/
│   └── demo.ipynb
├── tests/
├── docs/images/
├── requirements.txt
└── README.md
```

## 📊 How Metrics Are Calculated

| Metric | Method |
|--------|--------|
| Daily return | `pct_change()` on adjusted close prices |
| Portfolio return | Weighted sum of asset returns |
| Cumulative return | `(1 + r).cumprod() - 1` |
| Annualized volatility | `std(daily returns) × √252` |
| Max drawdown | Largest peak-to-trough decline in cumulative value |
| Sharpe ratio | `(annualized return − risk-free rate) / annualized volatility` |

## 🧪 Running Tests

```bash
pytest
```

## 🛠 Tech Stack

- **Python 3.10+**
- **Pandas / NumPy:** data handling and calculations
- **Matplotlib:** charts
- **yfinance:** market price data
- **requests / python-dotenv:** Ghostfolio API access

## 🗺 Roadmap

- [ ] Dividend and contribution tracking
- [ ] Monte Carlo projection
- [ ] Correlation heatmap
- [ ] Export report to PDF
- [ ] Multi-currency support

## ⚠️ Disclaimer

This project is for educational and informational purposes only and is **not financial advice**. Past performance does not guarantee future results. Market data from third-party sources may be delayed or inaccurate.

## 🔐 Privacy

Never commit real account data or API tokens. Keep secrets in `.env` (already in `.gitignore`).

## 📄 License

Released under the [MIT License](LICENSE).

## 🙌 Acknowledgements

- [Ghostfolio](https://ghostfol.io) for the open-source wealth management platform
- [yfinance](https://github.com/ranaroussi/yfinance) for market data access
