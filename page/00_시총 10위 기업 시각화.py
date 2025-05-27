import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
from datetime import datetime, timedelta

st.set_page_config(layout="wide")
st.title("🌍 글로벌 시가총액 TOP 10 기업 주가 시각화")
st.markdown("데이터 출처: Yahoo Finance")

# 기업과 티커 매핑
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

# 기본 기간 설정
end_date = datetime.today()
start_date = end_date - timedelta(days=365)

# 사용자 선택
default_companies = ['Apple', 'Microsoft', 'Nvidia']
selected_companies = st.multiselect(
    "📈 시각화할 기업을 선택하세요",
    options=list(companies.keys()),
    default=default_companies
)

# 시각화
if selected_companies:
    fig = go.Figure()

    for name in selected_companies:
        ticker = companies[name]
        try:
            # 단일 티커 방식 사용 (가장 안전함)
            stock = yf.Ticker(ticker)
            data = stock.history(start=start_date, end=end_date)

            if data.empty:
                st.warning(f"⚠️ {name}의 데이터를 가져올 수 없습니다.")
                continue

            # Adj Close 존재 여부 확인
            if 'Adj Close' in data.columns:
                fig.add_trace(go.Scatter(
                    x=data.index, y=data['Adj Close'],
                    mode='lines', name=name
                ))
            else:
                st.warning(f"⚠️ {name}에 'Adj Close' 데이터가 없습니다.")

        except Exception as e:
            st.error(f"❌ {name} 오류: {e}")

    if fig.data:
        fig.update_layout(
            title="📊 글로벌 시가총액 상위 기업 주가 (최근 1년)",
            xaxis_title="날짜",
            yaxis_title="조정 종가 (USD)",
            hovermode="x unified"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("⚠️ 유효한 데이터를 가진 기업이 없습니다.")
else:
    st.info("✅ 하나 이상의 기업을 선택해주세요.")
