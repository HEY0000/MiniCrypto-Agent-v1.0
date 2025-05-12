import yfinance as yf
import pandas as pd
import mplfinance as mpf
import talib  # ✅ 기술지표용 라이브러리 설치 필요

def plot_candlestick_with_indicators(ticker="ETH-USD", interval="1d", period="1mo"):
    try:
        data = yf.download(
            tickers=ticker,
            interval=interval,
            period=period,
            auto_adjust=False,
            actions=False,
            progress=False
        )
        if data.empty:
            raise ValueError("다운로드된 데이터가 비어 있습니다.")



        if isinstance(data.columns, pd.MultiIndex):
            data = data.xs(ticker, level="Ticker", axis=1)

        required_columns = ["Open", "High", "Low", "Close", "Volume"]
        if not all(col in data.columns for col in required_columns):
            raise ValueError("필수 컬럼 없음: " + str(data.columns))

        data.dropna(subset=required_columns, inplace=True)
        data.index = pd.to_datetime(data.index)

        # ✅ 이동평균선
        data["MA5"] = data["Close"].rolling(window=5).mean()
        data["MA20"] = data["Close"].rolling(window=20).mean()

        # ✅ RSI
        data["RSI"] = talib.RSI(data["Close"], timeperiod=14)

        # ✅ 골든크로스 감지
        data["golden_cross"] = (data["MA5"] > data["MA20"]) & (data["MA5"].shift() <= data["MA20"].shift())

        # ✅ 차트 그리기
        addplot = [
            mpf.make_addplot(data["MA5"], color='blue'),
            mpf.make_addplot(data["MA20"], color='orange'),
            mpf.make_addplot(data["RSI"], panel=1, color='green', ylabel='RSI')
        ]

        fig, _ = mpf.plot(
            data,
            type='candle',
            volume=True,
            style='yahoo',
            addplot=addplot,
            returnfig=True
        )
        return fig, data.tail(1)  # 마지막 줄 데이터 반환 → GPT 요약용

    except Exception as e:
        print(f"[plot_candlestick_with_indicators ERROR] {e}")
        return None, None
