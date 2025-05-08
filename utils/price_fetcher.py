# utils/price_fetcher.py

import yfinance as yf

def get_price(ticker="BTC-USD"):
    coin = yf.Ticker(ticker)
    data = coin.history(period="1d", interval="1m")  # 1일치, 1분 간격
    latest = data.tail(1)  # 가장 최근 시세
    if not latest.empty:
        return {
            "price": round(latest["Close"].iloc[0], 2),
            "time": str(latest.index[0])
        }
    return {"price": None, "time": None}

# 테스트용
if __name__ == "__main__":
    btc = get_price("BTC-USD")
    print(f"BTC 가격: ${btc['price']} (기준: {btc['time']})")
