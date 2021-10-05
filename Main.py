from datetime import datetime

import pandas  as pd
import plotly.graph_objects as go
import praw
import streamlit as st
import yfinance as yf
from plotly.subplots import make_subplots


reddit = praw.Reddit(
    client_id="wwHC3rv4KZi5rpSivJlXOg",
    client_secret="fBQYs5gUoHAWgPJPGA6KqcMehUMuJA",
    user_agent="MacOS:Fin_Dash:v1.1.1 (by u/_JM_56_)",
)

global chart_type


def main():
    # List of possible options for the site
    menu_options = ["Stock Charting", "Reddit Trending Stocks", "Financial News"]

    menu = st.sidebar.selectbox("Select an Option", menu_options)

    if menu == "Stock Charting":
        stock_charting()
    elif menu == "Reddit Trending Stocks":
        reddit()
    elif menu == "Financial News":
        pass


def makeChart(df, chart_type):
    #return fig
    pass


# Function to find the difference between two dates. As if the difference is larger than 30,
# then the interval between price quotes cannot be 1 or 2 minutes as this would generate too many data points


def RSIcalc(df):
    #Typically RSI is calculated using the prior 14 days, therefore I will also be using 14 days
    
    df['Price Change'] = df['Adj Close'].pct_change()
    df['Up'] = df['Price Change'].apply(lambda x : x if x > 0 else 0) # replacing all negative values witha 0 
    df['Down'] = df['Price Change'].apply(lambda x : abs(x) if x < 0 else 0) # replacing all positive values with a 0
    df.dropna() # getting rid of all fields containing zeros to not affect the average

    df['Avg Up'] = df['Up'].ewm(span = 27).mean()
    df['Avg Down'] = df['Down'].ewm(span = 27).mean()
    
    df['RS'] = df['Avg Up']/df['Avg Down']
    df['RSI'] = 100 - (100/(1+df['RS']))
    return df



def date_difference(start_date, end_date):
    return abs((start_date - end_date).days)


def stock_charting():
    st.header("Stock Charting")
    st.text(
        """
    Enter a stock ticker(name), a start date, an end date, and an interval in the sidebar. 
    Once all of these have been added a chart of the stocks historical stock price will appear
    """
    )

    stock_ticker = st.sidebar.text_input("Enter the ticker of the stock").upper()

    start_date = st.sidebar.date_input("Enter the start date from when you want prices")

    end_date = st.sidebar.date_input("Enter the end date up to where you want prices")

    date_diff = date_difference(start_date, end_date)

    if date_diff < 30:
        # array containing all the interval options for the chart
        interval_timings = [
            "1m",
            "2m",
            "5m",
            "15m",
            "60m",
        ]
        interval = st.sidebar.selectbox(
            "Enter the interval in minutes", interval_timings
        )
    else:
        # array containing all the interval options for the chart
        interval_timings = [
            "5m",
            "15m",
            "60m",
        ]
        interval = st.sidebar.selectbox(
            "Enter the interval in minutes", interval_timings
        )

    df = yf.download(stock_ticker, start_date, end_date)

    print(df)

    st.dataframe(df)

    RSIcalc(df)

    if st.sidebar.checkbox("Candlestick chart"):
        chart_type = "Candlestick"
    if st.sidebar.checkbox("OHLC chart"):
        chart_type = "Ohlc"

    if st.sidebar.button("Graph"):
        st.plotly_chart(plot_chart(df, chart_type)) #config)


def reddit():

    st.header("Trending Stocks")
    st.markdown("The **hot** stocks on 'wallstreetbets' over the last 12 hours")


if __name__ == "__main__":
    main()
