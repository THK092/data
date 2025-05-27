import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
from datetime import datetime, timedelta

st.set_page_config(layout="wide")
st.title("🌍 글로벌 시가총액 TOP 10 기업 주가 시각화")
st.markdown("데이터 출처: Yahoo Finance")

# 티커 목록
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
        try:
            # 다운로드 시 group_by='ticker'는 기본 적용되므로 멀티 인덱스 대응 필요
            data = yf.download(ticker, start=start_date, end=end_date, progress=False)

            if data.empty:
                st.warning(f"⚠️ {name}의 데이터를 가져올 수 없습니다.")
                continue

            # 멀티 인덱스 처리 (예: BRK.B, 2222.SR 등)
            if isinstance(data.columns, pd.MultiIndex):
                if ('Adj Close', ticker) in data.columns:
                    y_data = data[('Adj Close', ticker)]
                elif 'Adj Close' in data.columns.levels[0]:
                    # fallback
                    y_data = data['Adj Close'].iloc[:, 0]
                else:
                    st.warning(f"⚠️ {name}의 'Adj Close' 데이터가 없습니다.")
                    continue
            else:
                if 'Adj Close' not in data.columns:
                    st.warning(f"⚠️ {name}의 'Adj Close' 데이터가 없습니다.")
                    continue
                y_data = data['Adj Close']

            fig.add_trace(go.Scatter(x=data.index, y=y_data, mode='lines', name=name))

        except Exception as e:
            st.error(f"❌ {name} 처리 중 오류 발생: {e}")
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
        st.error("📉 시각화할 수 있는 데이터가 없습니다.")
else:
    st.info("✅ 하나 이상의 기업을 선택해주세요.")
