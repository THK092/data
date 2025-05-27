import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
from datetime import datetime, timedelta

# 앱 제목
st.title("🌎 글로벌 시가총액 TOP 10 기업 주가 시각화")
st.markdown("데이터 출처: Yahoo Finance (야후 파이낸스)")

# 시가총액 기준 상위 10개 기업
companies = {
    'Apple': 'AAPL',
    'Microsoft': 'MSFT',
    'Saudi Aramco': '2222.SR',
    'Alphabet (Google)': 'GOOGL',
    'Amazon': 'AMZN',
    'Nvidia': 'NVDA',
    'Meta (Facebook)': 'META',
    'Berkshire Hathaway': 'BRK-B',
    'Tesla': 'TSLA',
    'TSMC': 'TSM'
}

# 날짜 선택
end_date = datetime.today()
start_date = end_date - timedelta(days=365)

# 사용자 선택 옵션
selected_companies = st.multiselect(
    "📈 시각화할 기업을 선택하세요",
    options=list(companies.keys()),
    default=['Apple', 'Microsoft', 'Nvidia']
)

# 데이터 다운로드 및 시각화
if selected_companies:
    fig = go.Figure()
    for name in selected_companies:
        ticker = companies[name]
        try:
            data = yf.download(ticker, start=start_date, end=end_date)
            fig.add_trace(go.Scatter(x=data.index, y=data['Adj Close'], mode='lines', name=name))
        except:
            st.warning(f"{name}의 데이터를 가져오는 데 실패했습니다.")

    fig.update_layout(
        title="📊 글로벌 시가총액 상위 기업 주가 (최근 1년)",
        xaxis_title="날짜",
        yaxis_title="조정 종가 (USD)",
        hovermode="x unified"
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("좌측에서 하나 이상의 기업을 선택해주세요.")
