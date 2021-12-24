import sys
from pandas.tseries.offsets import Day
from yahoo_finance_api2 import share
from yahoo_finance_api2.exceptions import YahooFinanceError
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt


class histroical_data:
    def __init__(self, code, span_in_year):
        self.code = str(code)
        self.df = pd.DataFrame(self.get_data_from_yahoo(span_in_year))
        self.add_calculated_columns()

    def get_data_from_yahoo(self, span_in_year):
        my_share = share.Share(self.code)
        symbol_data = None
        try:
            symbol_data = my_share.get_historical(
                            share.PERIOD_TYPE_YEAR, span_in_year,
                            share.FREQUENCY_TYPE_DAY, 1)
        except YahooFinanceError as e:
            print(e.message)
            sys.exit(1)
        df = pd.DataFrame(symbol_data)
        df = df.ffill()
        return df
    
    def add_calculated_columns(self):
        self.add_date_and_time_to_df()
        self.add_calculated_value_to_df()

    def add_date_and_time_to_df(self):
        self.df["datetime"] = pd.to_datetime(self.df.timestamp, unit="ms")
        self.df["date"] = self.df["datetime"].dt.date
        self.df["previous_date"] = (self.df["datetime"] - Day(1)).dt.date

    def add_calculated_value_to_df(self):
        self.df["dailyFluction"] = self.df["close"].diff()
        self.df["dailyFluctionPCT"] = self.df["close"].pct_change()*100

    def plot_df(self):
        self.df.plot(x="datetime", y="close", alpha=0.5)
        plt.show()

    def print_df(self):
        print(self.code)
        print(self.df)

skew = histroical_data('^SKEW', 1)
skew.print_df()

## test