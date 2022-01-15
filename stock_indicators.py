import plotly.graph_objects as go

class indicators:
    def __init__(self, fig, df):
        self.fig = fig
        self.df = df

    def MA20(self):
        # Calculating the moving average over the last 20 rows in the data frame
        self.df["MA20"] = self.df["Adj Close"].rolling(window=20).mean()
        self.fig.add_trace(
            go.Scatter(
                x=self.df.index,
                y=self.df["MA20"],
                line=dict(color="blue", width=2),
                name="MA20",
            ),
            row=1,
            col=1,
        )
        return self.fig

    def MA60(self):
        # Calculating the moving average over the last 20 rows in the data frame
        self.df["MA60"] = self.df["Adj Close"].rolling(window=60).mean()
        self.fig.add_trace(
            go.Scatter(
                x=self.df.index,
                y=self.df["MA60"],
                line=dict(color="pink", width=2),
                name="MA60",
            ),
            row=1,
            col=1,
        )
        return self.fig

    def RSIcalc(self):
        df = self.df
        # RSI calculated using the prior 14 intervals
        df["Price Change"] = df["Adj Close"].pct_change()
        df["Up"] = df["Price Change"].apply(
            lambda x: x if x > 0 else 0
        )  # replacing all negative values witha 0
        df["Down"] = df["Price Change"].apply(
            lambda x: abs(x) if x < 0 else 0
        )  # replacing all positive values with a 0
        df.dropna()  # getting rid of all fields containing zeros to not affect the average

        # Calculating the average ups and downs
        df["Avg Up"] = df["Up"].ewm(span=27, min_periods=14).mean()
        df["Avg Down"] = df["Down"].ewm(span=27, min_periods=14).mean()

        # Calculating the relative strength
        df["RS"] = df["Avg Up"] / df["Avg Down"]

        # Converting the relative strength to an index
        df["RSI"] = 100 - (100 / (1 + df["RS"]))

        # Getting rid of unnecessary columns
        df = df.drop(columns=["Avg Up", "Avg Down", "Up", "Down", "Price Change", "RS"])

        return df

    def MACDcalc(self):
        df = self.df

        # Calculating the 12 period EMA
        df["EMA12"] = df["Adj Close"].ewm(span=12, min_periods=12).mean()

        # Calculating the 26 period EMA
        df["EMA26"] = df["Adj Close"].ewm(span=26, min_periods=26).mean()

        # Getting the MACD
        df["MACD"] = df["EMA12"] - df["EMA26"]

        # Calculating signal line
        df["Signal"] = df["MACD"].ewm(span=9, min_periods=9).mean()

        # Getting rid of unnecessary columns
        df = df.drop(columns=["EMA12", "EMA26"])

        return df

    def RSIplot(self):
        df = self.df

        # Creating a line chart of the RSI
        self.fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df["RSI"],
                line=dict(color="lightblue", width=2),
                name="RSI",
            ),
            row=3,
            col=1,
        )
        return self.fig

    def MACDplot(self):
        df = self.df

        # Creating the line chart for the MACD
        self.fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df["MACD"],
                line=dict(color="orange", width=2),
                name="MACD",
            ),
            row=4,
            col=1,
        )

        # Creating the line chart for the Signal
        self.fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df["Signal"],
                line=dict(color="grey", width=2),
                name="Signal",
            ),
            row=4,
            col=1,
        )
        return self.fig
