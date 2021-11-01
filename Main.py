from datetime import date


import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(
    page_title="Financial Dash",
    page_icon="🦧",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def MainMenu():

    # Text widgets are not displayed in rank order, i.e. all the headings appear before subheaders etc.
    # Instead, the formatting works in a sequential manner so whatever comes first is displayed first.

    # Title of the current section
    st.title("Hello & Welcome! 😃")

    # Provides a brief description of what the site is and what it can be used for (i.e. stock charting etc).
    st.header("**What is this site?  🤔**")
    st.write(
        """
    This site is split up into 3 sections excluding this one. Section 1 is Stock Charting & Indicators, section 2 is Reddit Trending Stocks, and section 3 is Financial 
    News. I will give a little description of each section in the hope of providing you with some understanding of what things are or do.
        
    """
    )
    st.header("Stock Charting & Indicators  📉")
    st.write(
        """    

    **Stock Charting**

    This section faciliates stock price charting using line charts, OHLC charts and Canldestick charts. 
    Line charts are plotted with the adjusted close price, this is represented as 'Adj Close' in the dataframe (*more to come on them later*). OHLC and Canldestick 
    charts use the 'Open', 'High', 'Low' and 'Close' columns from the dataframe. 

    Along the bottom of the chart you will see a family of badgers plus a long bar chart, this is shows the volume of stock traded on that day.

    The 'dataframe' is was referring to earlier is basically just a table containing the data. It is called a dataframe in the *library* I am using so I also use this term. 

    **Indicators**
    
    The availabe indicators are RSI, MACD and some averages. I may add more in the *future*, but for now these are all.

    *RSI*

    The relative strength index (RSI) is a momentum indicator used in technical analysis that measures the magnitude of recent price changes to evaluate overbought 
    or oversold conditions in the price of a stock or other asset. 
    
    Traditional interpretation and usage of the RSI are that values of 70 or above indicate that a security (e.g. a stock) is becoming overbought or overvalued and may
     be primed for a trend reversal or corrective pullback in price. An RSI reading of 30 or below indicates an oversold or undervalued condition.

    The formula to calculate RSI is split into two parts:

    Part One:
      """
    )
    # In this, LaTeX 'code' is implemented as fractions are used and these cannot be shown with a simple python string, the 'r' is
    # necessary to show what type it is (LaTeX), removing this would change the appearance of the formula to how it is currently written.
    st.latex(
        r"""
            RSI_{\text{step one}} = 100- \left[ \frac{100}{ 1 + \frac{\text{Average gain}}{\text{Average loss} }} \right]
     """
    )

    st.write(
        """
    Part two
    """
    )
    # In this, LaTeX 'code' is implemented as fractions are used and these cannot be shown with a simple python string, the 'r' is
    # necessary  to show what type it is (LaTeX), removing this would change the appearance of the formula to how it is currently written.‹
    st.latex(
        r"""
            RSI_{\text{step two}} = 100 - \left [ \frac{ 100 }{ 1 + \frac{ \left ( \text{Previous Average Gain} \times 13 \right ) \ + \ 
            \text{Current Gain} }{ \left ( \left ( \text{Previous Average Loss} \times 13 \right ) \ + \ \text{Current Loss} \right ) } } \right ]
     """
    )

    st.write(
        """
    ***Courtesy of Investopedia (https://www.investopedia.com).***
    """
    )

    st.write(
        """

    *MACD*

    Moving average convergence divergence (MACD) is a trend-following momentum indicator that shows the relationship between two moving averages of a security’s price. 
    The MACD is calculated by subtracting the 26-period exponential moving average (EMA) from the 12-period EMA.

    The result of that calculation is the MACD line. A nine-day EMA of the MACD called the "signal line," is then plotted on top of the MACD line, which can function 
    as a trigger for buy and sell signals.

    The formula for MACD:
    """
    )

    # This simply uses a raw python string to show the formula, "st.latex" is still used as this still changes the general appearnace
    # of the formula on the website
    st.latex("""MACD = 12PeriodEMA - 26PeriodEMA""")
    # Tell the user how to use the site, what needs inputting, what buttons do and so on.
    st.write(
        """
    ***Courtesy of Investopedia (https://www.investopedia.com).***
    """
    )

    st.header("Reddit Trending Stocks 📊 📈 🌖")

    st.write(
        """
    **Disclaimer**: whilst it should not happen, there may be some occurances in the chart that are not actually stock tickers. If this happens please do your best to ignore this.

    A bar chart showing the current trending stocks in the wallstreetbets subreddit will be present on screen. The height of the bar chart shows how many mentions there have 
    been of that stock ticker over the last *X* amount of posts. 
    
    """
    )

    st.header("Financial News 🚨 📰 🚨")

    st.write(
        "The recent financial news headlines will be displayed here. The headline will be accompanied with a link to the original article."
    )

    st.header("**How to use the site**")

    if st.checkbox("Show more text"):
        st.write(
            """
        **Sidebar**

        In the top left of this webpage, you will see an arrow. Clicking on this brings out the sidebar. It is through this that you will navigate throughout the 
        website.
        This is done using the dropdown menu.

        You will also enter a lot of the necessary inputs using the sidebar as well.

        **Help**

        Next to some inputs/buttons, you may see a '?', upon hovering over this, some text will appear which can tell you a little more about what something is or what 
        should be input. An example of this can be seen below.

        """
        )

    demo_text = st.text_input("foobar", help="This is some more info")

    if demo_text.upper() == "BADGER":
        st.info("tehe")

    st.write(
        """

    **Stock Charting**

    The required inputs for the stock charting are: a ticker, a start date and an end date. This is not an exhaustive list by any means, these are just the ones that you must use
    to make the program work. 


    **Reddit Trending Stocks & Financial News**

    There are no user requirements in these parts of the site, so I have little to explain in this section.

    """
    )


def Stock_Charting():

    # Variable for the max number of characters in a ticker.
    max_chars_ticker = 4

    # If statement to remove the chars cap if the stock is non-US.
    if st.sidebar.checkbox("Is this a non-US listed stock"):
        max_chars_ticker = None

    # The stock ticker is passed into the request made to yahoo finance. It is used as the name for the stock. Default Value of AAPL is used.
    ticker = st.sidebar.text_input(
        "Enter a stock ticker",
        "AAPl",
        help="""A stock ticker is an abbreviated name for a company. E.g. Tesla becomes TSLA and Facebook become FB. A 
        company's ticker can be found with a simple search.""",
        max_chars=max_chars_ticker,
    ).upper()

    # Removing all spaces in the string by replacing spaces (" ") with nothing ("")
    ticker = ticker.replace(" ", "")

    # Replacing any '.'s in the ticker in preparation for checking its alphanumeric
    ticker_wo_point = ticker.replace(".", "")

    # Checking the ticker is alphanumeric.
    if ticker_wo_point.isalnum() == False:
        st.error("Enter a valid stock ticker")

    # The first date prices are fetched from
    start_date = st.sidebar.date_input("Enter the first date you want prices from")
    # The final date prices are feteched from
    end_date = st.sidebar.date_input("Enter the lst date you want prices from")

    interval_options = [
        "1m",
        "2m",
        "5m",
        "15m",
        "30m",
        "60m",
        "1d",
        "1wk",
    ]
    # The select box containing all of the options for the interval, which will then be passed in the request to yahoo finance
    interval = st.sidebar.selectbox(
        "Please select an interval from the options below",
        interval_options,
        help="The interval is the gap between price quotes. Xm = minutes, Xd = days, Xwk = weeks",
    )

    # If statment that outputs error if any date is in the future
    if start_date > date.today() or end_date > date.today():
        st.error("Nice try 🦡 ! Dates cannot be in the future")
    # If statement to check that the start date is before the end date
    elif start_date > end_date:
        # Error message telling the user to input valid dates
        st.error("Start date must be before End date!")

    # The request to yahoo finance. The response is a pandas DataFrame and is consequently stored under the name df, meaning dataframe.
    df = yf.download(tickers=ticker, start=start_date, end=end_date, interval=interval)

    # Checkbox that when ticked will bring up the historical price data of the stock.
    if st.checkbox("View historical stock price data"):
        # Embedding the data frame containing the stock price data into the webpage
        st.dataframe(df)

   

    #df['date'] = pd.to_datetime(df['date'])

    st.sidebar.write("Select a chart type:")

    chart_type = "line"

    if st.sidebar.checkbox("Candlestick Chart"):
        chart_type = "Candlestick"
    elif st.sidebar.checkbox("OHLC chart"):
        chart_type = "Ohlc"

    if st.checkbox("Show chart"):
        if chart_type == "line":
            st.line_chart(df["Adj Close"])
        elif chart_type == "Candlestick":
            fig = go.Figure(
                data=go.Candlestick(
                    x=df.index,
                    open=df["Open"],
                    high=df["High"],
                    low=df["Low"],
                    close=df["Close"],
                )
            )
            st.plotly_chart(fig, use_container_width=True)

        elif chart_type == "Ohlc":
            fig = go.Figure(
                data=go.Ohlc(
                    x=df.index,
                    open=df["Open"],
                    high=df["High"],
                    low=df["Low"],
                    close=df["Close"],
                )
            )
            st.plotly_chart(fig, use_container_width=True)


def main():

    # An array that contains all of the options for the selectbox called "menu_select"
    menu_options = [
        "Main Menu",
        "Stock Charting & Indicators",
        "Reddit Trending Stocks",
        "Financial News",
    ]

    # The selectbox which allows you to navigate to different parts of the site, options are the items of "menu_options"
    menu_select = st.sidebar.selectbox(
        "Please select the section of the site you wish", menu_options
    )

    # Selection statement which will calls the corresponding function to the option selected previously
    if menu_select == "Main Menu":
        # Calls a function which brings up a Main Menu, which contains a description of the site‹
        MainMenu()
    elif menu_select == "Stock Charting & Indicators":
        # The function responsable for stock charting is called
        Stock_Charting()
    elif menu_select == "Reddit Trending Stocks":
        # The function responsable for Treding reddit stocks is called
        pass

    elif menu_select == "Financial News":
        # The function responable for the Financial News is called
        pass


if __name__ == "__main__":
    main()

