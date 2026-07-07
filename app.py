import streamlit as st
import plotly.graph_objects as go
from agent import fetch_stock_data, calculate_indicators, get_agent_decision

st.set_page_config(page_title="AI Trading Agent", layout="wide")

st.title("AI Trading Agent")
st.markdown("Enter a stock ticker and get an AI-powered buy/sell/hold decision")

# Sidebar inputs
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Groq API Key", type="password")
    ticker = st.text_input("Stock Ticker", value="AAPL").upper()
    period = st.selectbox("Period", ["1mo", "3mo", "6mo", "1y"], index=2)
    analyze = st.button("Analyze Stock", use_container_width=True)

if analyze:
    if not api_key:
        st.error("Please enter your Groq API key in the sidebar")
    else:
        with st.spinner("Fetching data and analyzing..."):
            
            # Fetch and process data
            df = fetch_stock_data(ticker, period)
            df = calculate_indicators(df)
            
            # Layout
            col1, col2, col3, col4 = st.columns(4)
            latest = df.iloc[-1]
            
            col1.metric("Current Price", f"${latest['Close']:.2f}")
            col2.metric("RSI", f"{latest['RSI']:.1f}")
            col3.metric("MACD", f"{latest['MACD']:.4f}")
            col4.metric("Volume", f"{latest['Volume']:,.0f}")
            
            # Price chart
            st.subheader("Price Chart with Moving Averages")
            fig = go.Figure()
            fig.add_trace(go.Candlestick(
                x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'],
                name='Price'
            ))
            fig.add_trace(go.Scatter(x=df.index, y=df['MA20'], 
                                     name='MA20', line=dict(color='orange')))
            fig.add_trace(go.Scatter(x=df.index, y=df['MA50'], 
                                     name='MA50', line=dict(color='blue')))
            fig.update_layout(height=500, xaxis_rangeslider_visible=False)
            st.plotly_chart(fig, use_container_width=True)
            
            # RSI chart
            st.subheader("RSI Indicator")
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(x=df.index, y=df['RSI'], 
                                      name='RSI', line=dict(color='purple')))
            fig2.add_hline(y=70, line_dash="dash", line_color="red", 
                           annotation_text="Overbought (70)")
            fig2.add_hline(y=30, line_dash="dash", line_color="green", 
                           annotation_text="Oversold (30)")
            fig2.update_layout(height=300)
            st.plotly_chart(fig2, use_container_width=True)
            
            # AI Decision
            st.subheader("AI Agent Decision")
            decision = get_agent_decision(ticker, df, api_key)
            
            if "BUY" in decision.upper():
                st.success(f"**{decision}**")
            elif "SELL" in decision.upper():
                st.error(f"**{decision}**")
            else:
                st.warning(f"**{decision}**")