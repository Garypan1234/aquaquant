import yfinance as yf
import pandas as pd

stocks = ["AAPL", "NVDA", "TSLA", "VFV.TO"]

def calculate_rsi(close, window=14):
    delta = close.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

for stock in stocks:
    data = yf.download(stock, period="3mo", auto_adjust=True, progress=False)

    if data.empty:
        print(f"\n=== {stock} ===")
        print("没有拿到数据")
        continue

    close = data["Close"]

    # 防止 yfinance 返回 DataFrame 而不是 Series
    if isinstance(close, pd.DataFrame):
        close = close.iloc[:, 0]

    data = pd.DataFrame({"Close": close})
    data["MA5"] = data["Close"].rolling(5).mean()
    data["MA10"] = data["Close"].rolling(10).mean()
    data["RSI"] = calculate_rsi(data["Close"])

    data = data.dropna()

    if len(data) < 2:
        print(f"\n=== {stock} ===")
        print("数据不足，暂时不能分析")
        continue

    latest = data.iloc[-1]
    prev = data.iloc[-2]

    print(f"\n=== {stock} ===")
    print(f"Close: {latest['Close']:.2f}")
    print(f"MA5: {latest['MA5']:.2f}")
    print(f"MA10: {latest['MA10']:.2f}")
    print(f"RSI: {latest['RSI']:.2f}")

    if prev["MA5"] < prev["MA10"] and latest["MA5"] > latest["MA10"]:
        print("🔥 金叉 -> 可以关注买入")
    elif prev["MA5"] > prev["MA10"] and latest["MA5"] < latest["MA10"]:
        print("⚠️ 死叉 -> 注意风险")
    elif latest["MA5"] > latest["MA10"]:
        print("趋势: MA5 在 MA10 上方")
    else:
        print("趋势: MA5 在 MA10 下方")

    if latest["RSI"] < 30:
        print("📉 RSI < 30 -> 超卖")
    elif latest["RSI"] > 70:
        print("📈 RSI > 70 -> 超买")
    else:
        print("RSI 正常")
