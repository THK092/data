import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
from datetime import datetime, timedelta

st.title("🌍 글로벌 시가총액 TOP 10 기업 주가 시각화")
st.markdown("데이터 출처: Yahoo Finance")

# 수정된 티커 목록
companies = {
    'Apple': 'AAPL',
    'Microsoft': 'MSFT',
    'Saudi Aramco': '2222.SR',  # 주의: 일부 지역에서는 차단될 수 있음
    'Alphabet (Google)': 'GOOGL',
    'Amazon': 'AMZN',
    'Nvidia': 'NVDA',
    'Meta (Facebook)': 'META',
    'Berkshire Hathaway': 'BRK.B',  # 수정됨
    'Tesla': 'TSLA',
    'TSMC': 'TSM'
}

# 날짜 범위 설정
end_date = datetime.today()
start_date = end_date - timedelta(days=365)

# 기업 선택
selected_companies = st.multiselect(
    "📈 시각화할 기업을 선택하세요",
    options=list(companies.keys()),
    default=['Apple', 'Microsoft', 'Nvidia']
)

# 시각화
if selected_companies:
    fig = go.Figure()
    for name in selected_companies:
        ticker = companies[name]
        data = yf.download(ticker, start=start_date, end=end_date)

        if data.empty:
            st.warning(f"⚠️ {name}의 데이터를 가져올 수 없습니다.")
            continue

        fig.add_trace(go.Scatter(x=data.index, y=data['Adj Close'], mode='lines', name=name))

    fig.update_layout(
        title="📊 글로벌 시가총액 상위 기업 주가 (최근 1년)",
        xaxis_title="날짜",
        yaxis_title="조정 종가 (USD)",
        hovermode="x unified"
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("좌측에서 하나 이상의 기업을 선택해주세요.")
