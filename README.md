# AI Trading Agent

I built this because I was curious about one question: can an LLM 
actually reason over numbers, or does it just pattern-match text?

Turns out — when you give it structured financial indicators with 
context, it reasons surprisingly well. This agent fetches real stock 
data, computes technical indicators, and asks Llama 3.3 to think 
through them like an analyst would.

## What it does
You enter a stock ticker. The agent pulls 6 months of real price 
data, calculates RSI, MACD, and moving averages, then sends everything 
to Llama 3.3-70B via Groq. The model returns a buy/sell/hold decision 
with a plain-English explanation of its reasoning.

## Why I built it this way
Most trading tools just flag indicators mechanically — RSI above 70 
means overbought, done. I wanted to see if an LLM could weigh multiple 
signals together and explain the tradeoffs, the way a human analyst 
would. It can, and the explanations are actually useful.

## Tech Stack
Python · yfinance · Groq API · Llama 3.3-70B · Streamlit · Plotly · pandas · ta

## Indicators used
| Indicator | What it captures |
|---|---|
| RSI | Whether the stock is overbought or oversold |
| MACD | Direction and strength of the current trend |
| MA20 / MA50 | Short and long term price momentum |

## How to run it yourself
1. Clone the repo
2. pip install -r requirement.txt
3. Get a free Groq API key at console.groq.com — takes 2 minutes
4. streamlit run app.py
5. Enter your API key and any ticker you want

## Honest limitations
This is built on technical indicators only. It knows nothing about 
earnings, news, or macro conditions. I wouldn't use it for real 
investment decisions — but as a demonstration of LLM reasoning over 
structured data, it works well.
