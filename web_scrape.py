from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st

def get_news():
    # url of website news is being scraped from without the ticker
    finviz_url = "https://finviz.com/quote.ashx?t="

    # ticker the news will be about
    ticker = st.text_input("Enter the tickers you want news about", "AMZN")

    # full url including the ticker
    url = finviz_url + ticker

    i = 0

    while i < 100:
        try:
            # making the request to the data
            req = Request(url=url, headers={"user-agent": "my-app"})
            response = urlopen(req)
            html = BeautifulSoup(response, "html.parser")

            # exttracting the rowns from the table in the webpage
            news_table = html.find(id="news-table")
            stock_rows = news_table.findAll("tr")

            # Array of the timestamps
            time_stamps = []

            # Array of the headline
            titles = []

            # Array of the links to the original
            links = []

            # Getting the healines and publication by accessing the text of the anchor tag
            for row in stock_rows:
                title = row.a.text
                titles.append(title)

                time = row.td.text
                time_stamps.append(time)

                i +=1

            # Getting all links from the table rows
            for link in news_table.find_all("a"):
                # adding the links to the links list
                if 'href' in link.attrs:
                    links.append(link.attrs["href"])
                    i +=1

            # Creating the data frame for the news
            news_df = pd.DataFrame()
            
            news_df.index = time_stamps
            news_df["Healines"] = titles
            
            if st.checkbox("Show Links"):
                news_df["Links"] = links
                
                i+=1
            
            #Adding it to the main page
            st.table(news_df)
        except:
            st.error("ENTER A VALID TICKER")
            i=100
