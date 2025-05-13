import yfinance as yf
import pandas as pd
import mplfinance as mpf
import talib
import numpy as np


def plot_candlestick_with_indicators(ticker="ETH-USD", interval="1d", period="1mo"):
    try:
        # 데이터 다운로드
        data = yf.download(
            tickers=ticker,
            interval=interval,
            period=period,
            auto_adjust=False,
            actions=False,
            progress=False
        )

        if data.empty:
            raise ValueError("❌ 다운로드된 데이터가 없습니다.")

        # 멀티인덱스 처리
        if isinstance(data.columns, pd.MultiIndex):
            data = data.xs(ticker, level="Ticker", axis=1)

        # 필수 컬럼 확인
        required_columns = ["Open", "High", "Low", "Close", "Volume"]
        if not all(col in data.columns for col in required_columns):
            raise ValueError("필수 컬럼 누락: " + str(data.columns))

        data.dropna(subset=required_columns, inplace=True)
        data.index = pd.to_datetime(data.index)

        # 이동평균선
        data["MA5"] = data["Close"].rolling(window=5).mean()
        data["MA20"] = data["Close"].rolling(window=20).mean()

        # RSI
        data["RSI"] = talib.RSI(data["Close"], timeperiod=14)

        # MACD
        data["MACD"], data["MACDSignal"], _ = talib.MACD(
            data["Close"], fastperiod=12, slowperiod=26, signalperiod=9
        )

        # 골든크로스
        data["golden_cross"] = (data["MA5"] > data["MA20"]) & (data["MA5"].shift() <= data["MA20"].shift())

        # 기술지표 NaN 제거
        data.dropna(subset=["MA5", "MA20", "RSI", "MACD", "MACDSignal"], inplace=True)

        # 차트 구성
        addplot = [
            mpf.make_addplot(data["MA5"], color='blue'),
            mpf.make_addplot(data["MA20"], color='orange'),
            mpf.make_addplot(data["RSI"], panel=1, color='green', ylabel='RSI'),
            mpf.make_addplot(data["MACD"], panel=2, color='red', ylabel='MACD'),
            mpf.make_addplot(data["MACDSignal"], panel=2, color='blue')
        ]

        # 캔들 차트 출력
        fig, _ = mpf.plot(
            data,
            type='candle',
            volume=True,
            style='yahoo',
            addplot=addplot,
            returnfig=True
        )
        return fig, data.tail(1)

    except Exception as e:
        print(f"[plot_candlestick_with_indicators ERROR] {e}")
        return None, None
