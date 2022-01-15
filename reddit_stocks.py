import praw
import operator
import plotly.graph_objects as go
import streamlit as st


#Making the connection to the reddit API
reddit = praw.Reddit(
    client_id="wwHC3rv4KZi5rpSivJlXOg",
    client_secret="fBQYs5gUoHAWgPJPGA6KqcMehUMuJA",
    user_agent="MacOS:Fin_Dash:v1.1.1 (by u/_JM_56_)",
)

#Function to get the tickers and their number of mentions
def getData():

    #Getting the last 500 posts in wallstreetbets
    posts = reddit.subreddit("wallstreetbets").hot(limit=500)

    #Creating a dictionary to store the tickers (key) and the mentions (value)
    stocks_dict = {}

    #iterating through the posts
    for post in posts:

        #Spliting the title of each posts into a list with each item in the list as a word from the title
        title_list = post.title.split()

        #Iterating through the title list
        for word in title_list:
            word = word.upper()
            #checks if the word starts with $ (as used to denote stocks)and the 2nd letter is a letter 
            if word.startswith("$") and word[1:].isalpha():

                #if the word is not already in the dictionary its added and its value (mentions) is set to 1
                if word not in stocks_dict:
                    stocks_dict[word] = 1
                
                #If the word is already in the dictionary, its value (mentions) count is increased by one
                else:
                    stocks_dict[word] += 1

    #Dictionary is sorted into descending order by mentions
    # a sorted dictionary gets returned
    sorted_stock_dict = dict(sorted(stocks_dict.items(), key=operator.itemgetter(1), reverse = True))

    #Arrays for the tickers and mentions so they are easier to plot 
    tickers =[]
    mentions =[]
    
    #Adding each ticker to the tickers array and its mentions to the mention array
    for x in sorted_stock_dict:
        tickers.append(x)
        mentions.append(sorted_stock_dict[x])

    #Return tickers and mentions array
    return tickers, mentions

#Function to plot the bar chart
def Reddit_BarChart(x_data, y_data):
    #Code for bar chart with y axis as metions and x as tickers
    fig = go.Figure()
    fig.add_trace(go.Bar(x=x_data, y=y_data, name="Reddit Stock Mentions",marker = {'color' : 'orange'}))
    fig.update_xaxes(title_text="Ticker")
    fig.update_yaxes(title_text="Mentions")
    st.plotly_chart(fig)

