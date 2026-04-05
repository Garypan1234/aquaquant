import yfinance as yf
import pandas as pd

stocks = ["AAPL", "NVDA", "TSLA", "VFV.TO"]

def calculate_rsi(data, window=14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

for stock in stocks:
    data = yf.download(stock, period="3mo")

    data["MA5"] = data["Close"].rolling(5).mean()
    data["MA10"] = data["Close"].rolling(10).mean()
    data["RSI"] = calculate_rsi(data)

    latest = data.iloc[-1]
    prev = data.iloc[-2]

    print(f"\n=== {stock} ===")

    if prev["MA5"] < prev["MA10"] and latest["MA5"] > latest["MA10"]:
        print("🔥 金叉 → 可以关注买入")
    elif prev["MA5"] > prev["MA10"] and latest["MA5"] < latest["MA10"]:
        print("⚠️ 死叉 → 注意风险")

    if latest["RSI"] < 30:
        print("📉 RSI < 30 → 超卖")
    elif latest["RSI"] > 70:
        print("📈 RSI > 70 → 超买")
