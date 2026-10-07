"""Plain-English insights and a Markdown summary report."""
from pathlib import Path

import numpy as np

CLASS_LABELS = {"stock": "Stocks", "bond": "Bonds", "fund": "Funds"}


def _pct(x, digits=1):
    return "n/a" if x is None or np.isnan(x) else f"{x * 100:.{digits}f}%"


def build_insights(summary, bench_summary, benchmark_name, table, allocation, risk):
    """Return a list of human-readable findings."""
    insights = []

    diff = summary["total_return"] - bench_summary["total_return"]
    verdict = "outperformed" if diff >= 0 else "underperformed"
    insights.append(
        f"The portfolio returned {_pct(summary['total_return'])} over the period and "
        f"{verdict} {benchmark_name} ({_pct(bench_summary['total_return'])}) "
        f"by {abs(diff) * 100:.1f} percentage points."
    )

    risk = risk.dropna()
    if not risk.empty:
        top = risk.idxmax()
        name = CLASS_LABELS.get(top, top)
        alloc, share = allocation[top], risk[top]
        if share > alloc + 0.05:
            insights.append(
                f"{name} were {_pct(alloc, 0)} of the portfolio but drove "
                f"{_pct(share, 0)} of its volatility."
            )
        else:
            insights.append(
                f"Risk is spread roughly in line with allocation; {name.lower()} are "
                f"{_pct(alloc, 0)} of value and {_pct(share, 0)} of risk."
            )

    insights.append(
        f"Maximum drawdown was {_pct(summary['max_drawdown'])} "
        f"(trough on {summary['max_drawdown_date']:%Y-%m-%d}) versus "
        f"{_pct(bench_summary['max_drawdown'])} for {benchmark_name}."
    )

    if not np.isnan(summary["sharpe"]):
        insights.append(
            f"Sharpe ratio was {summary['sharpe']:.2f} vs {bench_summary['sharpe']:.2f} "
            f"for {benchmark_name}."
        )

    classes = [c for c in table.index if c in CLASS_LABELS]
    for label in ["5Y", "1Y", "6M", "1M"]:
        col = table.loc[classes, label].dropna()
        if len(col) >= 2:
            best, worst = col.idxmax(), col.idxmin()
            insights.append(
                f"Over {label}, {CLASS_LABELS[best].lower()} were the best performing class "
                f"({_pct(col[best])}) and {CLASS_LABELS[worst].lower()} the weakest "
                f"({_pct(col[worst])})."
            )
            break
    return insights


def _markdown_table(table, class_labels=CLASS_LABELS):
    header = "| | " + " | ".join(table.columns) + " |"
    sep = "|---|" + "---|" * len(table.columns)
    rows = []
    for name, row in table.iterrows():
        label = class_labels.get(name, name)
        rows.append(f"| {label} | " + " | ".join(_pct(v) for v in row) + " |")
    return "\n".join([header, sep, *rows])


def write_report(path, summary, bench_summary, benchmark_name, table,
                 allocation, risk, insights, period):
    lines = [
        "# Portfolio Report",
        "",
        f"*Period: {period}. Holdings are modelled as if today's share counts "
        f"were held throughout (what-if, not actual history).*",
        "",
        "## Insights",
        "",
        *[f"- {i}" for i in insights],
        "",
        "## Summary",
        "",
        "| Metric | Portfolio | " + benchmark_name + " |",
        "|---|---|---|",
        f"| Total return | {_pct(summary['total_return'])} | {_pct(bench_summary['total_return'])} |",
        f"| CAGR | {_pct(summary['cagr'])} | {_pct(bench_summary['cagr'])} |",
        f"| Annual volatility | {_pct(summary['volatility'])} | {_pct(bench_summary['volatility'])} |",
        f"| Sharpe ratio | {summary['sharpe']:.2f} | {bench_summary['sharpe']:.2f} |",
        f"| Max drawdown | {_pct(summary['max_drawdown'])} | {_pct(bench_summary['max_drawdown'])} |",
        "",
        "## Trailing returns",
        "",
        _markdown_table(table),
        "",
        "## Allocation vs risk",
        "",
        "| Asset class | Share of value | Share of risk |",
        "|---|---|---|",
        *[
            f"| {CLASS_LABELS.get(c, c)} | {_pct(allocation[c], 0)} | {_pct(risk.get(c, np.nan), 0)} |"
            for c in allocation.index
        ],
        "",
        "*Not financial advice. Past performance does not guarantee future results.*",
        "",
    ]
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"Report saved to {out}")
    return out
