import sys
from yahoo_finance_api2 import share
from yahoo_finance_api2.exceptions import YahooFinanceError
import pandas as pd

my_share = share.Share('^SKEW')
symbol_data = None

try:
    symbol_data = my_share.get_historical(
        share.PERIOD_TYPE_YEAR, 40,
        share.FREQUENCY_TYPE_DAY, 1)
except YahooFinanceError as e:
    print(e.message)
    sys.exit(1)

df = pd.DataFrame(symbol_data)
df["datetime"] = pd.to_datetime(df.timestamp, unit="ms")
df.head()
print(df)
