import sys
from yahoo_finance_api2 import share
from yahoo_finance_api2.exceptions import YahooFinanceError
import pandas as pd


class histroical_data:
    def __init__(self, code):
        self.df = pd.DataFrame()
        self.code = str(code)

    def get_data_from_yahoo(self,span_in_year):
        my_share = share.Share(self.code)
        symbol_data = None
        try:
            symbol_data = my_share.get_historical(
            share.PERIOD_TYPE_YEAR, span_in_year,
            share.FREQUENCY_TYPE_DAY, 1)
        except YahooFinanceError as e:
            print(e.message)
            sys.exit(1)

        self.df = pd.DataFrame(symbol_data)
        self.df["datetime"] = pd.to_datetime(self.df.timestamp, unit="ms")
        self.df.head()

    def print_df(self):
        print(self.code)
        print(self.df)

a = histroical_data('^SKEW')
a.get_data_from_yahoo(40)
a.print_df()