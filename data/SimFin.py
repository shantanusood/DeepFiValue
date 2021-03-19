import pandas as pd
import seaborn as sns

# Import the main functionality from the SimFin Python API.
import simfin as sf

# Import names used for easy access to SimFin's data-columns.
from simfin.names import *

sf.set_data_dir('~/simfin_data/')
sf.load_api_key(path='~/simfin_api_key.txt', default_key='free')

# We are interested in the US stock-market.
## market = 'us'

# List of tickers we want. If None then all tickers are used.
## tickers = ['AAPL', 'AMZN', 'MSFT']

# Add this date-offset to the fundamental data such as
# Income Statements etc., because the REPORT_DATE is not
# when it was actually made available to the public,
# which can be 1, 2 or even 3 months after the Report Date.
## offset = pd.DateOffset(days=60)

# Refresh the fundamental datasets (Income Statements etc.)
# every 30 days.
## refresh_days = 30

# Refresh the dataset with shareprices every 10 days.
## refresh_days_shareprices = 10

## hub = sf.StockHub(market=market, tickers=tickers, offset=offset, refresh_days=refresh_days, refresh_days_shareprices=refresh_days_shareprices)

## df_prices = hub.load_shareprices(variant='daily')

## print(df_prices.head())


## df_prices = hub.load_shareprices(variant='daily')

## df_income_ttm = hub.load_income(variant='ttm')

## print(df_income_ttm.head())

df = sf.load_income(variant='annual', market='us')

# Print all Revenue and Net Income for Microsoft (ticker MSFT).
print(df.loc['ZM', [REVENUE, NET_INCOME]])

df_prices = sf.load_shareprices(market='us', variant='daily')

# Plot the closing share-prices for ticker MSFT.
print(df_prices.loc['MSFT', CLOSE])