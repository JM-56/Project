import plotly.graph_objects as go
import math

def time_to_float(df):
    # Selecting tbe 1st and last rows of the data frame
    start = df.index[0]
    end = df.index[-1]

    # Accessing the time attribute of the rows
    start_time = start.time()
    end_time = end.time()

    # Converting the times to integer forms
    start_time_int = int(start_time.strftime("%H%M%S")) / 10000
    end_time_int = int(end_time.strftime("%H%M%S")) / 10000

    # Converting the start time as an integer to float but with the decimal changed to be as a proportion of 60 mins
    split_start = math.modf(start_time_int)
    start_as_float = split_start[1] + split_start[0] * (5 / 3)

    # Converting the end time as an integer to a float but with the decimal changed to be as a proportion of 60 mins
    split_end = math.modf(end_time_int)
    # Adding 0.05 on as the boundaries are inclusive of the values so without this addition the last price quote is ommited from the graph
    end_as_float = math.ceil(split_end[1] + (split_end[0] * (5 / 3))) + 0.05

    return start_as_float, end_as_float

# Class for the charting
class PriceCharting:
    def __init__(
        self,
        fig,
        df,
        interval,
    ):
        self.fig = fig
        self.df = df
        self.interval = interval

    # creating the candlestick chart
    def Candlestick_chart(self):

        self.fig.add_trace(
            go.Candlestick(
                x=self.df.index,
                open=self.df["Open"],
                high=self.df["High"],
                low=self.df["Low"],
                close=self.df["Close"],
                name="Candlestick Chart",
            ),
            row=1,
            col=1,
        )
        # Filtering out weekends and non-trading hours
        if self.interval == "1d":
            self.fig.update_xaxes(
                rangebreaks=[
                    dict(bounds=["sat", "mon"]),
                ],
            )
        elif self.interval != "1wk":
            # Calling function to give the time of the 1st and last price quote
            start, end = time_to_float(self.df)

            self.fig.update_xaxes(
                rangebreaks=[
                    dict(bounds=["sat", "mon"]),
                    dict(bounds=[end, start], pattern="hour"),
                ],
            )
        # Removing the rangeslider as it overlaps with other charts
        self.fig.update_layout(xaxis_rangeslider_visible=False)
        return self.fig

    def OHLC_chart(self):
        # Creating OHLC chart
        self.fig.add_trace(
            go.Ohlc(
                x=self.df.index,
                open=self.df["Open"],
                high=self.df["High"],
                low=self.df["Low"],
                close=self.df["Close"],
                name="OHLC chart",
            ),
            row=1,
            col=1,
        )
        # Removing the weekends and non-trading hours
        if self.interval == "1d":
            self.fig.update_xaxes(
                rangebreaks=[
                    dict(bounds=["sat", "mon"]),
                ],
            )
        elif self.interval != "1wk":
            # Calling function to the give the time of the 1st and last price quote
            start, end = time_to_float(self.df)

            self.fig.update_xaxes(
                rangebreaks=[
                    dict(bounds=["sat", "mon"]),
                    dict(bounds=[end, start], pattern="hour"),
                ],
            )
            pass
        # Remving range slider
        self.fig.update_layout(xaxis_rangeslider_visible=False)
        return self.fig

    # Creating volume bar chart
    def Volume_chart(self):

        self.fig.add_trace(
            go.Bar(x=self.df.index, y=self.df["Volume"], name="Volume"), row=2, col=1
        )
        return self.fig
