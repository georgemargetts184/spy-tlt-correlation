"""Rolling 60-day correlation of SPY and TLT daily returns over the last year."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf

WINDOW = 60

# Pull an extra ~3 months so the rolling window is full for the whole last year.
closes = yf.download(["SPY", "TLT"], period="15mo", interval="1d",
                     auto_adjust=True, progress=False)["Close"].dropna()
returns = closes.pct_change().dropna()
corr = returns["SPY"].rolling(WINDOW).corr(returns["TLT"]).dropna()
corr = corr[corr.index >= corr.index[-1] - pd.DateOffset(years=1)]

INK, MUTED, GRID, SURFACE, LINE = "#0b0b0b", "#52514e", "#e6e5e1", "#fcfcfb", "#2a78d6"
fig, ax = plt.subplots(figsize=(10, 5), facecolor=SURFACE)
ax.set_facecolor(SURFACE)
ax.plot(corr.index, corr.values, color=LINE, linewidth=2)
ax.axhline(0, color=MUTED, linewidth=1)
ax.set_ylim(-1, 1)
ax.grid(axis="y", color=GRID, linewidth=0.8)
for side in ("top", "right", "left"):
    ax.spines[side].set_visible(False)
ax.spines["bottom"].set_color(GRID)
ax.tick_params(colors=MUTED, length=0)
ax.set_ylabel("Correlation", color=MUTED)
ax.set_title(f"SPY vs TLT: rolling {WINDOW}-day correlation of daily returns",
             color=INK, loc="left", fontsize=13, pad=12)
last = corr.iloc[-1]
ax.annotate(f"{last:+.2f}", (corr.index[-1], last), xytext=(6, 0),
            textcoords="offset points", va="center", color=INK, fontsize=10)
fig.tight_layout()
fig.savefig("spy_tlt_corr.png", dpi=150)

print(f"Data: {closes.index[0].date()} to {closes.index[-1].date()}")
print(f"Latest: {last:+.2f}  Mean: {corr.mean():+.2f}  "
      f"Min: {corr.min():+.2f} ({corr.idxmin().date()})  Max: {corr.max():+.2f} ({corr.idxmax().date()})")
