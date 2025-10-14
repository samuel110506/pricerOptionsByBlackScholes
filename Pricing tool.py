# -*- coding: utf-8 -*-
"""
Created on Tue Oct  7 15:16:12 2025

@author: samue
"""

from scipy.stats import norm
import numpy as np
import yfinance as yf
import numpy.random as rd
import streamlit as st
import matplotlib.pyplot as plt
import datetime
from dateutil.relativedelta import relativedelta

st.title("Pricing tool Call and Put options by Black-Scholes")
tickers= [
    # Commodities
    "GC=F", "SI=F", "CL=F", "BZ=F", "NG=F", "HG=F", "ZS=F", "KC=F",
    # Indices
    "^GSPC", "^DJI", "^IXIC", "^FTSE", "^GDAXI", "^FCHI", "^N225", "^HSI",
    # Equities
    "AAPL", "MSFT", "AMZN", "GOOG", "META", "TSLA", "NVDA", "JPM", "XOM", "BRK-B"
]

rates = [0.02,0.021,0.022,0.023,0.024,0.025,0.026,0.027,0.028,0.029,
         0.03,0.031,0.032,0.033,0.034,0.035,0.036,0.037,0.038,0.039,
         0.04,0.041,0.042,0.043,0.044,0.045,0.046,0.047,0.048,0.049,0.05]

today=datetime.date.today()

riskfreerate=st.selectbox("Select a rate:", rates, format_func=lambda x: f"{(x*100):.1f}%")
asset=st.selectbox("Select an asset:",tickers)
stock_price = yf.Ticker(asset).info["regularMarketPrice"]
print(stock_price)
maturity=st.date_input("Select the maturity of the option",value=today+ datetime.timedelta(days=1),min_value=today+ datetime.timedelta(days=1))
time=(maturity-today).days/365.25
strikeprice = st.number_input("Select the strike price :", min_value=1.0, value=1.0, format="%.2f")

data = yf.download(asset, start=today-relativedelta(years=1), end=today)
data['Return'] = data['Close'].pct_change()
returns = data['Return'].dropna()
sigma=returns.std()*np.sqrt(252)
print(sigma)

d1=(np.log(stock_price/strikeprice)+(riskfreerate+(1/2)*sigma**2)*time)/(sigma*np.sqrt(time))
d2=d1-sigma*np.sqrt(time)

call=stock_price*norm.cdf(d1)-strikeprice*np.exp((-1)*riskfreerate*time)*norm.cdf(d2)
put=strikeprice*np.exp((-1)*riskfreerate*time)*norm.cdf(-d2)-stock_price*norm.cdf(-d1)


st.write(f"Call Price: USD {call:.2f}")

st.write(f"Put Price: USD {put:.2f}")

st.markdown(
    """
    ---
    👤 **Samuel ZEITOUN, SKEMA PGE Student**  
    🔗 [LinkedIn](https://www.linkedin.com/in/szeitoun11/)  
    📧 [Email](mailto:samuel.zeitoun@skema.edu)
    """,
    unsafe_allow_html=True
)










