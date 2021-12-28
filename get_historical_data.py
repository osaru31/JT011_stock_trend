import sys
from pandas.tseries.offsets import Day
from yahoo_finance_api2 import share
from yahoo_finance_api2.exceptions import YahooFinanceError
import pandas as pd
import matplotlib.pyplot as plt
import tableFunction as tf


class histroical_data:
    def __init__(self, code, span_in_year):
        self.code = str(code)
        self.df = pd.DataFrame(self.get_data_from_yahoo(span_in_year))
        self.add_date_and_time_to_df()

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
        self.add_calculated_value_to_df()

    def add_date_and_time_to_df(self):
        self.df["timestamp"] = pd.to_datetime(self.df["timestamp"], unit="ms")
        self.df = self.df.rename(columns={'timestamp': 'datetime'})
        self.df["date"] = self.df["datetime"].dt.date
        self.df["previous_date"] = (self.df["datetime"] - Day(1)).dt.date

    def add_calculated_value_to_df(self):
        self.df["dailyFluction"] = self.df["close"].diff()
        self.df["dailyFluctionPCT"] = self.df["close"].pct_change()*100
        self.df["weeklyavg"] = self.df["close"] - self.df["close"].rolling(7).mean()
        self.df["weeklyavgdiff"] = self.df["weeklyavg"].diff()
        self.df["weeklystdev"]= self.df["close"].rolling(7).std()
        self.df["weeklyslope"]= self.df["close"].rolling(7, min_periods=4).apply(tf.get_slope_adjusted, raw=False)
        self.df["monthlyavg"] = self.df["close"] - self.df["close"].rolling(30).mean()
        self.df["monthlyavgdiff"] = self.df["monthlyavg"].diff()
        self.df["monthlystdev"]= self.df["close"].rolling(30).std()
        self.df["monthlyslope"]= self.df["close"].rolling(30, min_periods=15).apply(tf.get_slope_adjusted, raw=False)
        self.df["quarterlyavg"] = self.df["close"] - self.df["close"].rolling(120).mean()
        self.df["quarterlyavgdiff"] = self.df["quarterlyavg"].diff()
        self.df["quarterlystdev"]= self.df["close"].rolling(120).std()
        self.df["quarterlyslope"]= self.df["close"].rolling(120, min_periods=60).apply(tf.get_slope_adjusted, raw=False)
        self.df["yearlyavg"] = self.df["close"] - self.df["close"].rolling(365).mean()
        self.df["yearlyavgdiff"] = self.df["yearlyavg"].diff()
        self.df["yearlystdev"]= self.df["close"].rolling(365).std()
        self.df["yearlyslope"]= self.df["close"].rolling(365, min_periods=180).apply(tf.get_slope_adjusted, raw=False)

    def plot_df(self):
        self.df.plot(x="datetime", y="close", alpha=0.5)
        plt.show()

    def print_df(self):
        print(self.code)
        print(self.df)

skew = histroical_data('^VIX', 2)
skew.plot_df()
skew.add_calculated_columns()
skew.print_df()
skew.df.to_csv('df.csv')
skew.df.plot.scatter(x="datetime", y="yearlyslope", alpha=0.3)
plt.show()

## test