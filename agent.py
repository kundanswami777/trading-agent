import yfinance as yf
import pandas as pd
import ta
from groq import Groq

def fetch_stock_data(ticker, period="6mo"):
    stock = yf.Ticker(ticker)
    df = stock.history(period=period)
    return df

def calculate_indicators(df):
    df['RSI'] = ta.momentum.RSIIndicator(df['Close']).rsi()
    df['MACD'] = ta.trend.MACD(df['Close']).macd()
    df['MACD_signal'] = ta.trend.MACD(df['Close']).macd_signal()
    df['MA20'] = df['Close'].rolling(window=20).mean()
    df['MA50'] = df['Close'].rolling(window=50).mean()
    return df.dropna()

def get_agent_decision(ticker, df, api_key):
    latest = df.iloc[-1]
    
    summary = f"""
    Stock: {ticker}
    Current Price: {latest['Close']:.2f}
    RSI: {latest['RSI']:.2f}
    MACD: {latest['MACD']:.4f}
    MACD Signal: {latest['MACD_signal']:.4f}
    20-day MA: {latest['MA20']:.2f}
    50-day MA: {latest['MA50']:.2f}
    Volume: {latest['Volume']:,.0f}
    """

    client = Groq(api_key=api_key)
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """You are an expert stock market analyst. 
                Analyze the given technical indicators and give a clear 
                BUY, SELL, or HOLD recommendation with a brief explanation.
                Keep your response under 150 words. Be direct and confident."""
            },
            {
                "role": "user",
                "content": f"Analyze these indicators and give a decision:\n{summary}"
            }
        ]
    )
    
    return response.choices[0].message.content