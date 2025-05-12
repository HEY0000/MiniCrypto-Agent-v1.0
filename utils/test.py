# test_chart.py

from chart_generator import plot_candlestick
import matplotlib.pyplot as plt



coin_name = "ETH-USD"

fig = plot_candlestick(ticker=coin_name, interval="1d", period="1mo")
if fig:
    print("✅ 차트 생성 성공")
    plt.show()
else:
    print("❌ 차트 생성 실패")
