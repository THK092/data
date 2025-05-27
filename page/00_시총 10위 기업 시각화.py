import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
from datetime import datetime, timedelta

st.title("🌍 글로벌 시가총액 TOP 10 기업 주가 시각화")
st.markdown("데이터 출처: Yahoo Finance")

companies = {
    'Apple': 'AAPL',
    'Microsoft': 'MSFT',
    'Saudi Aramco': '2222.SR',
    'Alphabet (Google)': 'GOOGL',
    'Amazon': 'AMZN',
    'Nvidia': 'NVDA',
    'Meta (Facebook)': 'META',
    'Berkshire Hathaway': 'BRK.B',
    'Tesla': 'TSLA',
    'TSMC': 'TSM'
}

end_date = datetime.today()
start_date = end_date - timedelta(days=365)

default_companies = ['Apple', 'Microsoft', 'Nvidia']
selected_companies = st.multiselect(
    "📈 시각화할 기업을 선택하세요",
    options=list(companies.keys()),
    default=default_companies
)

if selected_companies:
    fig = go.Figure()
    for name in selected_companies:
        ticker = companies[name]
        data = yf.download(ticker, start=start_date, end=end_date, progress=False)

        if data.empty:
            st.warning(f"⚠️ {name}의 데이터를 가져올 수 없습니다.")
            continue

        # 안전하게 'Adj Close'가 있는지 확인
        if 'Adj Close' in data.columns:
            fig.add_trace(go.Scatter(x=data.index, y=data['Adj Close'], mode='lines', name=name))
        else:
            st.warning(f"⚠️ {name}의 데이터에 'Adj Close' 컬럼이 없습니다.")
            continue

    if fig.data:
        fig.update_layout(
            title="📊 글로벌 시가총액 상위 기업 주가 (최근 1년)",
            xaxis_title="날짜",
            yaxis_title="조정 종가 (USD)",
            hovermode="x unified"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("⚠️ 표시할 수 있는 데이터가 없습니다.")
else:
    st.info("좌측에서 하나 이상의 기업을 선택해주세요.")
